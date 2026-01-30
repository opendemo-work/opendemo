# Dashboard RBAC Configuration

## Overview

This demo demonstrates how to configure Role-Based Access Control (RBAC) for Kubeflow Dashboard, enabling multi-user namespace management and fine-grained permission control. You'll learn how to set up user isolation, configure roles and bindings, and manage access to Kubeflow resources.

Kubeflow's RBAC system extends Kubernetes RBAC to provide multi-tenancy support, allowing different users to work in isolated namespaces with appropriate permissions.

## Prerequisites

Before starting this demo, ensure you have:

- A running Kubernetes cluster (v1.24+) with RBAC enabled
- Kubeflow installed (v1.7+)
- kubectl configured with cluster admin access
- Basic understanding of Kubernetes RBAC concepts
- Kubeflow Dashboard already deployed

## Architecture

### RBAC Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubeflow Platform                        │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   User A     │      │   User B     │                    │
│  │  (email)     │      │  (email)     │                    │
│  └──────┬───────┘      └──────┬───────┘                    │
│         │                     │                            │
│         │                     │                            │
│  ┌──────▼──────────────────────▼───────┐                   │
│  │      Central Dashboard              │                   │
│  │   (Authentication Gateway)          │                   │
│  └──────┬──────────────────────┬───────┘                   │
│         │                      │                           │
│  ┌──────▼─────────┐     ┌──────▼─────────┐                │
│  │  Namespace A   │     │  Namespace B   │                │
│  │  ┌──────────┐  │     │  ┌──────────┐  │                │
│  │  │  Role    │  │     │  │  Role    │  │                │
│  │  │  Binding │  │     │  │  Binding │  │                │
│  │  └────┬─────┘  │     │  └────┬─────┘  │                │
│  │  ┌────▼─────┐  │     │  ┌────▼─────┐  │                │
│  │  │Resources │  │     │  │Resources │  │                │
│  │  │Notebooks │  │     │  │Notebooks │  │                │
│  │  │Pipelines │  │     │  │Pipelines │  │                │
│  │  └──────────┘  │     │  └──────────┘  │                │
│  └────────────────┘     └────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### Key Concepts

1. **Profile**: Kubeflow CRD that represents a user's namespace and associated RBAC policies
2. **ClusterRole**: Defines cluster-wide permissions
3. **Role**: Defines namespace-scoped permissions
4. **RoleBinding**: Binds roles to users/groups in a namespace
5. **ServiceAccount**: Identity for pods to access Kubeflow resources

## Step-by-Step Guide

### Step 1: Create User Profiles

Create separate profiles (namespaces) for different users:

```bash
# Create profile for data scientist
kubectl apply -f manifests/profile-data-scientist.yaml

# Create profile for ml engineer
kubectl apply -f manifests/profile-ml-engineer.yaml

# Verify profiles created
kubectl get profiles
```

### Step 2: Configure RBAC Roles

Apply custom roles with specific permissions:

```bash
# Apply kubeflow user role
kubectl apply -f manifests/kubeflow-user-role.yaml

# Apply kubeflow admin role
kubectl apply -f manifests/kubeflow-admin-role.yaml

# Verify roles
kubectl get clusterroles | grep kubeflow
```

### Step 3: Create Role Bindings

Bind roles to users in their respective namespaces:

```bash
# Create role bindings
kubectl apply -f manifests/role-bindings.yaml

# Verify bindings
kubectl get rolebindings -n kubeflow-user-data-scientist
kubectl get rolebindings -n kubeflow-user-ml-engineer
```

### Step 4: Configure Service Accounts

Set up service accounts for application access:

```bash
# Create service accounts
kubectl apply -f manifests/service-accounts.yaml

# Verify service accounts
kubectl get serviceaccounts -n kubeflow-user-data-scientist
```

### Step 5: Test RBAC Configuration

Verify that RBAC is working correctly:

