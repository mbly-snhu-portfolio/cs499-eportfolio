"""
Authentication service.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Initialize passwords - generate hashes at module load time
# Using a workaround to avoid bcrypt initialization issues
def _generate_password_hash(password: str) -> str:
    """Generate password hash, handling bcrypt initialization."""
    try:
        return pwd_context.hash(password)
    except (ValueError, AttributeError):
        # Fallback: use bcrypt directly if passlib has issues
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Mock user database (in production, use real database)
USERS_DB = {
    "admin": {
        "id": "1",
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": None,  # Will be initialized on first access
        "role": "admin",
        "is_active": True
    },
    "user": {
        "id": "2",
        "username": "user",
        "email": "user@example.com",
        "hashed_password": None,  # Will be initialized on first access
        "role": "user",
        "is_active": True
    }
}

# Initialize passwords on first use
def _init_passwords():
    """Initialize password hashes if not already set."""
    if USERS_DB["admin"]["hashed_password"] is None:
        USERS_DB["admin"]["hashed_password"] = _generate_password_hash("admin123")
    if USERS_DB["user"]["hashed_password"] is None:
        USERS_DB["user"]["hashed_password"] = _generate_password_hash("user123")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, AttributeError):
        # Fallback: use bcrypt directly if passlib has issues
        import bcrypt
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def get_user(username: str) -> Optional[dict]:
    """Get user by username."""
    _init_passwords()  # Ensure passwords are initialized
    return USERS_DB.get(username)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate a user."""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    if not user.get("is_active", True):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Get current authenticated user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Get current active user."""
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: dict = Depends(get_current_active_user)) -> dict:
    """Get current admin user."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

