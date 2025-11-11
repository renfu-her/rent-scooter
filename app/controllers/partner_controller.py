from app.models import db
from app.models.partner import Partner


class PartnerController:
    @staticmethod
    def get_all():
        """Get all partners"""
        return Partner.query.all()
    
    @staticmethod
    def get_by_id(partner_id):
        """Get partner by ID"""
        return Partner.query.get_or_404(partner_id)
    
    @staticmethod
    def create(name, address=None, tax_id=None):
        """Create a new partner"""
        partner = Partner(name=name, address=address, tax_id=tax_id)
        db.session.add(partner)
        db.session.commit()
        return partner
    
    @staticmethod
    def update(partner_id, name=None, address=None, tax_id=None):
        """Update partner"""
        partner = Partner.query.get_or_404(partner_id)
        if name:
            partner.name = name
        if address is not None:
            partner.address = address
        if tax_id is not None:
            partner.tax_id = tax_id
        db.session.commit()
        return partner
    
    @staticmethod
    def delete(partner_id):
        """Delete partner"""
        partner = Partner.query.get_or_404(partner_id)
        db.session.delete(partner)
        db.session.commit()

