\# Exercise 2 – Minikube, Kubectl and Flask



\## Objective



Deploy a Python Flask application on Minikube using Docker, Kubernetes Deployment and NodePort Service.



\## Files



\- `app.py` – Flask application

\- `Dockerfile` – Docker image configuration

\- `flask-deployment.yaml` – Kubernetes Deployment and Service configuration

\- `screenshots/` – Practical execution screenshots



\## Deployment



The Flask application runs on port `15000`.



A Docker image named `flask-app:latest` was built and loaded into Minikube.



The Kubernetes Deployment runs one replica of the Flask application.



A NodePort Service named `flask-app-service` exposes the application.



\## Verification



Pod status:



```text

1/1 Running

