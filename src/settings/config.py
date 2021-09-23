from pydantic import BaseSettings


class Config(BaseSettings):
    debug: bool = True
    app_title: str = "CORE"
    SECRET_KEY: str = "eWaUa%ngb*9mrhoCGZ%g%wSwcF&mCtjVDoXD6FaHLdsS9D82HWNCrG&Zee^hF5K3"

    class Config:
        case_sensitive = False
        env_file = "../.env"
        env_file_encoding = "utf-8"


env_config = Config()
