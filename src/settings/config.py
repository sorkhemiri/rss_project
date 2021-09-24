from pydantic import BaseSettings


class Config(BaseSettings):
    debug: bool = True
    app_title: str = "CORE"
    SECRET_KEY: str = "eWaUa%ngb*9mrhoCGZ%g%wSwcF&mCtjVDoXD6FaHLdsS9D82HWNCrG&Zee^hF5K3"
    # redis host
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_user: str = "default"
    redis_password: str = "password"
    # postgres host
    postgres_user = "postgres"
    postgres_password = "password"
    postgres_db = "core_db"
    postgres_host = "127.0.0.1"
    postgres_port = 5432

    class Config:
        case_sensitive = False
        env_file = "../.env"
        env_file_encoding = "utf-8"


env_config = Config()
