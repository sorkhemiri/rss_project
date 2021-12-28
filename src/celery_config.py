import os

CELERY_QUEUE = os.getenv("CELERY_QUEUE", "rss_streamer")

CELERY_CONFIG = {
    "imports": {
        "utils.jobs",
    },
    "include": {
        "utils.jobs",
    },
    "task_routes": {
        "utils.jobs.*": {"queue": CELERY_QUEUE},
    },
    "task_default_queue": CELERY_QUEUE,
    "timezone": "Asia/Tehran",
    "worker_max_tasks_per_child": 1,
    "redis_max_connections": 16,
    "broker_transport_options": {"max_connections": 16},
    "redis_retry_on_timeout": True,
    "accept_content": ["pickle", "json", "msgpack", "yaml"],
    "task_serializer": "pickle",
    "beat_schedule": {
        "stream-job": {
            "task": "utils.jobs.add_from_stream.add_from_stream",
            "schedule": 60 * 2,
        },
    },
}
