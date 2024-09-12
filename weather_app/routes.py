from flask import Blueprint, request, url_for, redirect
from weather_app.services import WeatherApiService
from weather_app.models import City
from weather_app.db import db


routes = Blueprint('routes', __name__)

def generate_response(status, data=None, error_message=None, status_code=200, **kwargs):
    """
    Just to keep the response format consistent
    **kwargs to add more data in the response
    """
    response = {
        "status": status
    }
    if data:
        response["data"] = data
    if error_message:
        response["error"] = error_message
    if kwargs:
        response.update(kwargs)
    return response, status_code


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
        return generate_response(status=False,
                                 error_message=f"No cities found. Goto {populate_cities_url}",
                                 status_code=400)
    return generate_response(status=True, data=cities_list, status_code=200, count=count)


@routes.route('/weather')
def weather():
    """
    Return the weather data for the city (from API)
    requires GET param ?city_id=<id:int>
    """
    city_id = request.args.get('city_id')
    if not city_id:
        return {"status": False, "message": "City id is required"}, 400
    
    weather_api_service = WeatherApiService()
    res, error = weather_api_service.get_weather_by_city_id(city_id)
    if error:
        return generate_response(status=False, error_message=error, status_code=400)
    return generate_response(status=True, data=res, status_code=200)


@routes.route('/weather-logs')
def weather_logs():
    """
    List all the weather logs
    """

    weather_api_service = WeatherApiService()
    logs, _ = weather_api_service.get_weather_logs(include_weather_data=True)  # this would hardly give any errors as we are just fetching the logs
    return generate_response(status=True, data=logs, status_code=200)


# Just to populate the cities in the database
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
    return generate_response(status=True, message="Cities populated in Database successfully!", status_code=200)
