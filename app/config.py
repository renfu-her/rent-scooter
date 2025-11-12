import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root@localhost/rent-scooter'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    TIMEZONE = 'Asia/Taipei'  # 時區設定
    
    # Flask-Caching configuration
    CACHE_TYPE = 'SimpleCache'  # 使用内存缓存，生产环境可改为 RedisCache
    CACHE_DEFAULT_TIMEOUT = 300  # 默认缓存时间5分钟
    
    # Flask-Compress configuration
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6  # 压缩级别 1-9，6是平衡性能和压缩率的好选择
    COMPRESS_MIN_SIZE = 500  # 只压缩大于500字节的响应

