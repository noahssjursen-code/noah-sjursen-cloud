"""
Gemini AI utilities for Noah Sjursen Cloud.
Generic AI client - no app-specific logic.
"""

from .client import (
    # Core client
    get_gemini_client,
    GeminiClient,
    
    # Text generation
    generate_text,
    generate_text_stream,
    
    # Utilities
    strip_code_blocks,
)

__all__ = [
    'get_gemini_client',
    'GeminiClient',
    'generate_text',
    'generate_text_stream',
    'strip_code_blocks',
]

