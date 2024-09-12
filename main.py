from flask import Flask
from app.db import db
from config import Config
from app.routes import routes as weather_routes 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init db 
    db.init_app(app)

    # import the weather blueprint
    app.register_blueprint(weather_routes)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create tables when the app
        db.create_all()
    app.run(debug=True)