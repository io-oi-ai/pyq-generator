import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
timeout = 120
keepalive = 5

# 日志设置
accesslog = "/var/log/pyq/access.log"
errorlog = "/var/log/pyq/error.log"
loglevel = "info"

# 进程名称
proc_name = "pyq_gunicorn"

# 工作模式
daemon = False

# 其他设置
reload = True
preload_app = True 