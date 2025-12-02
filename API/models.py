from pydantic import BaseModel


class NoResponse(BaseModel):
    pass


class LoginResponse(BaseModel):
    token: str
    expires: str
