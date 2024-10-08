import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from flask_migrate import Migrate
from config import Config
from weather_app.db import db as weather_db
from weather_app.routes import routes as weather_routes

def create_app(app_name=__name__):
    app = Flask(app_name)
    app.config.from_object(Config)

    # init db 
    weather_db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, weather_db)

    # import the weather blueprint
    app.register_blueprint(weather_routes)
    
    return app

app = create_app()

if __name__ == '__main__':        
    app.run(debug=True)