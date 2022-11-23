from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenBase(BaseModel):
    refresh_token: str
    token_type: str = "Bearer"

