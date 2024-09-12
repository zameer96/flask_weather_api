from flask import Blueprint, request, jsonify, url_for, redirect
from app.services.weather_service import WeatherApiService
from app.models import City, db

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET'])
def index():
    """
    redirect to list-cities
    """
    return redirect(url_for('routes.list_cities'))

@routes.route('/list-cities', methods=['GET'])
def list_cities():
    """
    List all the cities in the database
    response: [{"id": 1, "lat": 40.7128, "long": -74.006, "name": "New York"}]
    """
    cities = City.query.all()
    cities_list = [city.to_dict() for city in cities]
    count = len(cities_list)
    if not cities_list:
        populate_cities_url = url_for('routes.populate_cities', _external=True)
        return {"message": f"No cities found. Goto {populate_cities_url}"}, 400
    
    return {"status": True,
            "count": count,
            "data": cities_list}, 200


@routes.route('/weather')
def weather():
    """
    Return the weather data for the city (from API)
    requires GET param ?city_id=<id:int>
    """
    city_id = request.args.get('city_id')
    if not city_id:
        return {"status": False, "message": "City id is required"}, 400
    
    weather_api = WeatherApiService()
    res, error = weather_api.get_weather_by_city_id(city_id)
    if error:
        return {"status": False, "message": error}, 400
    return {"status": True, "data": res}



@routes.route('/populate-cities', methods=['GET'])
def populate_cities():
    """
    Endpoint to populate the cities in the database
    Ideally, this should be a one-time operation
    """
    cities = [
        {"name": "New York", "lat": 40.7128, "long": -74.0060},
        {"name": "London", "lat": 51.5074, "long": -0.1278},
        {"name": "Tokyo", "lat": 35.6762, "long": 139.6503},
        {"name": "Paris", "lat": 48.8566, "long": 2.3522},
        {"name": "Sydney", "lat": -33.8688, "long": 151.2093},
        {"name": "Berlin", "lat": 52.5200, "long": 13.4050},
        {"name": "Moscow", "lat": 55.7558, "long": 37.6173},
        {"name": "Calgary", "lat": 51.0447, "long": -114.0719},
        {"name": "Waterloo", "lat": 43.4643, "long": -80.5204},
        {"name": "Edmonton", "lat": 53.5461, "long": -113.4938}
    ]
    
    for city_data in cities:
        city = City.query.filter_by(name=city_data['name']).first()
        if not city:
            new_city = City(name=city_data['name'], lat=city_data['lat'], long=city_data['long'])
            db.session.add(new_city)
    
    db.session.commit()
    return {"status": True,
            "message": "Cities populated successfully"}, 200
