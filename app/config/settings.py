from pydantic_settings import BaseSettings


class JWT(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


class Yandex(BaseSettings):
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str


class Settings(
    Yandex,
    JWT
):
    ...


settings = Settings()
