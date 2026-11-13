# Testing Strategy

## 1. Purpose

The purpose of this testing strategy is to ensure that the microservices application works correctly, individual components perform as expected, and services communicate reliably.

Testing will be performed throughout development to identify defects early and improve application reliability.

## 2. Testing Types

### 2.1 Unit Testing (Planned)

Unit testing verifies individual functions and components independently.

Examples:
- Password hashing and verification.
- Input validation.
- Authentication token generation and validation.

Tool: pytest

### 2.2 Integration Testing

Integration testing verifies that different application components work together correctly.

Examples:
- API endpoints interacting with the database.
- User registration storing user information.
- Login retrieving user information and generating authentication tokens.

Tool: pytest and FastAPI TestClient.

### 2.3 End-to-End Testing

End-to-end testing verifies complete application workflows from beginning to end.

Example:
1. Register a new user.
2. Log in using the registered credentials.
3. Access the authenticated user profile.
4. Verify that the expected information is returned.

Tool: pytest and HTTPX.

## 3. Existing User Service Tests

The User Service currently contains seven automated test functions:

| Test Function | Purpose |
|---|---|
| test_health | Verifies service health |
| test_register_and_duplicate | Verifies successful registration and duplicate email handling |
| test_login_and_me | Verifies authentication and profile access |
| test_wrong_password | Verifies incorrect credentials are rejected |
| test_bad_token | Verifies invalid authentication tokens are rejected |
| test_get_user_by_id | Verifies existing and missing user handling |
| test_metrics_exposed | Verifies Prometheus metrics are exposed |

These tests primarily validate API behavior and interactions with the test database.

Separate unit tests and complete end-to-end tests are planned improvements.

## 4. Test Environment

- Programming language: Python
- Application framework: FastAPI
- Testing framework: pytest
- API testing: FastAPI TestClient and HTTPX
- Test database: SQLite
- Application database: PostgreSQL is supported through SQLAlchemy.

## 5. Continuous Integration

GitHub Actions will be used to automate testing whenever changes are pushed to the repository or a pull request is created.

The planned workflow will:
1. Check out the repository.
2. Set up Python.
3. Install application and development dependencies.
4. Execute automated tests.
5. Report whether the tests passed or failed.

## 6. Future Testing Improvements

As additional microservices are developed, the testing strategy will be expanded to include:
- Tests for each additional service.
- Cross-service integration testing.
- Complete application workflow testing.
- Automated test execution through GitHub Actions.

## 7. Conclusion

This testing strategy establishes a foundation for validating the reliability and functionality of the microservices application. Automated testing and continuous integration will help identify issues early and support consistent project delivery.
