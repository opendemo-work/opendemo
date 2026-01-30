# Notebook Persistent Storage

## Overview

This demo demonstrates how to configure persistent volumes for Kubeflow Notebooks to preserve data, code, and work across pod restarts and recreations. Persistent storage is essential for maintaining your development environment, datasets, models, and experiment results in Kubeflow.

Without persistent storage, all data in a notebook is lost when the pod is deleted or restarted. This demo shows how to configure PersistentVolumeClaims (PVCs) to ensure data persistence.

## Prerequisites

Before starting this demo, ensure you have:

- A Kubernetes cluster with Kubeflow Notebooks (v1.7+)
- Storage provisioner installed (e.g., default storage class)
- kubectl configured with cluster access
- Basic understanding of Kubernetes storage concepts
- Familiarity with PersistentVolumes and PersistentVolumeClaims

## Architecture

### Storage Architecture

```
┌─────────────────────────────────────────────────────┐
│         Kubeflow Notebook Pod                       │
│                                                     │
│  ┌──────────────────────────────────────────┐     │
│  │  Jupyter Notebook Container              │     │
│  │  ┌────────────────────────────────────┐  │     │
│  │  │  /home/jovyan/work (mounted PVC)   │  │     │
│  │  │  - notebooks/                      │  │     │
│  │  │  - data/                          │  │     │
│  │  │  - models/                        │  │     │
│  │  └────────────────────────────────────┘  │     │
│  └──────────────────────────────────────────┘     │
│                    │                               │
│                    ▼                               │
│  ┌──────────────────────────────────────────┐     │
│  │  PersistentVolumeClaim (PVC)             │     │
│  │  - Size: 10Gi                            │     │
│  │  - AccessMode: ReadWriteOnce             │     │
│  └──────────────────────────────────────────┘     │
│                    │                               │
└────────────────────┼───────────────────────────────┘
                     │
                     ▼
      ┌──────────────────────────────┐
      │  PersistentVolume (PV)       │
      │  - Storage Backend           │
      │    (NFS/Ceph/EBS/etc)        │
      └──────────────────────────────┘
```

## Step-by-Step Guide

### Step 1: Check Available Storage Classes

```bash
# List available storage classes
kubectl get storageclass

# View default storage class
kubectl get storageclass -o jsonpath='{.items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=="true")].metadata.name}'
```

### Step 2: Create Notebook with Persistent Storage

Apply the notebook manifest that includes PVC configuration:

```bash
kubectl apply -f manifests/notebook-with-pvc.yaml

# Check notebook status
kubectl get notebooks -n kubeflow-user-example-com

# Check PVC status
kubectl get pvc -n kubeflow-user-example-com
```

### Step 3: Verify PVC is Bound

```bash
# Check PVC details
kubectl describe pvc notebook-workspace -n kubeflow-user-example-com

# Expected status: Bound
# Should show volume name and capacity
```

### Step 4: Access Notebook and Verify Storage

Once the notebook is ready, access it and verify the persistent volume:

```bash
# Port-forward to notebook
kubectl port-forward -n kubeflow-user-example-com \
  svc/persistent-storage-notebook 8080:80

# Access at http://localhost:8080
```

### Step 5: Test Data Persistence

In Jupyter, create test data:

```python
# Create a test file
import os
import json
from datetime import datetime

# Create test data
data = {
    "timestamp": str(datetime.now()),
    "message": "This data should persist across restarts"
}

# Write to persistent storage
with open('/home/jovyan/work/test_persistence.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Data saved to persistent storage")
```

### Step 6: Restart Notebook and Verify

Delete and recreate the notebook to test persistence:

```bash
# Delete the notebook
kubectl delete notebook persistent-storage-notebook -n kubeflow-user-example-com

# Recreate it (PVC remains)
kubectl apply -f manifests/notebook-with-pvc.yaml

# Wait for notebook to be ready
kubectl wait --for=condition=Ready \
  notebook/persistent-storage-notebook \
  -n kubeflow-user-example-com \
  --timeout=300s
```

