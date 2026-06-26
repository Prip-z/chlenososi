import os
from typing import List, Dict
from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()

ENV_DATABASE_MAPPER: Dict[str, str] = {
    "prod": "forestmap",
    "stage": "forestmap",
    "dev": "forestmap",
    "test": "forestmap",
}

DB_ENGINE_MAPPER: Dict[str, str] = {
    "postgresql": "postgresql",
    "mysql": "mysql+pymysql",
}

class Configs(BaseSettings):
    ENV: str = "dev"  
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    PROJECT_NAME: str = "fca-api"
    
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    DB: str = "postgresql"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = ""
    
    DATABASE_URI: str = ""

    @validator("DB_PORT", pre=True, always=True)
    def assemble_db_port(cls, v, values):
        if v:
            return v
        return "5432" if values.get("DB") == "postgresql" else "3306"

    @validator("DATABASE_URI", pre=True, always=True)
    def assemble_db_connection(cls, v, values):
        if v:
            return v
            
        db = values.get("DB", "postgresql")
        engine = DB_ENGINE_MAPPER.get(db, "postgresql")
        user = values.get("DB_USER")
        password = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = values.get("DB_PORT")
        if not os.path.exists("/local_run_marker") and host == "postgres":
            if not os.path.exists("/.dockerenv"):
                host = "127.0.0.1"
        env = values.get("ENV", "dev")
        database = values.get("DB_NAME") or ENV_DATABASE_MAPPER.get(env, "forestmap")
        
        return f"{engine}://{user}:{password}@{host}:{port}/{database}"

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"

    class Config:
        case_sensitive = True
        env_file = ".env" 


configs = Configs()