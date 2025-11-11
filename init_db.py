from app import create_app, db
from app.models.user import User
import os

app = create_app()

with app.app_context():
    # Create upload directories
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'motorcycles'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'banners'), exist_ok=True)
    print('Upload directories created')
    
    # Create database tables
    db.create_all()
    
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

