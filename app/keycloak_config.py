import os
from dotenv import load_dotenv

load_dotenv()

# Keycloak configuration
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "cars-api")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-client")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
KEYCLOAK_ADMIN_USERNAME = os.getenv("KEYCLOAK_ADMIN_USERNAME", "admin")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD", "admin")

# JWT settings
JWT_ALGORITHM = "RS256"
JWT_ISSUER = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"

# Debug: Print configuration
print(f"Keycloak URL: {KEYCLOAK_URL}")
print(f"Keycloak Realm: {KEYCLOAK_REALM}")
print(f"JWT Issuer: {JWT_ISSUER}")
print(f"Client ID: {KEYCLOAK_CLIENT_ID}") 