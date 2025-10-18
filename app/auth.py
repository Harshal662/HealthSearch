from fastapi import Header, HTTPException, Security
from app.config import settings

def get_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer" or parts[1] != settings.HEALTHSEARCH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True
