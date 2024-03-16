from pydantic import BaseModel


class TokensPair(BaseModel):
    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


# class Login(BaseModel):
#     username: str
#     password: str
