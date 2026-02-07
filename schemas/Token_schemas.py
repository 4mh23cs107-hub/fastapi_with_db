from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    email: str
    password: str
