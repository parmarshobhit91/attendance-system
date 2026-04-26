from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    if not isinstance(password, str):
        raise ValueError("Password must be string")

    password = password.strip()

    if len(password) > 72:
        password = password[:72]
        
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)