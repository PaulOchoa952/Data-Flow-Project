from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import httpx
import logging
from .keycloak_config import KEYCLOAK_INTERNAL_URL, KEYCLOAK_REALM, JWT_ALGORITHM, JWT_ISSUER

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBearer()

class KeycloakAuthError(Exception):
    """Custom exception for Keycloak authentication errors"""
    pass

async def fetch_jwks() -> dict:
    """Fetch JWKS from Keycloak using internal URL"""
    jwks_url = f"{KEYCLOAK_INTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
    try:
        logger.info(f"Fetching JWKS from: {jwks_url}")
        async with httpx.AsyncClient() as client:
            response = await client.get(jwks_url, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch JWKS: {str(e)}")
        raise KeycloakAuthError(f"JWKS fetch failed: {str(e)}")

async def get_signing_key(token: str) -> str:
    """Get the appropriate signing key for the token"""
    try:
        # Fetch JWKS
        jwks = await fetch_jwks()
        
        # Get the key ID from the token header
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        
        # Find the matching key
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return key
                
        raise KeycloakAuthError(f"No matching key found for kid: {kid}")
    except Exception as e:
        logger.error(f"Signing key resolution failed: {str(e)}")
        raise KeycloakAuthError(f"Key resolution failed: {str(e)}")

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token from Keycloak with proper validation"""
    try:
        token = credentials.credentials
        
        logger.info(f"Token verification started (length: {len(token)})")
        
        # Get the appropriate signing key
        signing_key = await get_signing_key(token)
        logger.info(f"Using signing key with kid: {signing_key.get('kid')}")
        
        # Verify the token with minimal required claims (remove audience check)
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
            options={
                "verify_aud": False,  # Disable audience verification
                "verify_iss": True,
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
            }
        )
        
        logger.info("Token verified successfully")
        return payload
        
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except KeycloakAuthError as e:
        logger.error(f"Authentication service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        )
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication",
        )

def require_role(role: str):
    """Decorator to require a specific role with improved error handling"""
    def role_checker(token_payload: dict = Depends(verify_token)):
        try:
            if not token_payload.get("realm_access", {}).get("roles"):
                logger.warning("No roles found in token")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No roles assigned to user",
                )
            
            if role not in token_payload["realm_access"]["roles"]:
                logger.warning(f"User missing required role: {role}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required role '{role}' not assigned",
                )
            
            return token_payload
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Role verification failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during authorization",
            )
    return role_checker