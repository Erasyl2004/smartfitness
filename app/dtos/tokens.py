from pydantic import BaseModel

class RefreshTokenInDTO(BaseModel):
    refresh_token: str

class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"