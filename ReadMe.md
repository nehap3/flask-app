# Flask + MongoDB on Kubernetes (Minikube)

## Project Overview

This project demonstrates how to deploy a Flask application connected to MongoDB on a Kubernetes cluster using Docker, Minikube, and Kubernetes resources such as Deployments, Services, Persistent Volumes, and Horizontal Pod Autoscaling.

The application exposes REST APIs to insert and retrieve data from MongoDB.

---

## Tech Stack

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

## Part 1 – Flask Application Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Flask Application

* `/` → returns welcome message
* `/data` → POST inserts data
* `/data` → GET retrieves stored data

MongoDB connection string:

```
mongodb://mongodb:27017
```

---

## Docker Setup

### Build Image

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

### Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/
```

### Verify Pods

```bash
kubectl get pods
```

---

## MongoDB Configuration

* MongoDB runs as a StatefulSet
* PersistentVolume and PersistentVolumeClaim ensure data persistence
* MongoDB is accessible internally via:

```
mongodb://mongodb:27017
```

---

## Services & Networking

### Flask Service

* Type: NodePort
* Access using:

```bash
minikube service flask-service
```

---

## Horizontal Pod Autoscaling (HPA)

The application automatically scales based on CPU usage.

### HPA Configuration

### HPA Status

```
kubectl get hpa flask-app
```

Example Output:

```
NAME        REFERENCE              TARGETS        MINPODS   MAXPODS   REPLICAS
flask-app   Deployment/flask-app   420m/70%       2         5         2
```

---

## Metrics Verification

```
kubectl top nodes
kubectl top pods -l app=flask-app
```

---

## Testing the Application

### Insert Data

```bash
curl -X POST http://<NODE-IP>:<PORT>/data \
-H "Content-Type: application/json" \
-d '{"name":"Neha","role":"DevOps Intern"}'
```

### Retrieve Data

```bash
curl http://<NODE-IP>:<PORT>/data
```
