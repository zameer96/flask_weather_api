from flask import Blueprint, request, url_for, redirect
from weather_app.services import WeatherApiService
from weather_app.utils import generate_structured_response
from weather_app.models import City
from weather_app.db import db


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
        return generate_structured_response(status=False,
                                 error_message=f"No cities found. Goto {populate_cities_url}",
                                 status_code=400)
    return generate_structured_response(status=True, data=cities_list, status_code=200, count=count)


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
        return generate_structured_response(status=False, error_message=error, status_code=400)
    return generate_structured_response(status=True, data=res, status_code=200)


@routes.route('/weather-logs')
def weather_logs():
    """
    List all the weather logs
    """
    limit = request.args.get('limit', 5)  # Just giving an option to user to limit the logs

    weather_api_service = WeatherApiService()
    logs, _ = weather_api_service.get_weather_logs(include_weather_data=True, limit=limit)  # this would hardly give any errors as we are just fetching the logs
    count = len(logs)
    return generate_structured_response(status=True, data=logs, status_code=200, count=count)
