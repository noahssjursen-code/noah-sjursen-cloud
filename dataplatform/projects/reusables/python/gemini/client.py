"""
Gemini AI client for Noah Sjursen Cloud.
Reusable Gemini 2.0 Flash integration with text output cleaning.
"""

import os
import re
from typing import Optional, Generator
from google import genai
from google.genai import types


class GeminiClient:
    """
    Reusable Gemini AI client.
    
    Usage:
        from reusables.python.gemini import get_gemini_client, generate_text
        
        client = get_gemini_client()
        response = generate_text("Explain Redis caching")
        print(response)
    """
    
    _instance: Optional[genai.Client] = None
    
    @classmethod
    def get_client(cls, api_key: Optional[str] = None) -> genai.Client:
        """
        Get or create Gemini client singleton.
        
        Args:
            api_key: Optional API key (defaults to GEMINI_API_KEY env var)
        
        Returns:
            Configured Gemini client
        """
        if cls._instance is None:
            key = api_key or os.environ.get("GEMINI_API_KEY")
            if not key:
                raise ValueError("GEMINI_API_KEY environment variable not set and no api_key provided")
            
            cls._instance = genai.Client(api_key=key)
            print("✅ Gemini client initialized")
        
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the singleton instance."""
        cls._instance = None


def get_gemini_client(api_key: Optional[str] = None) -> genai.Client:
    """
    Get the shared Gemini client.
    
    Args:
        api_key: Optional API key (defaults to GEMINI_API_KEY env var)
    
    Returns:
        Configured Gemini client
    """
    return GeminiClient.get_client(api_key)


def strip_code_blocks(text: str) -> str:
    """
    Strip code block markers from AI responses.
    
    Removes:
        - ```python, ```javascript, etc.
        - ``` at start/end
        - Leaves the actual code content
    
    Args:
        text: Raw AI response text
    
    Returns:
        Cleaned text without code block markers
    
    Example:
        Input:  "```python\\nprint('hello')\\n```"
        Output: "print('hello')"
    """
    # Remove code blocks with language specifier: ```python, ```javascript, etc.
    text = re.sub(r'```\w+\n', '', text)
    
    # Remove standalone code block markers: ```
    text = re.sub(r'```', '', text)
    
    # Clean up extra newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def generate_text(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "gemini-2.0-flash-lite",
    temperature: float = 0.7,
    strip_code_markers: bool = True
) -> str:
    """
    Generate text using Gemini 2.0 Flash Lite.
    
    Args:
        prompt: Input prompt/question
        api_key: Optional API key (uses env var if not provided)
        model: Gemini model to use (default: gemini-2.0-flash-lite)
        temperature: Creativity (0.0-1.0, default: 0.7)
        strip_code_markers: Remove code block markers from output
    
    Returns:
        Generated text (cleaned if strip_code_markers=True)
    
    Example:
        response = generate_text("Explain Redis in one sentence")
        print(response)
    """
    client = get_gemini_client(api_key)
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]
    
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=8192
    )
    
    # Generate response
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config
    )
    
    text = response.text
    
    # Strip code block markers if requested
    if strip_code_markers:
        text = strip_code_blocks(text)
    
    return text


def generate_text_stream(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "gemini-2.0-flash-lite",
    temperature: float = 0.7,
    strip_code_markers: bool = True
) -> Generator[str, None, None]:
    """
    Generate text using Gemini 2.0 Flash Lite (streaming).
    
    Args:
        prompt: Input prompt/question
        api_key: Optional API key (uses env var if not provided)
        model: Gemini model to use (default: gemini-2.0-flash-lite)
        temperature: Creativity (0.0-1.0, default: 0.7)
        strip_code_markers: Remove code block markers from output
    
    Yields:
        Text chunks as they're generated
    
    Example:
        for chunk in generate_text_stream("Write a poem about Redis"):
            print(chunk, end="", flush=True)
    """
    client = get_gemini_client(api_key)
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]
    
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=8192
    )
    
    # Stream response
    full_text = []
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config
    ):
        if chunk.text:
            full_text.append(chunk.text)
            yield chunk.text
    
    # If stripping code markers, yield cleaned version at the end
    if strip_code_markers and full_text:
        complete_text = ''.join(full_text)
        cleaned = strip_code_blocks(complete_text)
        # Clear previous output conceptually (caller handles this)


