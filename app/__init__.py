from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from app.config import Config
from app.models import db
from app.models.user import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '請先登入以繼續'
login_manager.login_message_category = 'info'

socketio = SocketIO(cors_allowed_origins="*")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    
    # Register blueprints
    from app.views.auth import auth_bp
    from app.views.frontend import frontend_bp
    from app.views.backend import backend_bp
    from app.views.admin.users import admin_users_bp
    from app.views.admin.partners import admin_partners_bp
    from app.views.admin.stores import admin_stores_bp
    from app.views.admin.motorcycles import admin_motorcycles_bp
    from app.views.admin.orders import admin_orders_bp
    from app.views.admin.banners import admin_banners_bp
    from app.views.api.partners import api_partners_bp
    from app.views.api.stores import api_stores_bp
    from app.views.api.motorcycles import api_motorcycles_bp
    from app.views.api.orders import api_orders_bp
    from app.views.api.banners import api_banners_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(frontend_bp)
    app.register_blueprint(backend_bp, url_prefix='/backend')
    app.register_blueprint(admin_users_bp, url_prefix='/backend/users')
    app.register_blueprint(admin_partners_bp, url_prefix='/backend/partners')
    app.register_blueprint(admin_stores_bp, url_prefix='/backend/stores')
    app.register_blueprint(admin_motorcycles_bp, url_prefix='/backend/motorcycles')
    app.register_blueprint(admin_orders_bp, url_prefix='/backend/orders')
    app.register_blueprint(admin_banners_bp, url_prefix='/backend/banners')
    app.register_blueprint(api_partners_bp, url_prefix='/api/partners')
    app.register_blueprint(api_stores_bp, url_prefix='/api/stores')
    app.register_blueprint(api_motorcycles_bp, url_prefix='/api/motorcycles')
    app.register_blueprint(api_orders_bp, url_prefix='/api/orders')
    app.register_blueprint(api_banners_bp, url_prefix='/api/banners')
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Register WebSocket event handlers
    from app.utils.websocket_events import register_websocket_events
    register_websocket_events(socketio)
    
    return app

