# Notebook Custom Image

## Overview

This demo demonstrates how to create and use custom Docker images for Kubeflow Notebook servers. You'll learn how to build images with specific Python packages, system dependencies, and configurations tailored to your machine learning workflows.

Custom images are essential when you need libraries or tools not available in standard Kubeflow notebook images, such as specific ML frameworks, data processing tools, or domain-specific packages.

## Prerequisites

Before starting this demo, ensure you have:

- A running Kubernetes cluster with Kubeflow (v1.7+) installed
- Docker installed locally or access to a container build service
- Access to a container registry (Docker Hub, GCR, ECR, or private registry)
- kubectl configured with access to your cluster
- Basic understanding of Docker and Dockerfile syntax
- Familiarity with Python package management

## Architecture

### Custom Image Workflow

```
┌──────────────────────────────────────────────────────────┐
│                  Development Workflow                     │
│                                                           │
│  1. Define Requirements                                   │
│     ┌────────────────────────────────┐                   │
│     │  • Python packages             │                   │
│     │  • System dependencies         │                   │
│     │  • Configuration files         │                   │
│     │  • Jupyter extensions          │                   │
│     └────────────────────────────────┘                   │
│                      │                                    │
│                      ▼                                    │
│  2. Create Dockerfile                                     │
│     ┌────────────────────────────────┐                   │
│     │  FROM base-notebook:latest     │                   │
│     │  RUN pip install ...           │                   │
│     │  COPY requirements.txt ...     │                   │
│     └────────────────────────────────┘                   │
│                      │                                    │
│                      ▼                                    │
│  3. Build & Test Image                                    │
│     ┌────────────────────────────────┐                   │
│     │  docker build -t myimage:v1    │                   │
│     │  docker run --rm myimage:v1    │                   │
│     └────────────────────────────────┘                   │
│                      │                                    │
│                      ▼                                    │
│  4. Push to Registry                                      │
│     ┌────────────────────────────────┐                   │
│     │  docker push myregistry/       │                   │
│     │    myimage:v1                  │                   │
│     └────────────────────────────────┘                   │
│                      │                                    │
│                      ▼                                    │
│  5. Deploy in Kubeflow                                    │
│     ┌────────────────────────────────┐                   │
│     │  Notebook CRD with custom      │                   │
│     │  image: myregistry/myimage:v1  │                   │
│     └────────────────────────────────┘                   │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Image Layers

```
┌─────────────────────────────────────────┐
│   Your Custom Packages & Config        │ ← Your additions
├─────────────────────────────────────────┤
│   Kubeflow Notebook Extensions          │ ← Kubeflow layer
├─────────────────────────────────────────┤
│   Jupyter & Python Base                 │ ← Base layer
├─────────────────────────────────────────┤
│   Ubuntu / Operating System             │ ← OS layer
└─────────────────────────────────────────┘
```

## Step-by-Step Guide

### Step 1: Prepare Custom Requirements

Create a requirements file with your needed packages:

```bash
# View the requirements file
cat code/requirements.txt

# Expected contents:
# - ML frameworks (TensorFlow, PyTorch, etc.)
# - Data processing libraries
# - Custom packages
```

### Step 2: Build Custom Image

Build the Docker image locally:

```bash
# Navigate to the code directory
cd code/

# Build the image
docker build -t my-kubeflow-notebook:v1.0 -f Dockerfile .

# Verify the image was created
docker images | grep my-kubeflow-notebook
```

### Step 3: Test Image Locally (Optional)

Test the image before deploying to Kubeflow:

```bash
# Run the container locally
docker run --rm -p 8888:8888 \
  my-kubeflow-notebook:v1.0

# Access Jupyter at http://localhost:8888
# Test your custom packages are available
```

### Step 4: Push to Container Registry

Tag and push the image to your registry:

```bash
# For Docker Hub
docker tag my-kubeflow-notebook:v1.0 yourusername/my-kubeflow-notebook:v1.0
docker login
docker push yourusername/my-kubeflow-notebook:v1.0

# For Google Container Registry (GCR)
docker tag my-kubeflow-notebook:v1.0 gcr.io/your-project/my-kubeflow-notebook:v1.0
docker push gcr.io/your-project/my-kubeflow-notebook:v1.0

