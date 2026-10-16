# 🚀 SpamShield Deployment Guide

## Quick Start with Docker Compose

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start Services
```bash
docker-compose up -d
```

This starts:
- PostgreSQL database on port 5432
- Redis cache on port 6379
- FastAPI application on port 8000
- Prometheus monitoring on port 9090
- Grafana dashboard on port 3000

### 3. Initialize Database
```bash
docker-compose exec api python -c "from database import init_db; init_db()"
```

### 4. Access Services
```
API Documentation:  http://localhost:8000/api/docs
Prometheus:         http://localhost:9090
Grafana:            http://localhost:3000 (admin/admin)
```

---

## Production Deployment with Kubernetes

### Prerequisites
- Kubernetes cluster (AWS EKS, GCP GKE, Azure AKS, or local)
- kubectl installed
- Helm 3+

### 1. Create Namespace
```bash
kubectl create namespace spamshield
```

### 2. Create Secrets
```bash
kubectl create secret generic spamshield-secrets \
  --from-literal=database-url=postgresql://user:pass@postgres/spamshield \
  --from-literal=secret-key=your-secret-key \
  -n spamshield
```

### 3. Deploy Database
```bash
kubectl apply -f k8s/postgres-deployment.yaml -n spamshield
kubectl apply -f k8s/redis-deployment.yaml -n spamshield
```

### 4. Deploy Application
```bash
kubectl apply -f k8s/api-deployment.yaml -n spamshield
kubectl apply -f k8s/api-service.yaml -n spamshield
```

### 5. Setup Ingress
```bash
kubectl apply -f k8s/ingress.yaml -n spamshield
```

### 6. Check Status
```bash
kubectl get pods -n spamshield
kubectl get svc -n spamshield
kubectl logs -f deployment/spamshield-api -n spamshield
```

---

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup PostgreSQL
```bash
# On macOS
brew install postgresql
brew services start postgresql

# On Linux
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start

# Create database
psql -U postgres
CREATE DATABASE spamshield;
\q
```

### 3. Configure Environment
```bash
cp .env.example .env
```

### 4. Run Application
```bash
# Terminal 1: Start FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Train BERT model (optional)
python train_bert_model.py
```

### 5. Access API
```
http://localhost:8000/api/docs
```

---

## CI/CD Pipeline Setup (GitHub Actions)

### 1. Add Secrets to Repository
```
Settings → Secrets and variables → Actions
```

Add these secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password
- `KUBERNETES_CONFIG`: Base64 encoded kubeconfig

### 2. Workflow File
Place `.github/workflows/ci-cd.yml` in repository

### 3. On Every Push
- Tests run
- Linting checks
- Security scans
- Docker image built and pushed
- Automatic deployment to production (on main branch)

---

## Monitoring & Logging

### Prometheus Metrics
```
http://localhost:9090
```

Tracks:
- Request counts
- Response times
- Model inference latency
- Database connection pool
- Error rates

### Grafana Dashboards
```
http://localhost:3000
```

Pre-configured dashboards:
- API Performance
- Model Accuracy Tracking
- User Activity
- System Health

### Logs
```bash
# Docker
docker-compose logs -f api

# Kubernetes
kubectl logs -f deployment/spamshield-api -n spamshield

# File-based
tail -f logs/spamshield.log
```

---

## Model Updates

### Retrain BERT Model
```bash
# Local
python train_bert_model.py

# Docker
docker-compose exec api python train_bert_model.py

# Kubernetes
kubectl exec deployment/spamshield-api -n spamshield -- python train_bert_model.py
```

### A/B Testing New Models
```bash
# API endpoint to trigger A/B test
POST /api/v1/admin/ab-test
{
    "model_a": "bert_v1",
    "model_b": "bert_v2",
    "traffic_split": 0.5
}
```

---

## Scaling

### Horizontal Scaling (Docker Compose)
```yaml
# docker-compose.yml
api:
  deploy:
    replicas: 3
```

### Horizontal Scaling (Kubernetes)
```bash
kubectl scale deployment spamshield-api --replicas=5 -n spamshield
kubectl autoscale deployment spamshield-api --min=2 --max=10 -n spamshield
```

---

## Health Checks

### API Health
```bash
curl http://localhost:8000/health
```

Response:
```json
{
    "status": "healthy",
    "service": "SpamShield API",
    "version": "2.0.0",
    "models_loaded": true
}
```

### Database Connection
```bash
curl http://localhost:8000/api/v1/admin/dashboard \
  -H "Authorization: Bearer <token>"
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
docker-compose exec postgres psql -U spamshield -d spamshield -c "SELECT 1"

# Check environment variables
docker-compose exec api env | grep DATABASE
```

### Model Loading Issues
```bash
# Check if models exist
docker-compose exec api ls -la models/

# Verify BERT model
docker-compose exec api python -c "from inference import get_detector; print(get_detector())"
```

### Memory Issues
```bash
# Increase Docker memory
docker-compose exec api free -h

# Update docker-compose.yml
api:
  mem_limit: 4g
  memswap_limit: 4g
```

---

## Security Best Practices

1. **Use HTTPS** in production
2. **Rotate secrets** regularly
3. **Enable CORS** only for trusted domains
4. **Rate limiting** on API endpoints
5. **API key rotation** for integrations
6. **Database backups** daily
7. **Monitor logs** for suspicious activity
8. **Keep dependencies** updated
