from tortoise import Tortoise, run_async

from settings import env_config


async def generate_schemas():
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

    await Tortoise.init(config=db_config)
    await Tortoise.generate_schemas()


run_async(generate_schemas())
