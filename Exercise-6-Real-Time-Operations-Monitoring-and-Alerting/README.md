# Exercise 6 - Real-Time Operations Monitoring and Alerting

## Objective

Build a simulated delivery service and monitor its metrics using Prometheus and
Grafana. Jenkins is used to build and start the application and monitoring
containers.

## Technology

- Python
- prometheus_client
- Prometheus
- Grafana
- Jenkins
- Docker

## Files

- `delivery_metrics.py` - Generates simulated delivery metrics every second.
- `prometheus.yml` - Configures Prometheus to scrape the delivery application
  and load alert rules.
- `alert_rules.yml` - Defines the delivery monitoring alerts.
- `Dockerfile` - Builds the Python application Docker image.
- `Jenkinsfile` - Automates Docker image building and starts the application,
  Prometheus, and Grafana.

## Python Application

The application exposes Prometheus metrics on:

`http://localhost:8000/metrics`

The following metrics are generated:

- `total_deliveries`
- `pending_deliveries`
- `on_the_way_deliveries`
- `average_delivery_time`

The application continuously simulates delivery activity every 1 second.

## Run with Docker

Run the following commands from the repository root with Docker running.

### Build the application image

```powershell
$exercise = Join-Path $PWD 'Exercise-6-Real-Time-Operations-Monitoring-and-Alerting'

docker build -t delivery-metrics:exercise-6 $exercise