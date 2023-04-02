from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, text
from sqlalchemy.orm import Session, Relationship, backref, declarative_base, joinedload
import config


Base = declarative_base()
class Database():
    def __init__(self, verbose=False) -> None:
        self.engine = create_engine(config.DB_CONNECTION_STRING, echo=verbose)
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
        
    def query_all_plants(self):
        with Session(bind=self.engine) as session:
            plants = session.query(Plant).all()
            if not plants:
                return None
            return {"plants": [plant.name for plant in plants]}
    
    def query_all_diseases_for_plant(self, plant_name):
        with Session(bind=self.engine) as session:
            diseases = session.query(Disease).join(Plant.diseases).filter(Plant.name == plant_name.lower()).options(joinedload(Disease.pictures)).all()
            if not diseases:
                return None
            return [{"id": disease.id, "pictures": disease.pictures, "name": disease.name }  for disease in diseases]
    
    # deprecated, some diseases have a common name among multiple plants
    def query_disease_detail(self, disease_name):
        with Session(bind=self.engine) as session:
            return session.query(Disease).filter(Disease.name == disease_name.lower()).first()

    def query_disease_detail_specify_plant(self, disease_name, plant_name):
        with Session(bind=self.engine) as session:
            disease = session.query(Disease).join(Plant.diseases).filter(Plant.name == plant_name.lower()).filter(Disease.name == disease_name.lower()).first()
            if not disease:
                return None
            disease.pictures # this needs to be called because of lazy-loading applied to Relationship object
            disease_summary = disease.__dict__
            return disease_summary

    def query_all_news(self):
        with Session(bind=self.engine) as session:
            news = session.query(News).all()
            if not news:
                return None
            return [news_item.__dict__ for news_item in news]

    def add_news(self, title, body):
        with Session(bind=self.engine) as session:
            news = News(title=title, body=body)
            session.add(news)
            session.commit()
            return (news in session)


class Plant(Base):
    __tablename__ = 'plant'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    diseases = Relationship('Disease', backref='plant')

    def __repr__(self):
        return f"<Plant(id={self.id} name='{self.name}')>"
    
    
class Disease(Base):
    __tablename__ = 'disease'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    info = Column(Text)
    treatment = Column(Text)
    plant_id = Column(Integer, ForeignKey('plant.id'))
    pictures = Relationship('Picture', backref='disease')
    
    def __repr__(self):
        return f"<Disease(id={self.id} name='{self.name}')>"
    

class Picture(Base):
    __tablename__ = 'picture'
    
    id = Column(Integer, primary_key=True)
    url = Column(String)
    disease_id = Column(Integer, ForeignKey('disease.id'))
    
    def __repr__(self):
        return f"<Picture(id={self.id})>"


class News(Base):
    __tablename__ = 'news'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    
    def __repr__(self):
        return f"<News(id={self.id} title={self.title})>"


# when database.py is called directly, it creates all tables in the database
if __name__ == "__main__":
    db = Database()
    db.create_tables()