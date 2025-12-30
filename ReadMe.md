```markdown
# Flask + MongoDB on Kubernetes (Minikube)

## Project Overview

This project demonstrates how to deploy a Flask application connected to MongoDB on a Kubernetes cluster using Docker, Minikube, and Kubernetes resources such as Deployments, Services, Persistent Volumes, and Horizontal Pod Autoscaling.

The application exposes REST APIs to insert and retrieve data from MongoDB.

---

## Tech Stack

- Python (Flask)
- MongoDB
- Docker
- Kubernetes (Minikube)
- Docker Hub
- Argo CD (for GitOps – optional)

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

```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Flask Application (app.py)

- `/` → returns welcome message
- `/data` → POST inserts data into MongoDB
- `/data` → GET retrieves stored data

MongoDB connection uses:

```
mongodb://mongodb:27017
```

---

## Docker Setup

### Build Image

```
docker build -t <docker-username>/flask-mongo-app .
```

### Push to DockerHub

```
docker push <docker-username>/flask-mongo-app
```

---

## Kubernetes Setup

### 1. Start Minikube

```
minikube start
```

### 2. Apply Kubernetes Manifests

```
kubectl apply -f k8s/
```

### 3. Verify Pods

```
kubectl get pods
```

---

## MongoDB Configuration

- MongoDB runs as a StatefulSet
- Data stored using PersistentVolume & PersistentVolumeClaim
- Authentication enabled using Kubernetes Secrets
- MongoDB accessible inside cluster via: `mongodb://mongodb:27017`

---

## Services & Networking

### Flask Service

- Type: NodePort
- Accessible via: `minikube service flask-service`

---

## Horizontal Pod Autoscaling (HPA)

HPA monitors Flask app CPU and scales 2→5 pods automatically at 70% CPU threshold.

### HPA Configuration

```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Current Status (Working)

```
$ kubectl get hpa flask-app
NAME        REFERENCE                  TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
flask-app   Deployment/flask-app     <420m>/70%   2         5         2          15m
```

### Metrics Server Status

```
$ kubectl top nodes
NAME       CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)
minikube   397m         3%       1075Mi          28%

$ kubectl top pods -l app=flask-app
NAME                    CPU(cores)   MEMORY(bytes)
flask-app-xxxx         180m         25Mi
flask-app-yyyy         0m           10Mi
```

### Scale Test Commands

```
# 1. Generate CPU Load
kubectl scale deployment flask-app --replicas=2
for i in {1..50}; do curl http://127.0.0.1:<NODEPORT>/; done

# 2. Watch Auto-Scaling
kubectl get hpa flask-app -w
# REPLICAS: 2 → 5 (30 seconds)

# 3. Verify Scaled Pods
kubectl get pods -l app=flask-app
```

### Required Screenshots

1. `kubectl get hpa flask-app` → Shows 2/5 replicas
2. `kubectl top nodes` → Metrics working
3. `kubectl top pods -l app=flask-app` → CPU utilization visible
4. `minikube service flask-service` → NodePort URL

---

## Testing the Application

### Insert Data

```
curl -X POST http://<NODE-IP>:<PORT>/data \
-H "Content-Type: application/json" \
-d '{"name":"Neha","role":"DevOps Intern"}'
```

### Retrieve Data

```
curl http://<NODE-IP>:<PORT>/data
```

---

**HPA working, Metrics Server live, Auto-scaling ready.** [attached_file:1]

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/84229273/7c044fd6-874f-49ac-9a41-20dc3732868a/paste.txt)
