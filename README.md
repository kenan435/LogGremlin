# LogGremlin

A multi-format log generator that sends synthetic logs via OpenTelemetry Protocol (OTLP).

[![CI/CD](https://github.com/kenan435/LogGremlin/actions/workflows/deploy.yaml/badge.svg)](https://github.com/kenan435/LogGremlin/actions)

## 🚀 GitOps with ArgoCD

This project uses **ArgoCD** for continuous deployment to Kubernetes.

### Architecture

```
Developer Push → GitHub → GitHub Actions → Docker Hub
                              ↓
                         ArgoCD watches repo
                              ↓
                    Auto-syncs to Kubernetes
```

### How It Works

1. **Push code** to `main` branch
2. **GitHub Actions** builds and pushes Docker image to Docker Hub
3. **ArgoCD** detects changes in the Git repo
4. **ArgoCD** automatically syncs the deployment to the cluster

### ArgoCD Dashboard

- **URL**: http://a4f1503041a3d4ac1a1edf015973612a-1744544696.eu-north-1.elb.amazonaws.com
- **Username**: `admin`
- **Password**: `XwzjyhsYDUzuMw5V`

### Manual Sync (Optional)

ArgoCD is configured for **automatic sync**, but you can manually sync if needed:

```bash
kubectl get application loggremlin -n argocd
```

## 📁 Project Structure

```
LogGremlin/
├── k8s/                    # Kubernetes manifests (managed by ArgoCD)
│   └── deployment.yaml
├── loggremlin.py          # Log generator application
├── dockerfile             # Docker image definition
├── argocd-application.yaml # ArgoCD Application manifest
└── .github/workflows/     # CI/CD pipeline
    └── deploy.yaml
```

## 🔧 Deployment

The deployment is fully automated via GitOps. Any changes to `k8s/` manifests will trigger ArgoCD to sync.

### Key Features

- ✅ **Automated Sync**: Changes auto-deploy within seconds
- ✅ **Self-Healing**: ArgoCD reverts manual cluster changes
- ✅ **Prune**: Removes resources deleted from Git
- ✅ **Retry Logic**: Auto-retries failed syncs

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
