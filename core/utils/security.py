from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)

def verify_password(plain_passwrod: str, password_hash: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_passwrod, password_hash)