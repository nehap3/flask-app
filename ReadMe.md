# Flask + MongoDB on Kubernetes

## Project Overview

This project demonstrates how to deploy a Flask application connected to MongoDB on a Kubernetes cluster using Docker, Minikube, and Kubernetes resources such as Deployments, Services, Persistent Volumes, and Horizontal Pod Autoscaling.

The application exposes REST APIs to insert and retrieve data from MongoDB.

---

## Technology Stack

* Python (Flask)
* MongoDB
* Docker
* Kubernetes (Minikube)
* Docker Hub
* Argo CD (optional)

---

## Project Structure

```
flask-mongo-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── k8s/
│   ├── flask-deployment.yaml
│   ├── flask-service.yaml
│   ├── mongo-statefulset.yaml
│   ├── mongo-service.yaml
│   ├── mongo-pv.yaml
│   ├── mongo-secret.yaml
│   └── hpa.yaml
└── README.md
```

---

## Part 1: Flask Application Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Flask Application Details

Endpoints:

* `/` → Returns welcome message with timestamp
* `/data` →

  * POST: Insert data into MongoDB
  * GET: Retrieve stored data

MongoDB connection string used:

```
mongodb://mongodb:27017
```

---

## Docker Setup

### Build Docker Image

```bash
docker build -t <docker-username>/flask-mongo-app .
```

### Push Image to Docker Hub

```bash
docker push <docker-username>/flask-mongo-app
```

---

## Kubernetes Setup

### Start Minikube

```bash
minikube start
```

### Deploy Kubernetes Resources

```bash
kubectl apply -f k8s/
```

### Verify Deployment

```bash
kubectl get pods
```

---

## MongoDB Configuration

* MongoDB runs as a StatefulSet
* PersistentVolume and PersistentVolumeClaim ensure data persistence
* Authentication handled via Kubernetes Secrets
* Accessible inside cluster at:

```
mongodb://mongodb:27017
```

---

## Service Configuration

* Flask Service type: NodePort
* Application accessible using:

```bash
minikube service flask-service
```

---

## Horizontal Pod Autoscaler (HPA)

HPA automatically scales the Flask application based on CPU usage.

### HPA Configuration
```bash
kubectl get hpa
```

---

## Testing the Application

### Insert Data

```bash
curl -X POST http://<NODE-IP>:<PORT>/data \
-H "Content-Type: application/json" \
-d '{"name":"Neha","role":"DevOps Intern"}'
```

### Fetch Data

```bash
curl http://<NODE-IP>:<PORT>/data
```
