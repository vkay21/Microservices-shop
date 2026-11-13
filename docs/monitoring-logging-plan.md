# Monitoring and Centralized Logging Plan

## 1. Purpose

The purpose of monitoring and centralized logging is to track
microservices performance, identify errors, and simplify troubleshooting.

## 2. Selected Tools

| Tool | Responsibility |
|---|---|
| Prometheus | Collect application metrics |
| Grafana | Visualize metrics and logs through dashboards |
| Loki | Store and query centralized application logs |
| Grafana Alloy | Collect container logs and forward them to Loki |

## 3. Proposed Architecture

1. Microservices expose application metrics.
2. Prometheus collects metrics from the services.
3. Application containers produce logs.
4. Grafana Alloy collects and forwards logs to Loki.
5. Grafana displays metrics from Prometheus and logs from Loki.

## 4. Current Project Status

- User Service exposes a Prometheus metrics endpoint at /metrics.
- User Service currently runs through Docker Compose.
- PostgreSQL is used as the User Service database.
- Product and Order services are planned additions.

## 5. Monitoring Requirements

We plan to monitor:

- HTTP request count.
- Request duration.
- Application error rates.
- Service availability.
- Container health and resource usage.

## 6. Logging Requirements

We plan to:

- Collect application logs from containers.
- Centralize logs using Loki.
- View and search logs through Grafana.
- Use logs to investigate application errors.
- Avoid logging passwords, tokens, and other sensitive information.

## 7. Implementation Plan

- Week 1: Document the monitoring and logging architecture.
- Week 2: Prepare monitoring configuration and review logging requirements.
- Week 3: Deploy Prometheus, Grafana, and centralized logging with Kubernetes.
- Week 4: Validate dashboards, logs, and monitoring during final integration.

## 8. Conclusion

Prometheus, Grafana, Loki, and Grafana Alloy will provide
a foundation for monitoring application performance and
centralizing logs across the microservices project.
