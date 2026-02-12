# LogGremlin

A multi-format log generator that sends synthetic logs via OpenTelemetry Protocol (OTLP).

## Features

- Generates multiple log formats:
  - **ELB** (Elastic Load Balancer)
  - **ALB** (Application Load Balancer)
  - **NGINX** access logs
  - **VPC Flow Logs**
- Sends logs via OTLP (OpenTelemetry Protocol)
- Configurable OTEL collector endpoint
- Kubernetes-ready deployment

## Usage

### Docker

Build and run:
```bash
docker build -t kenan435/loggremlin:latest .
docker run -e OTEL_HOST=localhost -e OTEL_PORT=4317 kenan435/loggremlin:latest
```

### Kubernetes

Deploy to your cluster:
```bash
kubectl apply -f loggremlin.yaml
```

## Configuration

Environment variables:
- `OTEL_HOST`: OpenTelemetry collector hostname (default: localhost)
- `OTEL_PORT`: OpenTelemetry collector port (default: 4317)

## OpenTelemetry Integration

Use `otel-values.yaml` to configure the Coralogix OpenTelemetry integration:

```bash
helm upgrade otel-coralogix-integration coralogix/otel-integration -n coralogix -f otel-values.yaml
```

## License

MIT
