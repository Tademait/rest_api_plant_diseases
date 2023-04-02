import pytest
import requests
import database


class Test_db:
    @pytest.fixture(scope='class')
    def db(self):
        db = database.Database()
        return db
    
    def test_establish_db_connection(self, db):
        assert db, "Database connection failed"
    
    def test_query_all_plants(self, db):
        res = db.query_all_plants()
        assert res is not None, "No plants in database"
        
    def test_query_all_diseases(self, db):
        res = db.query_all_diseases_for_plant("tomato")
        assert res is not None, "No diseases in database"
        
    def test_query_all_diseases_doesnt_exist(self, db):
        res = db.query_all_diseases_for_plant("doesntexist")
        assert res is None, "Diseases exist for plant that doesn't exist"
    
    def test_query_disease_detail(self, db):
        res = db.query_disease_detail_specify_plant("early blight", "tomato")
        assert res, "No disease detail"
        
    def test_query_disease_detail_doesnt_exist(self, db):
        res = db.query_disease_detail_specify_plant("doesntexist", "tomato")
        assert res is None, "Disease detail found for non existant disease"
        
    def test_query_disease_detail_plant_doesnt_exist(self, db):
        res = db.query_disease_detail_specify_plant("bacterial spot", "doesntexist")
        assert res is None, "Disease detail found for non existant plant"
