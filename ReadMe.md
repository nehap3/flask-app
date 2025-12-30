

# Flask + MongoDB on Kubernetes (Minikube)

## Project Overview

This project demonstrates how to deploy a **Flask application connected to MongoDB** on a **Kubernetes cluster** using **Docker**, **Minikube**, and **Kubernetes resources** such as Deployments, Services, Persistent Volumes, and Horizontal Pod Autoscaling.

The application exposes REST APIs to insert and retrieve data from MongoDB.

---

## Tech Stack

* Python (Flask)
* MongoDB
* Docker
* Kubernetes (Minikube)
* Docker Hub
* Argo CD (for GitOps – optional)

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

### 3. Flask Application (`app.py`)

* `/` → returns welcome message
* `/data` → POST inserts data into MongoDB
* `/data` → GET retrieves stored data

MongoDB connection uses:

```python
mongodb://mongodb:27017
```

---

## Docker Setup

### Build Image

```bash
docker build -t <docker-username>/flask-mongo-app .
```

### Push to DockerHub

```bash
docker push <docker-username>/flask-mongo-app
```

---

## Kubernetes Setup

### 1. Start Minikube

```bash
minikube start
```

### 2. Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/
```

### 3. Verify Pods

```bash
kubectl get pods
```

---

## MongoDB Configuration

* MongoDB runs as a **StatefulSet**
* Data stored using **PersistentVolume & PersistentVolumeClaim**
* Authentication enabled using Kubernetes **Secrets**
* MongoDB accessible inside cluster via:

```
mongodb://mongodb:27017
```

---

## Services & Networking

### Flask Service

* Type: NodePort
* Accessible via:

```bash
minikube service flask-service
```

## DNS Resolution in Kubernetes

Kubernetes uses **CoreDNS** for service discovery.

Example:

```
mongodb.default.svc.cluster.local
```

Inside the cluster, the Flask app connects using:

```
mongodb://mongodb:27017
```

This allows seamless communication without hardcoding IPs.

---



This ensures stability and prevents resource starvation.

---

## 🧪 Testing the Application

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

---

## What This Project Demonstrates

✔ Flask + MongoDB integration
✔ Kubernetes Deployment & Services
✔ StatefulSet with Persistent Volume
✔ Docker Image Creation
✔ Kubernetes DNS & Networking
✔ Production-ready architecture

---

## Final Notes

This project fulfills all requirements of the internship assignment including:

* Application deployment
* Containerization
* Kubernetes orchestration
* Persistent storage
* Scaling
* DNS resolution

---
