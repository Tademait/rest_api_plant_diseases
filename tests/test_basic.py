import pytest
import requests
import json
import pytest


class Test_basic:
    def test_establish_connection(self):
        response = requests.get("http://localhost:8000/")
        assert response.ok, "Connection to REST API failed"
        
    @pytest.mark.skip()
    def test_get_request(self):
        response = requests.get("http://localhost:8000/analyze")
        assert response.status_code == 200, "GET request failed"
