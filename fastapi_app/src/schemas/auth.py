from pydantic import Field, BaseModel

ACCESS_TOKEN = "JWT токен доступа"
TOKEN_TYPE = "Тип токена (bearer)"
USERNAME = "Имя пользователя"
PASSWORD = "Пароль пользователя"
REFRESH_TOKEN = "Refresh токен для обновления access_token"


class Token(BaseModel):
    access_token: str = Field(description=ACCESS_TOKEN)
    token_type: str = Field(description=TOKEN_TYPE)


class TokenData(BaseModel):
    user_id: int
    username: str
    is_superuser: bool = False
    is_staff: bool = False


class LoginRequest(BaseModel):
    username: str = Field(description=USERNAME)
    password: str = Field(description=PASSWORD)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(description=REFRESH_TOKEN)