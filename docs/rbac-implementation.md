# Kubernetes RBAC Implementation

## 1. Overview

Implemented Kubernetes Role-Based Access Control (RBAC) for the Microservices Shop project using Docker Desktop Kubernetes.

The goal is to apply the principle of least privilege by restricting access to Kubernetes resources.

## 2. Namespace

Created a dedicated namespace:

- `microservices-shop`

This separates project resources from the default namespace.

## 3. Service Accounts

Created two Service Accounts:

- `user-service-sa`: Dedicated identity for the User Service. Automatic Service Account token mounting is disabled.
- `developer-sa`: Test identity used to validate developer read-only permissions.

## 4. Role Configuration

Created a namespace-scoped Role named `developer-read-only`.

Allowed resources:
- Pods
- Services
- Deployments
- ReplicaSets

Allowed operations:
- `get`
- `list`
- `watch`

The Role does not grant permission to create, update, patch, or delete these resources.

## 5. RoleBinding

Created `developer-read-only-binding` to connect the `developer-sa` Service Account to the `developer-read-only` Role.

The binding applies only within the `microservices-shop` namespace.

## 6. Validation and Testing

Validated the YAML configurations using Kubernetes server-side dry-run.

Applied the Role and RoleBinding successfully.

Permission tests using `kubectl auth can-i` produced these results:

| Test | Expected | Actual |
|---|---|---|
| List Pods | Yes | Yes |
| List Deployments | Yes | Yes |
| Delete Pods | No | No |
| Create Deployments | No | No |

All four permission tests passed.

## 7. Security Benefits

- Applies least-privilege access.
- Limits developer permissions to read-only operations.
- Uses namespace-scoped access rather than granting cluster-wide permissions.
- Disables automatic API token mounting for the User Service Service Account.

## 8. Remaining Work

- Integrate `user-service-sa` into the actual User Service Kubernetes Deployment when the deployment manifest is available.
- Validate application deployment and runtime behavior.
- Review additional security requirements as the other microservices are integrated.
