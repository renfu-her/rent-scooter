from app import create_app, db
from app.models.user import User
import os
import pymysql

app = create_app()

with app.app_context():
    # Create upload directories
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'motorcycles'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'banners'), exist_ok=True)
    print('Upload directories created')
    
    # Try to create database if it doesn't exist
    try:
        # Connect to MySQL without specifying database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
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

