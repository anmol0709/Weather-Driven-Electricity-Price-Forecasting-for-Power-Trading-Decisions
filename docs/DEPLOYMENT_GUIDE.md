# Deployment Guide - Electricity Price Forecasting Interface

## 📋 Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

---

## Local Development

### Minimal Setup

```bash
# 1. Navigate to project directory
cd Weather-Driven-Electricity-Price-Forecasting-for-Power-Trading-Decisions

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
streamlit run src/app.py
```

**Access at:** `http://localhost:8501`

### With Custom Port

```bash
streamlit run src/app.py --server.port 8080
```

### Development Mode (with auto-reload)

```bash
streamlit run src/app.py --logger.level=debug
```

---

## Docker Deployment

### Docker Option 1: Using Docker Compose (Recommended)

**Easiest method for quick deployment:**

```bash
# From project root directory
docker-compose -f deployment/docker-compose.yml up --build

# In detached mode (background)
docker-compose -f deployment/docker-compose.yml up -d --build

# Stop the application
docker-compose -f deployment/docker-compose.yml down
```

**Or from deployment directory:**

```bash
cd deployment
docker-compose up --build
cd ..
```

**Access at:** `http://localhost:8501`

### Docker Option 2: Manual Docker Commands

```bash
# Build the image from project root
docker build -f deployment/Dockerfile -t electricity-forecaster .

# Run the container
docker run -p 8501:8501 \
  -v $(pwd):/app \
  --name forecaster \
  electricity-forecaster

# Run in background
docker run -d -p 8501:8501 \
  -v $(pwd):/app \
  --name forecaster \
  electricity-forecaster

# View logs
docker logs forecaster -f

# Stop container
docker stop forecaster

# Remove container
docker rm forecaster
```

### Docker Health Check

```bash
# Check if container is healthy
docker ps --filter "name=forecaster"

# Get detailed container info
docker inspect forecaster
```

---

## Cloud Deployment

### Option 1: Streamlit Cloud (Easiest)

**Steps:**
1. Push your GitHub repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your GitHub repo, branch, and file (`app.py`)
5. Click "Deploy"

**Advantages:**
- Free tier available
- Auto-deploys on git push
- Built-in SSL
- Simple management

**Configuration file `streamlit/config.toml`:**
```toml
[client]
showErrorDetails = false

[server]
runOnSave = true
enableXsrfProtection = true
```

### Option 2: Heroku

1. **Create Heroku account and install CLI**

2. **Create `Procfile`:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

3. **Create `.slugignore`:**
```
.git
.gitignore
__pycache__
*.pyc
.pytest_cache
.DS_Store
```

4. **Deploy:**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: AWS (EC2)

```bash
# Launch EC2 instance (Ubuntu 20.04)
# Then SSH into instance and run:

sudo apt update
sudo apt install python3-pip python3-venv

git clone <your-repo>
cd Weather-Driven-Electricity-Price-Forecasting-for-Power-Trading-Decisions

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with nohup for persistence
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

# Access at: http://<your-ec2-public-ip>:8501
```

### Option 4: Google Cloud Run (Containerized)

```bash
# Install gcloud CLI first

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy electricity-forecaster \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# View deployment
gcloud run services describe electricity-forecaster --region us-central1
```

### Option 5: Azure Container Instances

```bash
# Create resource group
az group create --name forecaster-rg --location eastus

# Create container
az container create \
  --resource-group forecaster-rg \
  --name electricity-forecaster \
  --image acrcustom.azurecr.io/electricity-forecaster:latest \
  --cpu 1 --memory 1.5 \
  --ports 8501 \
  --environment-variables STREAMLIT_SERVER_HEADLESS=true
```

---

## Production Considerations

### 1. Security

```bash
# Use environment variables
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLECORS=false

# Enable authentication (Streamlit Cloud)
# Add to streamlit/config.toml:
```

```toml
[client]
showErrorDetails = false
toolbarMode = "minimal"

[server]
enableXsrfProtection = true
enableCORS = false
headless = true
```

### 2. Load Balancing (with Nginx)

```nginx
upstream streamlit {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    listen 80;
    server_name electricity-forecast.com;

    location / {
        proxy_pass http://streamlit;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 3. Monitoring and Logging

```bash
# Docker container logging
docker logs forecaster --tail 100 --follow

# System resource monitoring
docker stats forecaster

# Application metrics
# Use Streamlit's built-in performance tracking
```

### 4. Performance Optimization

**Increase model cache:**
```python
@st.cache_resource(ttl=24*3600)  # Cache for 24 hours
def load_model_and_scaler():
    # ...
```

**Limit CSV upload size:**
```python
# In app.py, add maximum file size check
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
```

### 5. Backup and Recovery

```bash
# Backup models
cp -r *.joblib ./backups/

# Create Docker image backup
docker image save electricity-forecaster > backup.tar
```

### 6. Scaling Strategies

**Vertical Scaling:**
- Increase CPU/Memory allocation
- Use faster hardware

**Horizontal Scaling:**
- Multiple instances behind load balancer
- Shared model file system (NFS, S3)
- Redis for session management

```python
# Redis caching example
import redis
cache = redis.Redis(host='localhost', port=6379)
```

---

## Performance Tuning

### Streamlit Configuration (`streamlit/config.toml`)

```toml
[client]
# Set to false in production
showErrorDetails = false
showWarningOnDirectExecution = false

[server]
# Performance settings
maxUploadSize = 200
enableXsrfProtection = true

[logger]
level = "info"

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Model Optimization

```python
# For faster predictions, consider:
# 1. Model quantization
# 2. Batch processing
# 3. Async predictions
# 4. GPU acceleration (if available)

# Example: GPU support in Docker
# FROM nvidia/cuda:11.6.2-runtime-ubuntu20.04
```

---

## Troubleshooting Deployment

### Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8080
```

### Out of Memory

```bash
# Monitor Docker memory
docker stats

# Increase limit
docker run -m 4g -p 8501:8501 electricity-forecaster
```

### Slow Response Times

```bash
# Profile application
streamlit run app.py --logger.level=debug

# Check model loading time
import time
start = time.time()
model = joblib.load('lgbm_model.joblib')
print(f"Load time: {time.time() - start}s")
```

### SSL/HTTPS Issues

```bash
# Use Nginx reverse proxy with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com

# Or use cloud provider's built-in SSL
# (AWS ELB, Azure App Service, Google Cloud Run, etc.)
```

---

## Quick Deploy Checklist

- [ ] Models saved (`lgbm_model.joblib`, `scaler.joblib`)
- [ ] Requirements file created (`requirements.txt`)
- [ ] Application tested locally
- [ ] Dockerfile created and tested
- [ ] Environment variables configured
- [ ] Security settings verified
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Domain/URL configured (if applicable)
- [ ] SSL certificate installed (if applicable)

---

## Support & Monitoring URLs

After deployment, access these endpoints:

| Endpoint | Purpose |
|----------|---------|
| `/` | Main application |
| `/_stcore/health` | Health check |
| `/statics/*` | Static files |
| `/_stcore/metrics` | Performance metrics |

---

## Key Deployment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `STREAMLIT_SERVER_PORT` | 8501 | Service port |
| `STREAMLIT_SERVER_ADDRESS` | localhost | Bind address |
| `STREAMLIT_SERVER_HEADLESS` | false | Headless mode |
| `STREAMLIT_CLIENT_LOGGER_LEVEL` | info | Log level |

---

**Last Updated:** March 2026  
**Version:** 1.0
