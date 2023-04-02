import pytest
import requests
import json


class Test_basic:
    def test_establish_connection(self):
        response = requests.get("http://localhost:8000/")
        assert response.ok, "Connection to REST API failed"
        
    def test_get_plant_list(self):
        response = requests.get("http://localhost:8000/api/v1/plant_list")
        assert response.status_code >= 200 and response.status_code < 300,\
            f"GET request failed with status code: {response.status_code}"
        assert "tomato" in response.text
