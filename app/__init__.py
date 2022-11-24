from flask import Flask
from app.models import db
from app.ui.routes import ui_bp


def create_app():
    # Create Flask App
    app = Flask(__name__)
    app.config.from_object('config')
    # Initialise extensions
    db.init_app(app)
    with app.app_context():
        from app.ui import routes
        app.register_blueprint(ui_bp)
        # Create sql tables for data models
        db.create_all()
    return app


