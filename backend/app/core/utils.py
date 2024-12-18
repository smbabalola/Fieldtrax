from datetime import datetime, timezone
from  sqlalchemy import DateTime
import uuid
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated='auto')

class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    
    def verify(plain_password, hashed_password):
        return pwd_cxt.verify(plain_password, hashed_password)

def generate_uuid():
    return str(uuid.uuid4())

def utcnow():
    return datetime.now(timezone.utc)
