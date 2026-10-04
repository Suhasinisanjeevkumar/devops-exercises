## \# Exercise 4 - Docker Networking

## 

## \## Objective

## 

## Understand Docker networking concepts and configure a multi-container application using a custom Docker bridge network.

## 

## \## Scenario

## 

## The application consists of three containers:

## 

## \- Flask web server

## \- MySQL database

## \- Redis cache

## 

## All three containers are connected through the custom Docker bridge network `my-bridge-net`.

## 

## \## Files

## 

## \- `app.py` - Flask REST API

## \- `Dockerfile` - Docker image configuration

## \- `requirements.txt` - Python dependencies

## \- `screenshots/` - Execution and verification screenshots

## 

## \## Docker Network

## 

## Created a custom bridge network:

## 

## ```bash

## docker network create --driver bridge my-bridge-net

