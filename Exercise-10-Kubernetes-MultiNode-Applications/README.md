# Exercise 10 - Kubernetes Multi-Node Applications and ReplicaSets

## Purpose

Deploy two Flask applications to Kubernetes: a Product Catalog with two replicas
and a Shopping Cart with three replicas. Each Deployment manages its ReplicaSet
and Pods. NodePort Services expose both applications.

The product IDs below are `1`, `2`, and `3`, in the order Laptop, Phone, and
Headphones. The exercise request named the products and prices but did not
provide literal ID values; these simple sequential IDs make the API usable.

## Files

| File | Purpose |
| --- | --- |
| `product_catalog.py` | Flask `GET /products` endpoint |
| `shopping_cart.py` | Flask `GET /cart` and `POST /cart` endpoints |
| `Dockerfile.product` | Python 3.9 slim image for Product Catalog |
| `Dockerfile.shopping` | Python 3.9 slim image for Shopping Cart |
| `product_catalog_deployment.yaml` | Two-replica Product Catalog Deployment |
| `shopping_cart_deployment.yaml` | Three-replica Shopping Cart Deployment |
| `product_catalog_service.yaml` | Product Catalog NodePort Service |
| `shopping_cart_service.yaml` | Shopping Cart NodePort Service |
| `screenshots/` | Screenshots captured while completing the exercise |

Both apps listen on `0.0.0.0:80` in their containers. Both Deployments and
Services explicitly use the `default` namespace. The supplied Shopping Cart
manifest mentioned `devops-exercise`, but no such namespace was created and the
service instructions used the default namespace. Using `default` consistently
avoids a namespace mismatch and means no namespace setup is needed.

## Resource and scheduling requirements

The required pod anti-affinity keeps replicas of the *same application* on
different nodes, using `kubernetes.io/hostname` as the topology key. This
reduces the impact of losing one node, but it is a hard scheduling rule:
Shopping Cart needs three schedulable nodes for all three replicas to run;
Product Catalog needs two. The manifests tolerate the standard control-plane
taints so a three-node Minikube cluster can schedule workloads on all three
nodes when necessary. Anti-affinity does not prevent a Product Catalog Pod and
a Shopping Cart Pod from sharing a node.

Each Pod requests `100m` CPU and `128Mi` memory and has limits of `500m` CPU and
`256Mi` memory. The app containers are small, but Kubernetes and the node OS
also need resources. Three Docker-driver Minikube nodes, existing Docker
workloads, and Windows/Docker Desktop overhead can exceed available memory.
Check Docker Desktop's resource allocation before starting the cluster. In the
environment inspected for this exercise, Docker reported about 12 CPUs and
6.7 GiB of memory; the running Jenkins container was using about 1.0 GiB. That
leaves limited headroom for a three-node cluster. Do not start it until
Docker Desktop has enough memory for the nodes plus the existing workloads.

## Build the images

Run these commands in PowerShell from this exercise folder:

```powershell
docker build -f Dockerfile.product -t product-catalog:latest .
docker build -f Dockerfile.shopping -t shopping-cart:latest .
```

## Minikube setup

The Deployment anti-affinity requires at least three schedulable nodes. The
existing `minikube` profile may need additional nodes: inspect it before
changing anything. Starting or changing that profile is a cluster change; do
not run the command until you have reviewed available Docker Desktop resources
and explicitly decided to proceed.

For a fresh or appropriately configured profile, the general multi-node Docker
driver command is:

```powershell
minikube start -p minikube --driver=docker --nodes=3 --cpus=2 --memory=2048
```

Minikube option behavior can vary by version and driver. Check
`minikube start --help` for this installed version and ensure the memory
allocation leaves room for Windows, Docker Desktop, and the already-running
containers. Do not use `minikube stop` or `minikube delete` as a troubleshooting
shortcut. After starting (only when approved), verify:

```powershell
minikube status -p minikube
kubectl get nodes -o wide
```

### Optional Minikube Registry add-on

The registry add-on is optional and is not needed for the image-loading workflow
in this exercise. Enabling it changes the cluster. If you choose to use it,
after the cluster is running, enable and inspect it:

