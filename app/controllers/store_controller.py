from app.models import db
from app.models.store import Store


class StoreController:
    @staticmethod
    def get_all():
        """Get all stores"""
        return Store.query.all()
    
    @staticmethod
    def get_by_id(store_id):
        """Get store by ID"""
        return Store.query.get_or_404(store_id)
    
    @staticmethod
    def create(name, address=None, phone=None):
        """Create a new store"""
        store = Store(name=name, address=address, phone=phone)
        db.session.add(store)
        db.session.commit()
        return store
    
    @staticmethod
    def update(store_id, name=None, address=None, phone=None):
        """Update store"""
        store = Store.query.get_or_404(store_id)
        if name:
            store.name = name
        if address is not None:
            store.address = address
        if phone is not None:
            store.phone = phone
        db.session.commit()
        return store
    
    @staticmethod
    def delete(store_id):
        """Delete store"""
        store = Store.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

