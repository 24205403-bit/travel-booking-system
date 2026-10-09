from routes.main import main_bp
from routes.auth import auth_bp
from routes.destination import dest_bp
from routes.booking import booking_bp
from routes.payment import payment_bp
from routes.review import review_bp
from routes.admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dest_bp, url_prefix='/destinations')
    app.register_blueprint(booking_bp, url_prefix='/bookings')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(admin_bp, url_prefix='/admin')
