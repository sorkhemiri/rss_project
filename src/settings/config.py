from pydantic import BaseSettings


class Config(BaseSettings):
    debug: bool = True
    app_title: str = "CORE"

    class Config:
        case_sensitive = False
        env_file = "../.env"
        env_file_encoding = "utf-8"


env_config = Config()
