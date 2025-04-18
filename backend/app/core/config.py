# App configuration and environment variables
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "SceneScopeAI"
    upload_dir: str = "app/static/uploads"
    model_dir: str = "app/static/models"


settings = Settings()
