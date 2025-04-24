from celery_app import celery_app
from tasks.notify import check_and_notify
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "notify-every-minute": {
        "task": "tasks.notify.check_and_notify",
        "schedule": crontab(),  # каждую минуту
    },
}
celery_app.conf.timezone = "UTC"
