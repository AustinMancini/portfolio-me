import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from config import SUPABASE_JWT_SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Token endpoint

# Get current user and token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        role = payload.get("user_role") # Custom claim from Supabase
        if not user_id or not role:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "role": role}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def require_subscriber(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "subscriber":
        raise HTTPException(status_code=403, detail="Subscriber access required")
    return current_user