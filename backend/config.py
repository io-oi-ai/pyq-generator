import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基础配置
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = '/var/log/pyq/app.log'
    
    # Redis配置（用于缓存）
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # 安全配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # API限流配置
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100/hour')

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///dev.db'
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    # 生产环境特定配置
    LOG_LEVEL = 'WARNING'
    
    # 使用更安全的会话配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600
    
    # 启用SSL
    SSL_REDIRECT = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    LOG_LEVEL = 'DEBUG'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# 获取当前配置
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default']) 