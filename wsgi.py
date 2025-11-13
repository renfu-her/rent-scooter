from app import create_app, socketio
from flask_migrate import Migrate
from app.models import db

# Create Flask application instance
app = create_app()
migrate = Migrate(app, db)

# WSGI application entry point
application = app

if __name__ == '__main__':
    # Run with auto-reload and debug mode
    socketio.run(app, debug=True, host='127.0.0.1', port=8000, use_reloader=True)
