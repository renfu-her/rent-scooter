from app import create_app, socketio
from flask_migrate import Migrate
from app.models import db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=8000)

