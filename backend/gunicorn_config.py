import multiprocessing
import os

# 确保日志目录存在
os.makedirs('/var/log/pyq', exist_ok=True)

# 监听地址和端口
bind = "0.0.0.0:8000"

# 工作进程数 - 根据2核CPU优化
workers = 3  # 2 * CPU核心数 + 1

# 工作模式
worker_class = 'gevent'

# 每个工作进程的并发量
worker_connections = 500

# 进程名称
proc_name = 'pyq'

# 进程pid记录路径
pidfile = '/var/run/pyq/gunicorn.pid'

# 日志配置
accesslog = '/var/log/pyq/access.log'
errorlog = '/var/log/pyq/error.log'
loglevel = 'info'

# 不作为守护进程运行，交给systemd管理
daemon = False

# 优雅重启时间
graceful_timeout = 30

# 请求超时时间
timeout = 30

# 最大并发请求数
max_requests = 1000
max_requests_jitter = 100

# 预加载应用
preload_app = True

# 用户组配置
user = os.getenv('USER')
group = os.getenv('USER')

# 工作模式配
worker_tmp_dir = '/dev/shm'  # 使用内存文件系统
threads = multiprocessing.cpu_count() * 2  # 每个工作进程的线程数 