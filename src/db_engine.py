from tortoise import Tortoise, run_async

from settings import env_config


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    db_config = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "database": env_config.postgres_db,
                    "host": env_config.postgres_host,
                    "password": env_config.postgres_password,
                    "port": env_config.postgres_port,
                    "user": env_config.postgres_user,
                    "maxsize": env_config.postgres_max_connections,
                },
            }
        },
        "apps": {
            "models": {
                "models": ["models"],
                "default_connection": "default",
            }
        },
    }
    print(db_config)
    await Tortoise.init(config=db_config)
    # Generate the schema


run_async(init())
