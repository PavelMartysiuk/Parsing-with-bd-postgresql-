from sqlalchemy import create_engine, Integer, String, DateTime, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://example_user:example_pass@localhost/Coronavirus', )

Base = declarative_base()
Session = sessionmaker(bind=engine)


class CoronavirusRussiaStatistic(Base):
    __tablename__ = 'russia'
    id = Column(Integer, primary_key=True)
    town = Column(String)
    sick = Column(String)
    recover = Column(String)
    death = Column(String)
    coordinates = Column(String)
    date = Column(DateTime)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    content = Column(String)
    source = Column(String)
    date = Column(DateTime)


class CoronavirusWorldStatistic(Base):
    __tablename__ = 'world'
    id = Column(Integer, primary_key=True)
    country = Column(String)
    sick = Column(String)
    recover = Column(String)
    death = Column(String)
    coordinates = Column(String)
    date = Column(DateTime)


Base.metadata.create_all(engine)
