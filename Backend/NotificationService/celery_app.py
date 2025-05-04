from celery import Celery

celery_app = Celery(
    "notification_service",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# Таймзона
celery_app.conf.timezone ="UTC"

# Оптимизация памяти и работы worker-ов
celery_app.conf.worker_max_tasks_per_child = 10           # перезапуск worker после 10 задач (борьба с утечками памяти)
celery_app.conf.worker_prefetch_multiplier = 1            # отключает предзагрузку задач (экономит RAM)
celery_app.conf.worker_concurrency = 2                    # число процессов воркера (меньше — меньше памяти)
celery_app.conf.task_acks_late = True                     # подтверждение задачи только после выполнения
celery_app.conf.task_ignore_result = True                 # не сохранять результат (если он не нужен)
celery_app.conf.result_backend = None                     # полностью отключить хранение результатов (если не нужны)

# Авто-дискавер тасков
celery_app.autodiscover_tasks(["tasks"])
