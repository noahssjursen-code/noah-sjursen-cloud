"""
Configuration for Komfyrvakt.
Environment-based settings for self-hosting or cloud deployment.
"""

import os
import secrets
from typing import Literal
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment from {env_path}")
else:
    print(f"⚠️  No .env file found at {env_path}")


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Settings
    API_KEY: str = os.getenv('KOMFYRVAKT_API_KEY', '')
    API_KEY_PREFIX: str = "kmf_"
    
    # Redis Settings
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    
    # Environment
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'local')
    
    # Log Storage Settings
    LOG_RETENTION_HOURS: int = int(os.getenv('LOG_RETENTION_HOURS', '48'))  # How long logs stay in Redis
    COLD_STORAGE: Literal['none', 'gcs', 'firestore'] = os.getenv('COLD_STORAGE', 'none')
    
    # AI Settings
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    @classmethod
    def has_ai_enabled(cls) -> bool:
        """Check if AI is configured and available."""
        return bool(cls.GEMINI_API_KEY or cls.OPENAI_API_KEY)
    
    # Service Settings
    SERVICE_NAME: str = "Komfyrvakt"
    VERSION: str = "0.1.0"
    
    @classmethod
    def generate_api_key(cls) -> str:
        """Generate a new API key."""
        random_part = secrets.token_urlsafe(24)
        return f"{cls.API_KEY_PREFIX}{random_part}"
    
    @classmethod
    def validate_api_key(cls, key: str) -> bool:
        """Validate API key format and value."""
        if not key:
            return False
        if not key.startswith(cls.API_KEY_PREFIX):
            return False
        return key == cls.API_KEY
    
    @classmethod
    def ensure_api_key(cls) -> str:
        """
        Ensure API key exists. 
        If not set via environment, check .env file or generate and save new one.
        """
        if cls.API_KEY:
            return cls.API_KEY
        
        # Try to load from .env file (in Komfyrvakt root, not api/)
        env_file = os.path.join(os.path.dirname(__file__), '../..', '.env')
        
        if os.path.exists(env_file):
            # Load existing key from .env
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('KOMFYRVAKT_API_KEY='):
                        key = line.strip().split('=', 1)[1]
                        if key:
                            cls.API_KEY = key
                            print(f"✅ Loaded API key from .env")
                            return cls.API_KEY
        
        # Generate new key and save to .env
        cls.API_KEY = cls.generate_api_key()
        
        # Save to .env file
        with open(env_file, 'w') as f:
            f.write(f'# Komfyrvakt Configuration\n')
            f.write(f'KOMFYRVAKT_API_KEY={cls.API_KEY}\n')
            f.write(f'REDIS_HOST={cls.REDIS_HOST}\n')
            f.write(f'REDIS_PORT={cls.REDIS_PORT}\n')
            f.write(f'ENVIRONMENT={cls.ENVIRONMENT}\n')
        
        print("=" * 50)
        print("🔥 Komfyrvakt Started!")
        print("=" * 50)
        print(f"✅ Generated new API key: {cls.API_KEY}")
        print(f"✅ Saved to .env file")
        print("=" * 50)
        
        return cls.API_KEY


# Global settings instance
settings = Settings()

