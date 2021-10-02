from celery import Celery
from settings.config import env_config
from celery_config import CELERY_CONFIG


celery_app = Celery('celery_app', broker='redis://{}:{}/{}'.format(env_config.redis_host, env_config.redis_port, 5))
celery_app.conf.update(CELERY_CONFIG)