### Step 7: Verify Data Persisted

Access the recreated notebook and check if data exists:

```python
# Read the previously saved file
import json

with open('/home/jovyan/work/test_persistence.json', 'r') as f:
    data = json.load(f)

print("Data from persistent storage:")
print(json.dumps(data, indent=2))
# Should show the data created before restart
```

## Configuration Files

### Notebook with PVC
See `manifests/notebook-with-pvc.yaml` for the complete configuration.

### Shared Storage Configuration
See `manifests/shared-pvc.yaml` for multi-notebook shared storage.

## Validation

### Verify PVC is Created

```bash
# Check PVC status
kubectl get pvc -n kubeflow-user-example-com

# Expected output:
# NAME                  STATUS   VOLUME            CAPACITY   ACCESS MODES
# notebook-workspace    Bound    pvc-xxxxx         10Gi       RWO
```

### Check Storage Usage

```bash
# Exec into notebook pod
kubectl exec -it -n kubeflow-user-example-com \
  $(kubectl get pod -n kubeflow-user-example-com -l notebook-name=persistent-storage-notebook -o jsonpath='{.items[0].metadata.name}') \
  -- df -h /home/jovyan/work

# Should show mounted volume with size
```

### Test Write and Read

```bash
# Write test file
kubectl exec -n kubeflow-user-example-com \
  $(kubectl get pod -n kubeflow-user-example-com -l notebook-name=persistent-storage-notebook -o jsonpath='{.items[0].metadata.name}') \
  -- bash -c "echo 'test data' > /home/jovyan/work/test.txt"

# Read test file
kubectl exec -n kubeflow-user-example-com \
  $(kubectl get pod -n kubeflow-user-example-com -l notebook-name=persistent-storage-notebook -o jsonpath='{.items[0].metadata.name}') \
  -- cat /home/jovyan/work/test.txt
```

## Expected Results

After completing this demo, you should observe:

1. **PVC Created**: PersistentVolumeClaim successfully bound to a PV
2. **Data Persists**: Files survive notebook pod restarts
3. **Workspace Available**: /home/jovyan/work directory contains persistent data
4. **Storage Mounted**: df command shows mounted volume
5. **No Data Loss**: Previously created files accessible after restart

### Success Indicators

- [ ] PVC status is "Bound"
- [ ] Notebook pod successfully mounts the volume
- [ ] Files created in /home/jovyan/work persist across restarts
- [ ] Storage capacity matches requested size
- [ ] No permission errors when writing to storage

## Troubleshooting

### PVC Stuck in Pending

**Problem**: PVC remains in Pending state

**Solution**:
```bash
# Check PVC events
kubectl describe pvc notebook-workspace -n kubeflow-user-example-com

# Common causes:
# 1. No storage provisioner available
kubectl get storageclass

# 2. Insufficient storage
kubectl get pv

# 3. Node affinity issues
kubectl describe pv <pv-name>
```

### Permission Denied Errors

**Problem**: Cannot write to persistent volume

**Solution**:
```bash
# Check volume permissions
kubectl exec -n kubeflow-user-example-com \
  <pod-name> -- ls -la /home/jovyan/work

# Fix permissions using initContainer in notebook spec
# Add to notebook YAML:
initContainers:
- name: fix-permissions
  image: busybox
  command: ['sh', '-c', 'chown -R 1000:100 /home/jovyan/work']
  volumeMounts:
  - name: workspace
    mountPath: /home/jovyan/work
```

### PVC Cannot Be Deleted

**Problem**: PVC stuck in Terminating state

**Solution**:
```bash
# Check what's using the PVC
kubectl get pods -n kubeflow-user-example-com -o json | \
  jq '.items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName=="notebook-workspace") | .metadata.name'

# Delete the pod first
kubectl delete pod <pod-name> -n kubeflow-user-example-com

# Force delete PVC if needed (data will be lost)
kubectl patch pvc notebook-workspace -n kubeflow-user-example-com -p '{"metadata":{"finalizers":null}}'
```

