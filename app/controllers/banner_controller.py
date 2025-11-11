from app.models import db
from app.models.banner import Banner


class BannerController:
    @staticmethod
    def get_all():
        """Get all banners"""
        return Banner.query.order_by(Banner.display_order, Banner.created_at.desc()).all()
    
    @staticmethod
    def get_active():
        """Get active banners"""
        return Banner.query.filter_by(is_active=True).order_by(Banner.display_order).all()
    
    @staticmethod
    def get_by_id(banner_id):
        """Get banner by ID"""
        return Banner.query.get_or_404(banner_id)
    
    @staticmethod
    def create(title, image_path, link_url=None, display_order=0, is_active=True):
        """Create a new banner"""
        banner = Banner(
            title=title,
            image_path=image_path,
            link_url=link_url,
            display_order=display_order,
            is_active=is_active
        )
        db.session.add(banner)
        db.session.commit()
        return banner
    
    @staticmethod
    def update(banner_id, title=None, image_path=None, link_url=None,
               display_order=None, is_active=None):
        """Update banner"""
        banner = Banner.query.get_or_404(banner_id)
        if title:
            banner.title = title
        if image_path:
            banner.image_path = image_path
        if link_url is not None:
            banner.link_url = link_url
        if display_order is not None:
            banner.display_order = display_order
        if is_active is not None:
            banner.is_active = is_active
        db.session.commit()
        return banner
    
    @staticmethod
    def delete(banner_id):
        """Delete banner"""
        banner = Banner.query.get_or_404(banner_id)
        db.session.delete(banner)
        db.session.commit()

