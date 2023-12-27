from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password: str):
    
    return pwd_context.hash(password)

def verifyPassword(new_password: str, password: str):
    
    return pwd_context.verify(new_password, password)