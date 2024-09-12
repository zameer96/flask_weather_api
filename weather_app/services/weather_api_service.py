import json
import requests
from flask import current_app
from sqlalchemy import asc, desc
from weather_app.services.serializers import transform_weather_data
from weather_app.models import City, WeatherRequestLog
from weather_app.db import db


class WeatherApiService:
    
    _WEATHER_API_KEY = None
    _WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"
    
    ERROR_MESSAGES = {
        "default": "An error occurred while fetching the weather data",
        "city_not_found": "City does not exists in the database",
        "all_fields_required": "All fields are required"
    }
    
    def __init__(self):
        self._WEATHER_API_KEY = current_app.config["WEATHER_API_KEY"]

    
    def save_weather_request_log(self, city_id, response_status, response_data):
        """
        Save the weather request log
        """
        if not all([city_id, response_status, response_data]):
            return None, self.ERROR_MESSAGES["all_fields_required"]
        
        # transform data to string (mostly if it's a dict)
        if response_data and isinstance(response_data, dict):
            response_data = json.dumps(response_data)
        
        weather_request_log = WeatherRequestLog(city_id=city_id, response_status=response_status, response_data=response_data)
        db.session.add(weather_request_log)
        db.session.commit()
        return weather_request_log, None
    
    def get_weather_by_city_id(self, city_id):
        """
        Get weather by city name
            input: city_name
            output: response(dict), error(str)
        
        This method fetches weather data and then saves the response in WeatherRequestLog table
        """
        print("API_KEY --->", self._WEATHER_API_KEY)
        response_status = None
        results = None
        error_msg = None
        
        city = City.query.filter_by(id=city_id).first()
        if not city:
            return None, self.ERROR_MESSAGES["city_not_found"]
        
        endpoint = f"{self._WEATHER_API_URL}?key={self._WEATHER_API_KEY}&q={city.name}"
        print("ENDPOINT --->", endpoint)
        response = requests.get(endpoint)
        if response.status_code != 200:
            response_status = "failed"
            try:
                response_data = response.json()
            except:
                response_data = response.text
            error_msg = self.ERROR_MESSAGES["default"]
        else:
            response_status = "success"
            response_data = response.json()
            results = transform_weather_data(response_data)
            # results = self.filter_weather_api_response(response_data)
            
        self.save_weather_request_log(city_id, response_status, response_data)
        return results, error_msg
    
    def get_weather_logs(self, limit=5, include_weather_data=False, filter_repsonse_status=None):
        """
        Get all the weather logs
        """
        filter_query = {}
        if filter_repsonse_status:
            filter_query["response_status"] = filter_repsonse_status
            
        logs = WeatherRequestLog.query.filter_by(**filter_query).order_by(WeatherRequestLog.timestamp.desc()).limit(limit).all()
        logs_list = [log.to_dict(include_weather_data=include_weather_data) for log in logs]
        return logs_list, None  # No error msg
    
    def filter_weather_api_response(self, response_dict):
        """
        Filter the weather API response
        input: response_dict(dict)
        output: filtered_dict(dict)
        """
        location = response_dict["location"]
        current = response_dict["current"]
        
        filtered_dict = {
            "city": location['name'],
            "country": location['country'],
            "weather_description": current['condition']['text'],
            "temperature": {
                "celsius": current['temp_c'],
                "fahrenheit": current['temp_f']
            },
            "temperature_feels_like": {
                "celcius": current['feelslike_c'],
                "fahrenheit": current['feelslike_f']
            },
            "wind_speed": {
                "kph": current['wind_kph'],
                "mph": current['wind_mph']
            },
            "last_updated": current['last_updated']
        }
        return filtered_dict
    
    