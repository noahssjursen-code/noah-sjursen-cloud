"""
GCP utilities for Noah Sjursen Cloud.
IAM permissions checking, project access validation, and gcloud command execution.
"""

import os
import subprocess
import json
from typing import Optional, Dict, Any, List


def check_user_has_project_access(email: str, project_id: Optional[str] = None) -> bool:
    """
    Check if a user email has IAM permissions on a GCP project.
    
    Args:
        email: User email to check
        project_id: GCP project ID (defaults to GCP_PROJECT_ID env var)
    
    Returns:
        True if user has any IAM role on the project
    
    Example:
        if check_user_has_project_access("user@gmail.com", "my-project"):
            print("User has access")
    """
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
    
    if not project_id:
        raise ValueError("project_id must be provided or GCP_PROJECT_ID env var must be set")
    
    try:
        # Use gcloud CLI to get IAM policy (Windows needs shell=True)
        cmd = f'gcloud projects get-iam-policy {project_id} --format=json'
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            shell=True
        )
        
        if result.returncode != 0:
            print(f"❌ Error getting IAM policy: {result.stderr}")
            return False
        
        policy = json.loads(result.stdout)
        user_member = f"user:{email}"
        
        # Check if user is in any role binding
        for binding in policy.get('bindings', []):
            if user_member in binding.get('members', []):
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error checking IAM permissions: {e}")
        return False


def get_user_project_roles(email: str, project_id: Optional[str] = None) -> list[str]:
    """
    Get all IAM roles a user has on a GCP project.
    
    Args:
        email: User email to check
        project_id: GCP project ID (defaults to GCP_PROJECT_ID env var)
    
    Returns:
        List of role names (e.g., ['roles/viewer', 'roles/editor'])
    
    Example:
        roles = get_user_project_roles("user@gmail.com")
        print(f"User has roles: {roles}")
    """
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
    
    if not project_id:
        raise ValueError("project_id must be provided or GCP_PROJECT_ID env var must be set")
    
    try:
        # Use gcloud CLI to get IAM policy (Windows needs shell=True)
        cmd = f'gcloud projects get-iam-policy {project_id} --format=json'
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            shell=True
        )
        
        if result.returncode != 0:
            print(f"❌ Error getting IAM policy: {result.stderr}")
            return []
        
        policy = json.loads(result.stdout)
        user_member = f"user:{email}"
        roles = []
        
        # Find all roles for this user
        for binding in policy.get('bindings', []):
            if user_member in binding.get('members', []):
                roles.append(binding.get('role', ''))
        
        return [r for r in roles if r]
        
    except Exception as e:
        print(f"❌ Error getting user roles: {e}")
        return []


# ============================================================================
# GCLOUD COMMAND EXECUTION
# ============================================================================

def execute_gcloud_command(command: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute a gcloud command and return JSON output.
    
    Args:
        command: gcloud command to execute (without 'gcloud' prefix)
        timeout: Command timeout in seconds
    
    Returns:
        Dict with 'success', 'data', and optional 'error' keys
    
    Example:
        result = execute_gcloud_command("compute instances list --format=json")
        if result['success']:
            print(result['data'])
    """
    try:
        # Ensure command includes --format=json
        if '--format=json' not in command:
            command += ' --format=json'
        
        full_command = f'gcloud {command}'
        
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=True
        )
        
        if result.returncode != 0:
            return {
                'success': False,
                'error': result.stderr.strip(),
                'data': None
            }
        
        # Parse JSON output
        try:
            data = json.loads(result.stdout) if result.stdout.strip() else []
        except json.JSONDecodeError:
            data = result.stdout.strip()
        
        return {
            'success': True,
            'data': data,
            'error': None
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Command timed out after {timeout} seconds',
            'data': None
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': None
        }


def list_compute_instances(project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all Compute Engine instances in a project.
    
    Args:
        project_id: GCP project ID (defaults to GCP_PROJECT_ID env var)
    
    Returns:
        List of instance dictionaries
    
    Example:
        instances = list_compute_instances("my-project")
        for instance in instances:
            print(f"{instance['name']}: {instance['status']}")
    """
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
    
    command = f'compute instances list --project={project_id}'
    result = execute_gcloud_command(command)
    
    return result['data'] if result['success'] else []


def list_cloud_run_services(project_id: Optional[str] = None, region: str = 'us-central1') -> List[Dict[str, Any]]:
    """
    List all Cloud Run services in a project.
    
    Args:
        project_id: GCP project ID (defaults to GCP_PROJECT_ID env var)
        region: GCP region
    
    Returns:
        List of service dictionaries
    
    Example:
        services = list_cloud_run_services()
        for service in services:
            print(f"{service['metadata']['name']}: {service['status']['url']}")
    """
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
    
    command = f'run services list --project={project_id} --region={region} --platform=managed'
    result = execute_gcloud_command(command)
    
    return result['data'] if result['success'] else []


def list_storage_buckets(project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all Cloud Storage buckets in a project.
    
    Args:
        project_id: GCP project ID (defaults to GCP_PROJECT_ID env var)
    
    Returns:
        List of bucket dictionaries
    
    Example:
        buckets = list_storage_buckets()
        for bucket in buckets:
            print(f"{bucket['name']}: {bucket['location']}")
    """
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
    
    command = f'storage buckets list --project={project_id}'
    result = execute_gcloud_command(command)
    
    return result['data'] if result['success'] else []


def list_all_resources(project_id: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    List all major resources in a GCP project.
    
    Args:
        project_id: GCP project ID (defaults to GCP_PROJECT_ID env var)
    
    Returns:
        Dictionary with resource types as keys
    
    Example:
        resources = list_all_resources()
        print(f"Compute instances: {len(resources['compute_instances'])}")
        print(f"Cloud Run services: {len(resources['cloud_run_services'])}")
    """
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
    
    return {
        'compute_instances': list_compute_instances(project_id),
        'cloud_run_services': list_cloud_run_services(project_id),
        'storage_buckets': list_storage_buckets(project_id)
    }


def list_project_iam_members(project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all IAM members with their roles in a project.
    
    Args:
        project_id: GCP project ID (defaults to GCP_PROJECT_ID env var)
    
    Returns:
        List of members with their roles
    
    Example:
        members = list_project_iam_members()
        for member in members:
            print(f"{member['email']}: {member['roles']}")
    """
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
    
    try:
        command = f'projects get-iam-policy {project_id}'
        result = execute_gcloud_command(command)
        
        if not result['success']:
            return []
        
        policy = result['data']
        members_map = {}
        
        # Group roles by member
        for binding in policy.get('bindings', []):
            role = binding.get('role', '')
            for member in binding.get('members', []):
                if member not in members_map:
                    members_map[member] = {'member': member, 'roles': []}
                members_map[member]['roles'].append(role)
        
        return list(members_map.values())
        
    except Exception as e:
        print(f"❌ Error listing IAM members: {e}")
        return []


