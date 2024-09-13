
import pytest
import json
from app import create_app
from weather_app.db import db
from weather_app.models import City, WeatherRequestLog
from weather_app.services.weather_api_service import WeatherApiService


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_weather_api(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({
            "location": {"name": "New York", "country": "USA"},
            "current": {
                "temp_c": 20, "temp_f": 68,
                "condition": {"text": "Sunny"}
            }
        }, 200)

    monkeypatch.setattr("requests.get", mock_get)


def test_list_cities(client, app):
    with app.app_context():
        city = City(name="New York", lat=40.7128, long=-74.0060)
        db.session.add(city)
        db.session.commit()

    response = client.get('/list-cities')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['name'] == "New York"


def test_get_weather(client, app, mock_weather_api):
    with app.app_context():
        city = City(name="New York", lat=40.7128, long=-74.0060)
        db.session.add(city)
        db.session.commit()

        # Re-query the city to reattach it to the session
        city = City.query.filter_by(name="New York").first()

    response = client.get(f'/weather?city_id={city.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] is True
    assert data['data']['city'] == "New York"
    assert 'temperature' in data['data']


def test_weather_logs(client, app):
    with app.app_context():
        city = City(name="New York", lat=40.7128, long=-74.0060)
        db.session.add(city)
        db.session.commit()

        log = WeatherRequestLog(city_id=city.id, response_status="success", response_data='{"temp": 20}')
        db.session.add(log)
        db.session.commit()

    response = client.get('/weather-logs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['city_name'] == "New York"


def test_weather_api_service(app, mock_weather_api):
    with app.app_context():
        city = City(name="New York", lat=40.7128, long=-74.0060)
        db.session.add(city)
        db.session.commit()

        service = WeatherApiService()
        result, error = service.get_weather_by_city_id(city.id)
        assert error is None
        assert result['city'] == "New York"
        assert 'temperature' in result