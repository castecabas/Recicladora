# gunicorn.conf.py

# Número de workers (ajusta según los recursos disponibles)
workers = 2

# Tipo de worker (sync es el predeterminado)
worker_class = "sync"

# Tiempo de espera para cada solicitud (en segundos)
timeout = 120

# Límite de solicitudes por worker antes de reiniciarlo
max_requests = 1000
max_requests_jitter = 50