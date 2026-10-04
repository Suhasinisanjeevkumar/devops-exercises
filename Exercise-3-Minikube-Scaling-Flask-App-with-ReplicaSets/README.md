# Exercise 3 – Minikube Scaling Flask App with ReplicaSets

## Objective

To understand ReplicaSets and Pods, scale a Flask application, and observe pod distribution on a single Minikube node.

## Application

The Flask application simulates a flash-sale e-commerce application.

Endpoints:
- `/` – Welcome message with Pod hostname and timestamp
- `/buy` – Simulates a purchase and shows which Pod served the request
- `/health` – Health check endpoint

## Files

- `app.py` – Flask application
- `Dockerfile` – Container image definition
- `flashsale-replicaset.yaml` – ReplicaSet and ClusterIP Service configuration

## Steps Performed

### 1. Build Docker Image

```bash
docker build -t flashsale:1.0 .