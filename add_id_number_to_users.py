"""
Add id_number column to users table
Run this script to add the id_number column to the users table
"""
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    try:
        # Check if column already exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'id_number' in columns:
            print('Column id_number already exists in users table')
        else:
            # Add column using raw SQL
            db.engine.execute(db.text('ALTER TABLE users ADD COLUMN id_number VARCHAR(20) NULL'))
            print('Successfully added id_number column to users table')
    except Exception as e:
        print(f'Error: {e}')
        print('Please run the following SQL manually:')
        print('ALTER TABLE users ADD COLUMN id_number VARCHAR(20) NULL;')

