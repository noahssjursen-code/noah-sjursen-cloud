"""
Common utilities shared across all projects.
"""

def get_greeting(service_name: str) -> str:
    """
    Simple utility function to demonstrate shared code pattern.
    Similar to how you'd share TableStorage clients in C#.
    
    Args:
        service_name: Name of the service calling this function
        
    Returns:
        A greeting message from the reusables library
    """
    return f"Hello from {service_name}! This message came from the reusables library 🎉"


def get_library_info() -> dict:
    """
    Returns information about the reusables library.
    """
    return {
        "library": "noah-sjursen-cloud-reusables",
        "version": "0.1.0",
        "description": "Shared utilities for all Noah Sjursen Cloud services"
    }

