def transform_weather_data(api_response):
    """
    tansform the API response data into the required format.
        api_response: dict: API response from the weather API
        return: transformed dict
    """
    # Extract relevant data from the API response
    location = api_response.get('location', {})
    current = api_response.get('current', {})

    # Create transformed data
    transformed_data = {
        "city": location.get('name', ''),
        "country": location.get('country', ''),
        "last_updated": current.get('last_updated', ''),
        "temperature": {
            "celsius": current.get('temp_c', 0.0),
            "fahrenheit": current.get('temp_f', 0.0)
        },
        "temperature_feels_like": {
            "celsius": current.get('feelslike_c', 0.0),
            "fahrenheit": current.get('feelslike_f', 0.0)
        },
        "weather_description": current.get('condition', {}).get('text', ''),
        "wind_speed": {
            "kph": current.get('wind_kph', 0.0),
            "mph": current.get('wind_mph', 0.0)
        }
    }

    return transformed_data
