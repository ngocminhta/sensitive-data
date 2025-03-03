# API Documentation

## Overview
This API provides classification endpoints for determining labels based on input data headers and content. It includes basic classification (`/classify`) and an advanced version (`/classify_advanced`) with additional processing rules.

## Endpoints

### 1. Classify Single Header
**Endpoint:** `POST /classify`

**Description:**
Classifies a single header and returns predicted labels.

**Request Body:**
```json
{
  "header": "<string>"
}
```

**Response:**
```json
{
  "labels": [<label>]
}
```

---

### 2. Classify with Advanced Processing
**Endpoint:** `POST /classify_advanced`

**Description:**
Performs classification based on both header and content. Applies additional rules to refine the predictions.

**Request Body:**
```json
{
  "header": "<string>",
  "content": [
    ["value1", "value2", "value3"],
    ["valueA", "valueB", "valueC"]
  ]
}
```

**Response:**
```json
{
  "labels": [<integer>]
}
```

## Installation & Deployment

### Using Docker
* Build the Docker image:

```sh
docker build -t my-api .
```

* Run the container:

```sh
docker run -e PORT=8000 -p 8000:8000 my-api
```

### Deploying to Kubernetes
* Create a Kubernetes deployment file (`deployment.yaml`):
   
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-api
  template:
    metadata:
      labels:
        app: my-api
    spec:
      containers:
      - name: my-api
        image: my-api:latest
        ports:
        - containerPort: 8000
```

* Apply the deployment:

```sh
kubectl apply -f deployment.yaml
```

* Expose the service:
   
```sh
kubectl expose deployment my-api --type=LoadBalancer --port=8000
```

## Example Usage
### Classify Single Header
```sh
curl -X POST "http://localhost:8000/classify" -H "Content-Type: application/json" -d '{"header": "email"}'
```

### Classify with Advanced Processing
```sh
curl -X POST "http://localhost:8000/classify_advanced" -H "Content-Type: application/json" -d '{"header": "phone_number", "content": [["1234567890", "0987654321"]]}'
```

## License
This project is licensed under the Viettel Information Technology Center license.
