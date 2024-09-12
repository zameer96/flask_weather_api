from app.db import db
from datetime import datetime

class City(db.Model):
    """
    City model to store the city details 
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<City {self.name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "long": self.long
        }
        
class WeatherRequestLog(db.Model):
    """
    Model to store the weather request history
    
    response_data: JSON response from the weather API
        We can filter the json response to show only the required fields
        
    advacement: 
        We can create new model for response_data to store it separately
        and then use a relationship to connect it with the WeatherRequestLog model
        **We can delete the response_data periodically to save space
        meanwhile preserving the response_status history
    """
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    response_status = db.Column(db.String(20), nullable=False)
    response_data = db.Column(db.Text)  # save json response as text
    
    