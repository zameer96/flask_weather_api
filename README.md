# Flask Weather API

A simple Flask-based API for retrieving weather information for various cities.

## Setup

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_APP_DATABASE_URL=sqlite:///weather_app_db.db
WEATHER_APP_API_KEY=xxxxxxxxx
```

Replace `xxxxxxxxx` with your actual weather API key.

### Database Setup

Run migrations to set up the database:

```bash
flask db upgrade
```

### Running the Application

Start the Flask application:

```bash
flask run
```

## API Endpoints

### Home
- **URL:** `/`
- **Method:** GET
- **Description:** Redirects to the list-cities endpoint.

### List Cities
- **URL:** `/list-cities`
- **Method:** GET
- **Description:** Returns a list of cities with their IDs and coordinates.
- **Response Example:**
  ```json
  {
    "count": 10,
    "data": [
      {
        "id": 1,
        "lat": 40.7128,
        "long": -74.006,
        "name": "New York"
      }
    ]
  }
  ```

### Weather for a City
- **URL:** `/weather`
- **Method:** GET
- **Parameters:** `city_id` (required)
- **Description:** Returns the current weather for the specified city.
- **Response Example:**
  ```json
  {
    "data": {
      "city": "Sydney",
      "country": "Australia",
      "last_updated": "2024-09-13 08:30",
      "temperature": {
        "celsius": 13.1,
        "fahrenheit": 55.6
      },
      "temperature_feels_like": {
        "celsius": 11,
        "fahrenheit": 51.8
      },
      "weather_description": "Partly cloudy",
      "wind_speed": {
        "kph": 25.9,
        "mph": 16.1
      }
    },
    "status": true
  }
  ```

### Weather Logs
- **URL:** `/weather-logs`
- **Method:** GET
- **Description:** Returns the latest 5 successful weather request logs.
- **Response Example:**
  ```json
  {
    "data": [
      {
        "city_name": "London",
        "id": 2,
        "response_data": {
          "city": "London",
          "country": "United Kingdom",
          "last_updated": "2024-09-12 23:30",
          "temperature": {
            "celsius": 6,
            "fahrenheit": 42.8
          },
          "temperature_feels_like": {
            "celsius": 3.8,
            "fahrenheit": 38.8
          },
          "weather_description": "Clear",
          "wind_speed": {
            "kph": 6.1,
            "mph": 3.8
          }
        },
        "response_status": "success",
        "timestamp": "Thu, 12 Sep 2024 18:45:38 GMT"
      }
    ],
    "status": true
  }
  ```

## Development

To run the application in debug mode, ensure that `FLASK_DEBUG=1` is set in your `.env` file.

## Database

The application uses SQLite as its database. The database file is located at `weather_app_db.db` in the root directory.

### Database Schema

The Flask Weather API uses SQLite as its database. The schema consists of two main tables: `City` and `WeatherRequestLog`.

#### City Table

The `City` table stores information about various cities.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier for each city |
| name | String(100) | Not Null | Name of the city |
| lat | Float | Not Null | Latitude of the city |
| long | Float | Not Null | Longitude of the city |


#### WeatherRequestLog Table

The `WeatherRequestLog` table stores the history of weather requests made through the API.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier for each log entry |
| city_id | Integer | Foreign Key (City.id) | References the City table |
| timestamp | DateTime | Default: Current time | When the request was made |
| response_status | String(20) | Not Null | Status of the API response |
| response_data | Text | | JSON response from the weather API (stored as text) |


#### Notes (Schema models)

1. The `WeatherRequestLog` model stores the entire JSON response from the weather API as text in the `response_data` column. This allows for flexibility in storing different response structures.

2. The `to_dict()` method in `WeatherRequestLog` can optionally include the weather data, transforming it using the `transform_weather_data()` function when the response status is successful.

3. For future improvements, consider creating a separate model for `response_data` and establishing a relationship with `WeatherRequestLog`. This would allow for easier management and potential periodic deletion of detailed response data while preserving request history.

4. The `City` model includes a `to_dict()` method for easy serialization of city data.

5. Both models use SQLAlchemy as the ORM (Object-Relational Mapping) tool, which provides an abstraction layer for database operations.

## API Key

Make sure to replace the placeholder API key in the `.env` file with a valid key for the weather service you're using.