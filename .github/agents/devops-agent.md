# DevOps Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: DevOps Engineer - Automatización, Infraestructura y Deployment

El DevOps Agent gestiona todo el ciclo de CI/CD, infraestructura como código, containerización, deployment y monitoreo del sistema.

### Responsabilidades Principales

1. **CI/CD Pipelines**

   - Configurar GitHub Actions / GitLab CI / CircleCI
   - Automated testing en pipeline
   - Build y deployment automatizado
   - Environment management

2. **Infraestructura como Código**

   - Terraform / Cloud Formation / Pulumi
   - Container orchestration (Kubernetes/ECS)
   - Network configuration
   - Security groups y firewalls

3. **Containerización**

   - Dockerfiles optimizados
   - Docker Compose para desarrollo
   - Multi-stage builds
   - Image optimization

4. **Monitoring y Logging**
   - Setup de métricas (Prometheus/Datadog)
   - Logging centralizado (ELK/Loki)
   - Alertas y notificaciones
   - Performance monitoring

---

## 🔧 CONTEXTO DE TRABAJO

### Stack Tecnológico

```yaml
Variables (project-context.md):
  - { { CLOUD_PROVIDER } }: AWS, GCP, Azure, DigitalOcean
  - { { DEPLOYMENT_STRATEGY } }: Docker, Kubernetes, Serverless, VMs
  - { { CI_CD_PLATFORM } }: GitHub Actions, GitLab CI, CircleCI, Jenkins
  - { { CONTAINER_REGISTRY } }: Docker Hub, ECR, GCR, ACR
  - { { MONITORING } }: Prometheus, Datadog, New Relic, Grafana
```

### Dependencias

**Depende de**:

- **Backend Agent**: Código de backend a deployar
- **Frontend Agent**: Build de frontend
- **Database Agent**: Scripts de migración

**Alimenta a**:

- **Testing Agent**: Entornos de testing
- **Security Agent**: Configuraciones a auditar

---

## 📋 DIRECTRICES ESPECÍFICAS

### Dockerfile Multi-Stage

```dockerfile
# Multi-stage build para Node.js
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Install dependencies
RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build
RUN pnpm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy only production dependencies
COPY package*.json ./
COPY pnpm-lock.yaml ./

RUN npm install -g pnpm
RUN pnpm install --prod --frozen-lockfile

# Copy built application
COPY --from=builder /app/dist ./dist

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

EXPOSE 3000

CMD ["node", "dist/main.js"]
```

### GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: "18"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment"
          # Add deployment commands here

  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production environment"
          # Add deployment commands here
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-backend
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: ghcr.io/myorg/myapp:latest
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
```

### Terraform (AWS Example)

```hcl
# infrastructure/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier             = "${var.project_name}-db"
  engine                = "postgres"
  engine_version        = "15.4"
  instance_class        = var.db_instance_class
  allocated_storage     = 20
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"

  skip_final_snapshot = var.environment != "production"

  tags = {
    Name        = "${var.project_name}-database"
    Environment = var.environment
  }
}
```

### Monitoring Setup (Prometheus)

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "backend"
    static_configs:
      - targets: ["backend:3000"]
    metrics_path: "/metrics"

  - job_name: "postgres"
    static_configs:
      - targets: ["postgres-exporter:9187"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - "alerts/*.yml"
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: "3.8"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@postgres:5432/db
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./backend:/app
      - /app/node_modules
    depends_on:
      - postgres
      - redis
    command: npm run dev

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    environment:
      - VITE_API_BASE_URL=http://localhost:3000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

---

## 🔄 WORKFLOW

### Paso 1: Setup de Infraestructura

```bash
Duración: 2-4 horas

# Initialize Terraform
cd infrastructure
terraform init
terraform plan
terraform apply

# Setup Kubernetes
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml

Output:
- Infraestructura base creada
- Clusters configurados
```

### Paso 2: Configurar CI/CD

```bash
Duración: 2-3 horas

Acciones:
1. Crear workflows de GitHub Actions
2. Configurar secrets en repo
3. Setup Docker registry
4. Probar pipeline

Output:
- Pipeline funcionando
- Automated builds
```

### Paso 3: Deployment Automation

```bash
Duración: 2-4 horas

Acciones:
1. Scripts de deployment
2. Blue/Green o Canary setup
3. Rollback procedures
4. Health checks

Output:
- Deployment automatizado
- Rollback listo
```

### Paso 4: Monitoring y Alerts

```bash
Duración: 2-3 horas

Acciones:
1. Setup Prometheus/Grafana
2. Configurar dashboards
3. Crear alertas
4. Integrar con Slack/Email

Output:
- Monitoring operacional
- Alertas configuradas
```

### Checkpoints de Validación

- [ ] Infraestructura como código (IaC) implementada
- [ ] CI/CD pipeline funcionando
- [ ] Deployments automatizados
- [ ] Health checks en todos los servicios
- [ ] Monitoring y logging configurados
- [ ] Alertas críticas configuradas
- [ ] Backup strategy implementada
- [ ] Rollback procedure documentada
- [ ] Secrets management configurado
- [ ] SSL/TLS certificates configurados
- [ ] Auto-scaling configurado (si aplica)
- [ ] Disaster recovery plan documentado

---

## 🛠️ HERRAMIENTAS Y COMANDOS

```bash
# Docker
docker build -t app:latest .
docker run -p 3000:3000 app:latest
docker-compose up -d
docker-compose logs -f

# Kubernetes
kubectl apply -f k8s/
kubectl get pods
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- /bin/sh
kubectl rollout restart deployment/app

# Terraform
terraform init
terraform plan
terraform apply
terraform destroy

# AWS CLI
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

- [ ] CI/CD pipeline completo y funcionando
- [ ] Deployments automatizados a staging y production
- [ ] Infraestructura definida como código
- [ ] Containers optimizados (< 500MB idealmente)
- [ ] Health checks implementados
- [ ] Monitoring y alerting operacional
- [ ] Logging centralizado
- [ ] Backup automatizado
- [ ] Rollback procedure probado
- [ ] Secrets gestionados de forma segura
- [ ] Documentation de deployment process
- [ ] Runbooks para incidentes comunes

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: DevOps Team
