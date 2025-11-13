"""
OAuth authentication for Cloud Control Center
"""

import os
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv

# Load .env file from project root
project_root = os.path.join(os.path.dirname(__file__), '..')
env_path = os.path.join(project_root, '.env')
print(f"Looking for .env at: {os.path.abspath(env_path)}")
load_dotenv(env_path)

# Session configuration
SESSION_SECRET = os.getenv('SESSION_SECRET', 'dev-secret-change-in-production')

# Check if OAuth credentials exist
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

if not client_id or not client_secret:
    print("WARNING: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not found in .env")
    print(f".env file exists: {os.path.exists(env_path)}")
    if os.path.exists(env_path):
        with open(env_path) as f:
            print(f".env contents preview: {f.read()[:100]}")

# OAuth configuration
oauth = OAuth()

oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

print(f"OAuth configured with Client ID: {client_id}")

