# Microservices Architecture and API Contracts

## 1. Project Overview

Microservices Shop is a microservices-based application.
The User Service is currently implemented using FastAPI
and PostgreSQL.

Product and Order services are planned additions.

## 2. Current User Service Architecture

- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Request validation: Pydantic
- Authentication: JWT Bearer tokens
- Password security: bcrypt
- Metrics: Prometheus FastAPI Instrumentator
- Containerization: Docker

## 3. User Service API Endpoints

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| GET | /health | Check application and database health | Not required |
| POST | /users/register | Register a new user | Not required |
| POST | /users/login | Authenticate a user | Not required |
| GET | /users/me | Retrieve logged-in user profile | Required |
| PUT | /users/me | Update logged-in user profile | Required |
| GET | /users/{user_id} | Retrieve user by ID; intended for Order Service lookup | Not required in current implementation |
| GET | /metrics | Expose Prometheus metrics | Not required in current implementation |

## 4. API Request Schemas

### UserCreate
- email: Valid email address
- full_name: Required, 1 to 255 characters
- password: Required, 6 to 72 characters

### UserLogin
- email: Valid email address
- password: User password

### UserUpdate
- full_name: Required, 1 to 255 characters

## 5. API Response Schemas

### UserOut
- id: User identifier
- email: User email address
- full_name: User full name
- created_at: Account creation timestamp

Password information is not included in the UserOut response.

### Token
- access_token: JWT access token
- token_type: Bearer

## 6. Authentication and Security

- Passwords are hashed using bcrypt.
- JWT Bearer tokens protect the current-user endpoints.
- Invalid or expired tokens return HTTP 401.
- Duplicate registration emails return HTTP 409.
- User responses exclude password hashes.

Security improvement identified:
The GET /users/{user_id} endpoint currently has no
authentication dependency. Service-to-service authentication
should be reviewed before relying on this endpoint for
Order Service communication.

## 7. Monitoring

- The User Service exposes a /metrics endpoint.
- Prometheus can scrape metrics from the service.
- Grafana is planned for monitoring dashboards.

## 8. Database

The User Service uses SQLAlchemy to communicate with
its PostgreSQL database.

The application checks database connectivity through
the /health endpoint.

## 9. Future Architecture Work

- Implement Product Service.
- Implement Order Service.
- Define service-to-service API contracts.
- Document service communication.
- Review service authentication and authorization.
- Update architecture diagrams as services are added.

## 10. Current Limitations

This document describes the implemented User Service
and planned architecture. Product and Order service
implementation details are not yet confirmed.