# For Amazon ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-west-2.amazonaws.com
docker tag my-kubeflow-notebook:v1.0 your-account.dkr.ecr.us-west-2.amazonaws.com/my-kubeflow-notebook:v1.0
docker push your-account.dkr.ecr.us-west-2.amazonaws.com/my-kubeflow-notebook:v1.0
```

### Step 5: Create Image Pull Secret (if using private registry)

If your registry requires authentication:

```bash
# Create a docker-registry secret
kubectl create secret docker-registry regcred \
  --docker-server=your-registry.com \
  --docker-username=your-username \
  --docker-password=your-password \
  --docker-email=your-email@example.com \
  -n kubeflow-user-example-com

# Verify secret created
kubectl get secret regcred -n kubeflow-user-example-com
```

### Step 6: Deploy Notebook with Custom Image

Deploy a notebook server using your custom image:

```bash
# Apply the notebook manifest
kubectl apply -f manifests/notebook-custom-image.yaml

# Check notebook status
kubectl get notebooks -n kubeflow-user-example-com

# Wait for the notebook to be ready
kubectl wait --for=condition=Ready \
  notebook/custom-image-notebook \
  -n kubeflow-user-example-com \
  --timeout=300s
```

### Step 7: Access the Notebook

Access your notebook through the Kubeflow Dashboard:

```bash
# Get the notebook URL
kubectl get notebook custom-image-notebook \
  -n kubeflow-user-example-com \
  -o jsonpath='{.status.url}'

# Or port-forward directly
kubectl port-forward -n kubeflow-user-example-com \
  svc/custom-image-notebook 8080:80

# Access at http://localhost:8080
```

### Step 8: Verify Custom Packages

Once inside the notebook, verify your custom packages:

```python
# Create a new notebook and run:
import tensorflow as tf
import torch
import transformers
import custom_package

print(f"TensorFlow version: {tf.__version__}")
print(f"PyTorch version: {torch.__version__}")
print(f"Transformers version: {transformers.__version__}")

# Test GPU availability (if configured)
print(f"GPU available: {torch.cuda.is_available()}")
```

## Configuration Files

### Dockerfile
See `code/Dockerfile` for the complete image definition.

### Requirements.txt
See `code/requirements.txt` for Python package dependencies.

### Notebook Manifest
See `manifests/notebook-custom-image.yaml` for the Notebook CRD configuration.

## Validation

### Verify Image Built Successfully

```bash
# Check image exists locally
docker images my-kubeflow-notebook:v1.0

# Inspect image layers
docker history my-kubeflow-notebook:v1.0

# Check image size
docker images my-kubeflow-notebook:v1.0 --format "{{.Size}}"
```

### Verify Image in Registry

```bash
# For Docker Hub
docker pull yourusername/my-kubeflow-notebook:v1.0

# For GCR
gcloud container images list --repository=gcr.io/your-project

# For ECR
aws ecr describe-images --repository-name my-kubeflow-notebook
```

### Test Notebook Functionality

```bash
# Check notebook pod is running
kubectl get pods -n kubeflow-user-example-com -l notebook-name=custom-image-notebook

# View notebook logs
kubectl logs -n kubeflow-user-example-com \
  -l notebook-name=custom-image-notebook

# Exec into the notebook container
kubectl exec -it -n kubeflow-user-example-com \
  $(kubectl get pod -n kubeflow-user-example-com -l notebook-name=custom-image-notebook -o jsonpath='{.items[0].metadata.name}') \
  -- /bin/bash

# Inside the container, verify packages
pip list | grep tensorflow
```

## Expected Results

After completing this demo, you should observe:

1. **Custom Image Built**: Successfully built Docker image with your dependencies
2. **Image in Registry**: Image pushed and available in container registry
3. **Notebook Running**: Notebook server using custom image is running
4. **Packages Available**: All custom packages accessible in Jupyter environment
5. **Persistent Configuration**: Settings and packages persist across restarts

### Success Indicators

- [ ] Docker image builds without errors
- [ ] Image size is reasonable (< 5GB for most use cases)
- [ ] Image successfully pushed to registry
- [ ] Notebook pod starts and reaches Running state
- [ ] All custom packages import successfully
- [ ] Jupyter extensions are loaded
- [ ] GPU drivers work (if GPU configured)

## Troubleshooting

### Image Build Fails

**Problem**: Docker build fails with package installation errors

**Solution**:
```bash
# Use build cache to identify failing layer
docker build --progress=plain -t my-kubeflow-notebook:v1.0 .

# Try building individual layers
docker build --target builder -t test .

