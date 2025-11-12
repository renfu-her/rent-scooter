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
    def create(name, address=None, phone=None, partner_id=None, image_path=None):
        """Create a new store"""
        store = Store(name=name, address=address, phone=phone, partner_id=partner_id, image_path=image_path)
        db.session.add(store)
        db.session.commit()
        return store
    
    @staticmethod
    def update(store_id, name=None, address=None, phone=None, partner_id=None, image_path=None):
        """Update store"""
        store = Store.query.get_or_404(store_id)
        if name:
            store.name = name
        if address is not None:
            store.address = address
        if phone is not None:
            store.phone = phone
        if partner_id is not None:
            store.partner_id = partner_id
        if image_path is not None:
            store.image_path = image_path
        db.session.commit()
        return store
    
    @staticmethod
    def delete(store_id):
        """Delete store"""
        store = Store.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

