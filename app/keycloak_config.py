import os
from dotenv import load_dotenv

load_dotenv()

# Keycloak configuration with security best practices
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_INTERNAL_URL = os.getenv("KEYCLOAK_INTERNAL_URL", "http://keycloak:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "cars-api")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-client")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

# JWT settings - HARDCODE to match the token issuer exactly
JWT_ALGORITHM = "RS256"
JWT_ISSUER = "http://localhost:8080/realms/cars-api"  # HARDCODED - must match token exactly
JWKS_URL = f"{KEYCLOAK_INTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"

# Security settings
TOKEN_VALIDATION_OPTIONS = {
    "verify_signature": True,
    "verify_exp": True,
    "verify_nbf": True,
    "verify_iat": True,
    "verify_aud": False,
    "require_exp": True,
    "require_iat": True,
    "require_nbf": True
}

# Debug output
print(f"Keycloak URL: {KEYCLOAK_URL}")
print(f"Keycloak Internal URL: {KEYCLOAK_INTERNAL_URL}")
print(f"JWT Issuer: {JWT_ISSUER}")