# Check for conflicting package versions
pip install --dry-run -r requirements.txt
```

### Image Too Large

**Problem**: Final image size exceeds several GB

**Solution**:
```dockerfile
# Use multi-stage builds
FROM python:3.9-slim as builder
RUN pip install --no-cache-dir -r requirements.txt

# Clean up in same layer
RUN apt-get update && apt-get install -y package \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Use .dockerignore to exclude unnecessary files
```

### Registry Push Fails

**Problem**: Cannot push image to registry

**Solution**:
```bash
# Re-authenticate
docker login your-registry.com

# Check registry permissions
docker push --debug your-registry.com/image:tag

# Verify network connectivity
curl -v https://your-registry.com/v2/
```

### Notebook Pod Won't Start

**Problem**: Notebook pod stuck in ImagePullBackOff

**Solution**:
```bash
# Check pod events
kubectl describe pod -n kubeflow-user-example-com -l notebook-name=custom-image-notebook

# Verify image pull secret
kubectl get secret regcred -n kubeflow-user-example-com -o yaml

# Test image pull manually
kubectl run test --image=your-registry.com/image:tag --image-pull-policy=Always -n kubeflow-user-example-com
```

### Packages Not Found in Notebook

**Problem**: Custom packages not available in Jupyter

**Solution**:
```bash
# Exec into pod and check
kubectl exec -it pod-name -n kubeflow-user-example-com -- pip list

# Verify requirements were installed
kubectl exec -it pod-name -n kubeflow-user-example-com -- cat /opt/conda/lib/python3.9/site-packages/*

# Check for installation errors in build logs
docker build --progress=plain . 2>&1 | tee build.log
```

## Advanced Usage

### Multi-Stage Build for Smaller Images

```dockerfile
# Build stage
FROM python:3.9 as builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Runtime stage
FROM gcr.io/kubeflow-images-public/tensorflow-2.6.0-notebook-cpu:1.0.0
COPY --from=builder /install /usr/local
```

### Custom Jupyter Extensions

```dockerfile
# Install Jupyter extensions
RUN pip install jupyter_contrib_nbextensions && \
    jupyter contrib nbextension install --sys-prefix && \
    jupyter nbextension enable collapsible_headings/main && \
    jupyter nbextension enable code_prettify/code_prettify
```

### GPU-Optimized Image

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install GPU-specific packages
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Add System Dependencies

```dockerfile
# Install system packages
RUN apt-get update && apt-get install -y \
    git \
    vim \
    htop \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

## Best Practices

1. **Use Official Base Images**: Start from Kubeflow's official notebook images
2. **Pin Versions**: Specify exact package versions for reproducibility
3. **Minimize Layers**: Combine RUN commands to reduce image size
4. **Clean Up**: Remove package manager caches in the same RUN command
5. **Use .dockerignore**: Exclude unnecessary files from build context
6. **Tag Properly**: Use semantic versioning for image tags
7. **Test Locally First**: Always test images locally before pushing
8. **Security Scanning**: Scan images for vulnerabilities before deployment
9. **Keep Images Small**: Remove build dependencies in final image
10. **Document Changes**: Maintain changelog for image versions

## Security Considerations

- Scan images for known vulnerabilities using tools like Trivy or Snyk
- Don't include secrets or credentials in the image
- Use minimal base images to reduce attack surface
- Keep base images and packages updated
- Use non-root users when possible
- Implement image signing for production deployments
- Use private registries for proprietary code
- Apply security contexts in Kubernetes manifests

## Cleanup

To remove the custom notebook:

```bash
# Delete the notebook
kubectl delete notebook custom-image-notebook -n kubeflow-user-example-com

# Verify deletion
kubectl get notebooks -n kubeflow-user-example-com

# Optional: Remove the image from registry
# Docker Hub
docker rmi yourusername/my-kubeflow-notebook:v1.0

# Or use registry API to delete remotely
```

## Additional Resources

- [Kubeflow Notebook Images](https://www.kubeflow.org/docs/components/notebooks/container-images/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/)
- [Container Image Security](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

## Related Demos

- [notebook-server-creation](../notebook-server-creation/): Basic notebook creation
- [notebook-gpu-allocation](../notebook-gpu-allocation/): GPU resource configuration
- [notebook-persistent-storage](../notebook-persistent-storage/): Data persistence

## Summary

This demo covered:
- Building custom Docker images for Kubeflow Notebooks
- Installing custom Python packages and dependencies
- Pushing images to container registries
- Deploying notebooks with custom images
- Best practices for image management

Custom images enable you to create reproducible, team-specific ML development environments in Kubeflow.