```bash
# Test as data scientist user
kubectl auth can-i create notebooks --as=user-data-scientist@example.com -n kubeflow-user-data-scientist
# Should return: yes

# Test unauthorized access
kubectl auth can-i delete notebooks --as=user-data-scientist@example.com -n kubeflow-user-ml-engineer
# Should return: no

# Test admin access
kubectl auth can-i '*' '*' --as=kubeflow-admin@example.com -n kubeflow
# Should return: yes
```

### Step 6: Access Dashboard with RBAC

Configure Dashboard to use the RBAC settings:

```bash
# Update Dashboard configuration
kubectl apply -f manifests/dashboard-rbac-config.yaml

# Verify Dashboard can authenticate users
kubectl logs -n kubeflow deployment/centraldashboard | grep -i rbac
```

## Configuration Files

### Profile for Data Scientist
See `manifests/profile-data-scientist.yaml` for user profile configuration.

### Kubeflow User Role
See `manifests/kubeflow-user-role.yaml` for standard user permissions.

### Role Bindings
See `manifests/role-bindings.yaml` for user-to-role mappings.

## Validation

### Test User Isolation

```bash
# Create a notebook in user-data-scientist namespace
kubectl apply -f - <<EOF
apiVersion: kubeflow.org/v1
kind: Notebook
metadata:
  name: test-notebook
  namespace: kubeflow-user-data-scientist
spec:
  template:
    spec:
      containers:
      - name: notebook
        image: jupyter/scipy-notebook:latest
EOF

# Try to access from another namespace (should fail)
kubectl get notebooks -n kubeflow-user-ml-engineer --as=user-data-scientist@example.com
```

### Verify Permission Boundaries

```bash
# Test create permissions
kubectl auth can-i create notebooks --as=user-data-scientist@example.com -n kubeflow-user-data-scientist

# Test delete permissions
kubectl auth can-i delete notebooks --as=user-data-scientist@example.com -n kubeflow-user-data-scientist

# Test cluster-wide access (should be denied)
kubectl auth can-i get nodes --as=user-data-scientist@example.com
```

### Check Dashboard Access Logs

```bash
# Monitor Dashboard authentication
kubectl logs -n kubeflow deployment/centraldashboard -f | grep -i "auth\|rbac"

# Check for any permission denied errors
kubectl logs -n kubeflow deployment/centraldashboard | grep -i "denied\|unauthorized"
```

## Expected Results

After completing this demo, you should observe:

1. **Multiple User Profiles**: Each user has an isolated namespace
2. **Role-Based Access**: Users can only access resources in their namespaces
3. **Permission Enforcement**: Unauthorized actions are blocked
4. **Dashboard Integration**: Dashboard respects RBAC policies
5. **Service Account Access**: Applications can authenticate with proper permissions

### Verification Checklist

- [ ] User profiles are created and active
- [ ] Roles and bindings are applied correctly
- [ ] Users can access their own namespaces
- [ ] Users cannot access other namespaces
- [ ] Service accounts work properly
- [ ] Dashboard displays correct namespaces per user

## Troubleshooting

### Profile Not Creating Namespace

**Problem**: Profile created but namespace doesn't exist

**Solution**:
```bash
# Check profile status
kubectl describe profile kubeflow-user-data-scientist

# Check profile controller logs
kubectl logs -n kubeflow deployment/profiles-controller

# Manually create namespace if needed
kubectl create namespace kubeflow-user-data-scientist
```

### Permission Denied Errors

**Problem**: User gets permission denied even with correct role

**Solution**:
```bash
# Verify role binding
kubectl get rolebinding -n kubeflow-user-data-scientist

# Check role permissions
kubectl describe role kubeflow-user -n kubeflow-user-data-scientist

# Verify user identity
kubectl auth can-i list notebooks --as=user@example.com -n kubeflow-user-data-scientist -v=10
```

### Dashboard Not Showing Namespaces

**Problem**: User logs in but doesn't see their namespace

