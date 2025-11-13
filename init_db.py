from app import create_app, db
from app.models.user import User
import os
import pymysql
from urllib.parse import urlparse, unquote

app = create_app()

def parse_database_url(db_url):
    """Parse DATABASE_URL to extract connection parameters."""
    # Format: mysql+pymysql://user:password@host:port/database
    parsed = urlparse(db_url)
    
    return {
        'user': parsed.username or 'root',
        'password': unquote(parsed.password) if parsed.password else '',
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 3306,
        'database': parsed.path.lstrip('/') if parsed.path else None
    }

with app.app_context():
    # Create upload directories
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'motorcycles'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'banners'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'stores'), exist_ok=True)
    print('Upload directories created')
    
    # Try to create database if it doesn't exist
    try:
        # Parse DATABASE_URL to get connection parameters
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        db_params = parse_database_url(db_url)
        
        # Connect to MySQL without specifying database
        connection = pymysql.connect(
            host=db_params['host'],
            port=db_params['port'],
            user=db_params['user'],
            password=db_params['password'],
            charset='utf8mb4'
        )
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS `rent-scooter` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print('Database created or already exists')
        connection.close()
    except Exception as e:
        print(f'Warning: Could not create database automatically: {e}')
        print('Please create the database manually: CREATE DATABASE `rent-scooter` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
    
    # Create database tables
    try:
        db.create_all()
        print('Database tables created')
    except Exception as e:
        print(f'Error creating tables: {e}')
        print('Please ensure the database exists and MySQL is running')
        raise
    
    # Create admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            user_type='admin',
            is_active=True
        )
        admin.set_password('admin123')  # Change this in production!
        db.session.add(admin)
        db.session.commit()
        print('Admin user created: username=admin, password=admin123')
    else:
        print('Admin user already exists')
    
    print('\n✓ Database initialization completed!')
    print('You can now start the application with: uv run python run.py')

