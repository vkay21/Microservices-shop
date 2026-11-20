# Kubernetes Network Policy Implementation

## 1. Overview

Implemented and tested Kubernetes Network Policies in the `microservices-shop` namespace using Docker Desktop Kubernetes.

The objective was to control incoming network traffic and demonstrate the principle of least privilege.

## 2. Test Environment

Created three temporary pods:

- `test-server`: Nginx server receiving HTTP requests.
- `test-client`: Authorized client.
- `test-untrusted`: Unauthorized client.

Created a Kubernetes Service named `test-server` to provide a stable endpoint for accessing the Nginx pod.

## 3. Network Policies

### Deny Ingress Policy

File: `test-server-deny-ingress.yaml`

- Selects pods labelled `app=test-server`.
- Applies ingress restrictions.
- Denies all incoming traffic by default.

### Allow Client Policy

File: `test-server-allow-client.yaml`

- Selects pods labelled `app=test-server`.
- Allows incoming traffic from pods labelled `run=test-client`.
- Permits TCP port 80 only.

Both policies apply within the `microservices-shop` namespace.

## 4. Validation and Testing

Both YAML files passed Kubernetes server-side dry-run validation.

The following connectivity tests were performed:

| Test | Expected Result | Actual Result |
|---|---|---|
| Client before policy | HTTP 200 | HTTP 200 |
| Client after deny-ingress policy | Blocked | HTTP 000, timeout |
| Authorized client after allow policy | HTTP 200 | HTTP 200 |
| Unauthorized client | Blocked | HTTP 000, timeout |

All four connectivity tests produced the expected results.

Both the server and authorized client remained running during the tests.

## 5. Security Benefits

- Restricts unnecessary incoming network traffic.
- Allows only explicitly selected clients.
- Limits access to the required application port.
- Demonstrates namespace-scoped network isolation.
- Supports the principle of least privilege.

## 6. Remaining Work

- Integrate appropriate Network Policies with the actual User, Product, and Order Services when their Kubernetes deployments are available.
- Define service-to-service communication requirements.
- Validate policies against the integrated application.
