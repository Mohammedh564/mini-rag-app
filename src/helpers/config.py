from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    model_config = SettingsConfigDict(env_file=".env")
    FILE_ALLOWED_TYPES :list
    FILE_MAX_SIZE : int
    FILE_DEFAULT_CHUNK_SIZE : int 

    MONGODB_URL : str
    MONGODB_DATABASE : str

def get_settings():
    return Settings()