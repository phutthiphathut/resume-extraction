from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str

    CLIENT_ORIGIN_URL: str

    JWT_SECRET_KEY: str
    JWT_EXPIRE_MINUTES: int

    STORAGE_SPACE_NAME: str
    STORAGE_REGION: str 
    STORAGE_ACCESS_ID: str
    STORAGE_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file='.env')

appConfig = AppConfig()
