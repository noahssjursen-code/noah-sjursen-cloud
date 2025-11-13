# Python Reusables - Shared Library Blueprint

## Purpose

This directory contains shared Python libraries following a class library pattern. Each module is self-contained, reusable, and importable by any project in the repository.

## Library Design Pattern

### Directory Structure

```
reusables/python/
├── requirements.txt          # Shared dependencies
├── __init__.py               # Root package marker
└── <module_name>/
    ├── __init__.py           # Module exports
    ├── client.py             # Main implementation
    ├── README.md             # Module documentation (required)
```

### Module Naming

- Use lowercase with underscores: `redis`, `gemini`, `database_utils`
- Name should describe the functionality clearly
- Avoid generic names like `utils` unless it's truly general purpose

## Creating a New Library Module

### Step 1: Create Directory Structure

```bash
mkdir reusables/python/<module_name>
cd reusables/python/<module_name>
```

### Step 2: Create `__init__.py`

Export the main functions/classes users will import:

```python
"""
Module description here.
"""

from .client import (
    main_function,
    MainClass,
    get_client,
)

__all__ = [
    'main_function',
    'MainClass', 
    'get_client',
]
```

### Step 3: Implement `client.py`

Follow these patterns:

**For Service Clients (Redis, Gemini, etc.):**

```python
"""
Module description and usage examples.
"""

import os
from typing import Optional

class ServiceClient:
    """
    Client for XYZ service.
    
    Usage:
        from reusables.python.module import get_client
        client = get_client()
    """
    
    _instance: Optional['ServiceClient'] = None
    
    @classmethod
    def get_client(cls, **config) -> 'ServiceClient':
        """
        Get or create singleton client.
        
        Args:
            **config: Configuration options
            
        Returns:
            Configured client instance
        """
        if cls._instance is None:
            cls._instance = cls(**config)
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset singleton (useful for testing)."""
        cls._instance = None
    
    def __init__(self, **config):
        # Initialize client
        pass

# Convenience function
def get_client(**config) -> ServiceClient:
    """Get the shared client instance."""
    return ServiceClient.get_client(**config)
```

**For Utility Functions:**

```python
"""
Utility functions for XYZ.
"""

from typing import Any, Optional

def utility_function(arg: str, optional: Optional[int] = None) -> Any:
    """
    Description of what this does.
    
    Args:
        arg: Description
        optional: Description (default: None)
        
    Returns:
        Description of return value
        
    Example:
        result = utility_function("test", optional=5)
    """
    pass
```

### Step 4: Add Dependencies

If the module requires external packages:

1. Add to `reusables/python/requirements.txt`
2. Use version pinning: `package>=1.0.0,<2.0.0`
3. Group related dependencies with comments:

```txt
# Redis
redis==5.0.1

# AI/ML
google-genai==1.0.0

# Your new module
new-package>=1.0.0
```

### Step 5: Document Usage (Required)

Every module must have a `README.md` documenting its usage:

```markdown
# Module Name

Brief description of what this module does.

## Installation

Requires dependencies from `requirements.txt`.

## Usage

\```python
from reusables.python.module import function_name

result = function_name()
\```

## API Reference

### `function_name(arg1, arg2)`

Description...
```

## Design Principles

### 1. Singleton Pattern for Clients

Use singleton pattern for service clients (databases, APIs, etc.) to avoid multiple connections:

```python
_instance: Optional[ClientClass] = None

@classmethod
def get_client(cls) -> ClientClass:
    if cls._instance is None:
        cls._instance = cls()
    return cls._instance
```

### 2. Environment-Based Configuration

Read config from environment variables with sensible defaults:

```python
host = os.getenv('SERVICE_HOST', 'localhost')
port = int(os.getenv('SERVICE_PORT', '8080'))
```

### 3. Type Hints

Always use type hints for function arguments and return values:

```python
def process_data(input: str, count: int = 10) -> List[Dict[str, Any]]:
    pass
```

### 4. Docstrings

Every function and class needs a docstring with:
- Brief description
- Args section
- Returns section
- Example usage

### 5. Error Handling

Handle errors gracefully with meaningful messages:

```python
try:
    result = external_call()
except SpecificError as e:
    print(f"❌ Failed to do X: {e}")
    raise
```

### 6. Logging vs Printing

- Use `print()` for important status messages (connection established, errors)
- Prefix with emojis for visibility: `✅ Success`, `❌ Error`, `⚠️ Warning`
- Keep output minimal

## Import Pattern for Projects

Projects should add parent directory to path before importing:

```python
import sys
import os

# Add reusables to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Now import
from reusables.python.redis import get_redis_client
from reusables.python.gemini import generate_text
```

## Current Modules

### `redis/`
Redis client with singleton pattern, CRUD operations, caching, counters, hash ops.

### `gemini/`
Gemini AI client wrapper with text generation and streaming support.

### `common/`
General utilities that don't fit in specific modules.

## Adding to Existing Modules

When adding functionality to existing modules:

1. Add new functions/classes to `client.py`
2. Export them in `__init__.py`
3. Update module's README
4. Keep related functionality together
5. Follow existing naming conventions in that module

