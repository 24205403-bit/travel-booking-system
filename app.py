from flask import Flask
from config import DevelopmentConfig
from models import init_db
from routes import register_blueprints
from models.package_type import PackageType

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize MongoDB connection
    init_db(app)

    # Seed default package types if none exist
    PackageType.seed_defaults()

    # Register Blueprint routes
    register_blueprints(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
