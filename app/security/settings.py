from pydantic import BaseModel
from dotenv import load_dotenv
import os
import base64

load_dotenv()

class AuthSettings(BaseModel):
    private_key: str = base64.b64decode(os.getenv("JWT_PRIVATE_KEY_64")).decode()
    public_key: str = base64.b64decode(os.getenv("JWT_PUBLIC_KEY_64")).decode()
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 30

settings = AuthSettings()