```powershell
minikube addons enable registry -p minikube
kubectl get services -n kube-system
```

To push images to the add-on registry from a separate PowerShell window, first
port-forward to its `registry` Service:

```powershell
kubectl port-forward -n kube-system service/registry 5000:80
```

Keep that command running. In another PowerShell window, tag and push the
images:

```powershell
docker tag product-catalog:latest localhost:5000/product-catalog:latest
docker push localhost:5000/product-catalog:latest
docker tag shopping-cart:latest localhost:5000/shopping-cart:latest
docker push localhost:5000/shopping-cart:latest
```

This pushes to the Minikube registry, not Docker Hub. If Docker Desktop rejects
the registry's HTTP connection, stop here and consult the registry add-on
instructions for this Minikube version rather than changing Docker's security
settings blindly. To deploy registry-backed images, change the image names in
the Deployments to
`registry.kube-system.svc.cluster.local:80/product-catalog:latest` and
`registry.kube-system.svc.cluster.local:80/shopping-cart:latest`, and use a
pull policy such as `IfNotPresent`. The supplied manifests instead use
`imagePullPolicy: Never` and the exact local image tags, so they are intended
for `minikube image load`, not a registry pull.

## Load images into Minikube

`minikube image load` transfers the locally built image into Minikube's
container runtime. It does **not** push the image to Docker Hub or any other
registry. With `imagePullPolicy: Never`, both images must already be present on
the cluster nodes that will run the Pods.

Only after Minikube is running and you have approved cluster changes, load the
images:

```powershell
minikube image load product-catalog:latest -p minikube
minikube image load shopping-cart:latest -p minikube
```

## Deploy the applications

Apply the two Deployments and two Services in the `default` namespace:

```powershell
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml
kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml
```

These commands change the cluster. Run them only after reviewing and approving
the deployment step.

## Verify Deployments, ReplicaSets, Pods, and Services

Wait for each Deployment to become ready, then inspect the resulting objects:

```powershell
kubectl rollout status deployment/product-catalog
kubectl rollout status deployment/shopping-cart
kubectl get deployments,replicasets,pods,services -o wide
kubectl get pods -o wide
```

Expected desired replica counts are **2** for `product-catalog` and **3** for
`shopping-cart`. All five Pods should be Ready and distributed so no two
replicas of the same application share a hostname. If a replica remains
Pending, check node availability, taints, resource capacity, and its scheduling
events:

```powershell
kubectl describe pod <pending-pod-name>
kubectl get events --sort-by=.lastTimestamp
```

## Access the NodePort Services

Ask Minikube for a reachable URL for each service:

```powershell
$productUrl = minikube service product-catalog-service -p minikube --url
$shoppingUrl = minikube service shopping-cart-service -p minikube --url
```

In a separate terminal, keep any required Minikube tunnel or port-forward
process running if Minikube reports that one is needed. Test the APIs:

```powershell
curl.exe "$productUrl/products"
curl.exe "$shoppingUrl/cart"
```

Add an item to the cart; a successful POST returns the updated cart with HTTP
status **201**:

```powershell
$body = '{"product_id":1,"name":"Laptop","price":1200,"quantity":1}'
Invoke-RestMethod -Method Post -Uri "$shoppingUrl/cart" `
  -ContentType 'application/json' -Body $body
curl.exe "$shoppingUrl/cart"
```

The Product Catalog response is a JSON array containing Laptop (1200), Phone
(800), and Headphones (150), with IDs 1, 2, and 3 respectively. The cart API
stores posted JSON objects in process memory. This is intentionally a demo:
each replica has its own independent memory, so load-balanced GET and POST
requests can reach different Pods and show different cart contents. The cart
is neither durable nor shared between replicas; a real application should use
a shared datastore.

## Screenshot checklist

Save screenshots in `screenshots/` showing:

- Minikube status and three-node listing.
- Both Deployments with ready replica counts 2 and 3.
- ReplicaSets and Pods distributed across node hostnames.
- Both NodePort Services.
- `GET /products` output.
- `GET /cart`, a successful `POST /cart`, and the updated cart output.
