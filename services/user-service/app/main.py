import logging
from contextlib import asynccontextmanager

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import models, schemas, security
from .db import Base, engine, get_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s user-service %(message)s")
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # create tables on startup
    log.info("database tables ready")
    yield


app = FastAPI(title="User Service", version="1.0.0", lifespan=lifespan)
Instrumentator().instrument(app).expose(app)  # exposes /metrics for Prometheus
bearer = HTTPBearer()


def current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)
) -> models.User:
    try:
        user_id = security.decode_token(creds.credentials)
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User no longer exists")
    return user


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "service": "user-service"}


@app.post("/users/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(body: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(models.User).where(models.User.email == body.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    user = models.User(
        email=body.email,
        full_name=body.full_name,
        password_hash=security.hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    log.info("registered user id=%s", user.id)
    return user


@app.post("/users/login", response_model=schemas.Token)
def login(body: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.scalar(select(models.User).where(models.User.email == body.email))
    if not user or not security.verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong email or password")
    return {"access_token": security.create_token(user.id)}


@app.get("/users/me", response_model=schemas.UserOut)
def me(user: models.User = Depends(current_user)):
    return user


@app.put("/users/me", response_model=schemas.UserOut)
def update_me(
    body: schemas.UserUpdate,
    user: models.User = Depends(current_user),
    db: Session = Depends(get_db),
):
    user.full_name = body.full_name
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Used by the Order service to check that a user exists."""
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user