**Solution**:
```bash
# Check Dashboard configuration
kubectl get configmap centraldashboard-config -n kubeflow -o yaml

# Verify profile-controller is running
kubectl get pods -n kubeflow | grep profile

# Check for authentication errors
kubectl logs -n kubeflow deployment/centraldashboard | grep -i "error\|failed"
```

### Service Account Token Issues

**Problem**: Service account cannot authenticate

**Solution**:
```bash
# Verify service account exists
kubectl get serviceaccount -n kubeflow-user-data-scientist

# Check token secret
kubectl get secrets -n kubeflow-user-data-scientist | grep default-token

# Create token manually if needed
kubectl create token default-editor -n kubeflow-user-data-scientist
```

## Advanced Usage

### Custom Roles for ML Teams

Create specialized roles for different ML team members:

```yaml
# ML Experimenter - Can create and run experiments
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ml-experimenter
rules:
- apiGroups: ["kubeflow.org"]
  resources: ["notebooks", "experiments", "trials"]
  verbs: ["get", "list", "create", "update"]
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list"]

---
# ML Deployer - Can deploy models
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ml-deployer
rules:
- apiGroups: ["serving.kserve.io"]
  resources: ["inferenceservices"]
  verbs: ["get", "list", "create", "update", "delete"]
```

### Multi-Tenant Pipeline Access

Configure shared pipeline access across teams:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: shared-pipeline-viewer
rules:
- apiGroups: ["pipelines.kubeflow.org"]
  resources: ["pipelines"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: all-users-view-pipelines
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: shared-pipeline-viewer
subjects:
- kind: Group
  name: system:authenticated
  apiGroup: rbac.authorization.k8s.io
```

### Dynamic Resource Quotas

Apply resource limits per user namespace:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: user-quota
  namespace: kubeflow-user-data-scientist
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    requests.nvidia.com/gpu: "2"
    persistentvolumeclaims: "5"
```

## Best Practices

1. **Principle of Least Privilege**: Grant only necessary permissions
2. **Namespace Isolation**: Keep user workloads in separate namespaces
3. **Regular Audits**: Periodically review RBAC configurations
4. **Service Account Rotation**: Rotate service account tokens regularly
5. **Group-Based Management**: Use groups instead of individual users when possible
6. **Resource Quotas**: Set limits to prevent resource exhaustion
7. **Audit Logging**: Enable audit logs for security compliance

## Security Considerations

- Use external authentication providers (OIDC, LDAP) for production
- Enable Pod Security Policies or Pod Security Standards
- Implement network policies for namespace isolation
- Regular security scans of RBAC configurations
- Monitor for privilege escalation attempts
- Use admission controllers to enforce security policies

## Cleanup

To remove the RBAC configuration:

```bash
# Delete role bindings
kubectl delete -f manifests/role-bindings.yaml

# Delete roles
kubectl delete -f manifests/kubeflow-user-role.yaml
kubectl delete -f manifests/kubeflow-admin-role.yaml

# Delete profiles (this will delete namespaces)
kubectl delete profile kubeflow-user-data-scientist
kubectl delete profile kubeflow-user-ml-engineer

# Verify cleanup
kubectl get profiles
kubectl get clusterroles | grep kubeflow
```

## Additional Resources

- [Kubeflow Multi-User Isolation](https://www.kubeflow.org/docs/components/multi-tenancy/)
- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubeflow Profiles Documentation](https://www.kubeflow.org/docs/components/multi-tenancy/getting-started/)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

## Related Demos

- [dashboard-basic-setup](../dashboard-basic-setup/): Basic Dashboard installation
- [notebook-server-creation](../notebook-server-creation/): Create Notebook servers
- [pipeline-experiment-management](../pipeline-experiment-management/): Manage ML experiments

## Summary

This demo covered:
- Creating user profiles for namespace isolation
- Configuring RBAC roles and bindings
- Testing permission boundaries
- Integrating RBAC with Kubeflow Dashboard
- Best practices for multi-user environments

RBAC is essential for production Kubeflow deployments to ensure security and resource isolation in multi-tenant scenarios.