### Storage Full

**Problem**: Out of disk space on persistent volume

**Solution**:
```bash
# Check usage
kubectl exec -n kubeflow-user-example-com <pod-name> -- du -sh /home/jovyan/work/*

# Option 1: Clean up unnecessary files
kubectl exec -n kubeflow-user-example-com <pod-name> -- rm -rf /home/jovyan/work/old_data

# Option 2: Expand PVC (if storage class supports it)
kubectl patch pvc notebook-workspace -n kubeflow-user-example-com \
  -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
```

## Advanced Usage

### Multiple PVCs for Different Data Types

```yaml
spec:
  template:
    spec:
      volumes:
      - name: workspace
        persistentVolumeClaim:
          claimName: notebook-workspace
      - name: datasets
        persistentVolumeClaim:
          claimName: shared-datasets
      - name: models
        persistentVolumeClaim:
          claimName: model-storage
      containers:
      - name: notebook
        volumeMounts:
        - name: workspace
          mountPath: /home/jovyan/work
        - name: datasets
          mountPath: /home/jovyan/datasets
        - name: models
          mountPath: /home/jovyan/models
```

### Shared Storage Between Notebooks

```yaml
# Create shared PVC with ReadWriteMany
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-workspace
spec:
  accessModes:
  - ReadWriteMany  # Allows multiple pods to mount
  resources:
    requests:
      storage: 50Gi
```

### Backup and Restore

```bash
# Backup notebook data
kubectl exec -n kubeflow-user-example-com <pod-name> -- \
  tar czf /tmp/backup.tar.gz /home/jovyan/work

kubectl cp kubeflow-user-example-com/<pod-name>:/tmp/backup.tar.gz ./backup.tar.gz

# Restore to new notebook
kubectl cp ./backup.tar.gz kubeflow-user-example-com/<new-pod-name>:/tmp/
kubectl exec -n kubeflow-user-example-com <new-pod-name> -- \
  tar xzf /tmp/backup.tar.gz -C /
```

## Best Practices

1. **Right-size Storage**: Request appropriate storage size for your needs
2. **Use Storage Classes**: Leverage different storage classes for different performance needs
3. **Regular Backups**: Backup important data regularly
4. **Organize Data**: Use clear directory structure in persistent volume
5. **Monitor Usage**: Track storage usage to avoid running out of space
6. **Cleanup**: Remove unused data periodically
7. **Separate Concerns**: Use different PVCs for code, data, and models
8. **Document Storage**: Keep track of what's stored where

## Security Considerations

- Set appropriate file permissions on persistent volumes
- Use separate namespaces and PVCs for different users
- Implement RBAC to control PVC access
- Enable encryption at rest for sensitive data
- Regular security scans of stored data
- Implement data retention policies

## Cleanup

To remove the notebook and storage:

```bash
# Delete notebook (PVC will remain)
kubectl delete notebook persistent-storage-notebook -n kubeflow-user-example-com

# Delete PVC (this will delete all data!)
kubectl delete pvc notebook-workspace -n kubeflow-user-example-com

# Verify cleanup
kubectl get pvc -n kubeflow-user-example-com
```

## Additional Resources

- [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Kubeflow Notebook Storage](https://www.kubeflow.org/docs/components/notebooks/setup/)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)

## Related Demos

- [notebook-server-creation](../notebook-server-creation/): Basic notebook setup
- [notebook-custom-image](../notebook-custom-image/): Custom images
- [notebook-gpu-allocation](../notebook-gpu-allocation/): GPU resources

## Summary

This demo covered:
- Creating PersistentVolumeClaims for notebooks
- Configuring persistent storage in Kubeflow Notebooks
- Testing data persistence across pod restarts
- Managing and troubleshooting storage issues
- Best practices for storage management

Persistent storage is crucial for production Kubeflow deployments, ensuring that valuable work, datasets, and models are preserved across notebook lifecycle events.
