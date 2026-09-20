from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt

SECRET = "SECRET_KEY"
security = HTTPBearer()

def create_token(username, role):
    return jwt.encode({"user": username, "role": role}, SECRET, algorithm="HS256")

def verify_token(credentials=Depends(security)):
    token = credentials.credentials
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")

def get_role(user_data=Depends(verify_token)):
    return user_data["role"]