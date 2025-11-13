# GCP Utilities

Utilities for GCP project access validation, IAM permission checking, and resource management via gcloud CLI.

## Installation

Requires dependencies from `reusables/python/requirements.txt`:

```txt
google-cloud-resourcemanager>=1.12.0
```

## Usage

### Check User Access

```python
from reusables.python.gcp import check_user_has_project_access

# Check if user has any IAM role on project
has_access = check_user_has_project_access(
    email="user@gmail.com",
    project_id="my-project"
)

if has_access:
    print("User has access")
```

### Get User Roles

```python
from reusables.python.gcp import get_user_project_roles

# Get all roles user has on project
roles = get_user_project_roles(
    email="user@gmail.com",
    project_id="my-project"
)

print(f"User roles: {roles}")
# Example: ['roles/viewer', 'roles/editor']
```

## Environment Variables

Both functions default to `GCP_PROJECT_ID` env var if project_id not provided:

```python
# Set in .env
GCP_PROJECT_ID=my-project

# Then use without project_id parameter
has_access = check_user_has_project_access("user@gmail.com")
```

## Resource Management

### Execute Custom Commands

```python
from reusables.python.gcp import execute_gcloud_command

# Execute any gcloud command
result = execute_gcloud_command("compute instances list --project=my-project")

if result['success']:
    print(result['data'])  # JSON parsed data
else:
    print(result['error'])
```

### List Resources

```python
from reusables.python.gcp import (
    list_compute_instances,
    list_cloud_run_services,
    list_storage_buckets,
    list_all_resources
)

# List specific resources
instances = list_compute_instances("my-project")
services = list_cloud_run_services("my-project")
buckets = list_storage_buckets("my-project")

# List everything
all_resources = list_all_resources("my-project")
print(f"Instances: {len(all_resources['compute_instances'])}")
print(f"Services: {len(all_resources['cloud_run_services'])}")
print(f"Buckets: {len(all_resources['storage_buckets'])}")
```

### List IAM Members

```python
from reusables.python.gcp import list_project_iam_members

members = list_project_iam_members("my-project")
for member in members:
    print(f"{member['member']}: {member['roles']}")
```

## API Reference

### `check_user_has_project_access(email, project_id=None)`

Check if user has any IAM permissions on project.

**Args:**
- `email` (str): User email to check
- `project_id` (str, optional): GCP project ID

**Returns:**
- `bool`: True if user has any role on project

**Example:**
```python
if check_user_has_project_access("admin@example.com", "prod-project"):
    allow_access()
```

### `get_user_project_roles(email, project_id=None)`

Get all IAM roles a user has on project.

**Args:**
- `email` (str): User email to check
- `project_id` (str, optional): GCP project ID

**Returns:**
- `list[str]`: List of role names

**Example:**
```python
roles = get_user_project_roles("user@example.com")
if "roles/owner" in roles:
    grant_admin_access()
```

## Error Handling

Both functions fail safely:
- On error, `check_user_has_project_access()` returns `False`
- On error, `get_user_project_roles()` returns `[]`
- Errors are printed to console

## Authentication

Requires GCP credentials configured:

**Local development:**
```bash
# Use service account key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

**Production (Cloud Run):**
- Uses Cloud Run's default service account automatically
- No credentials needed

