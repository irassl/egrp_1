# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

# from geoalchemy2 import Geometry

SQLITE = "sqlite"

ADDRESS = "address"

engine = create_engine("sqlite:///db.sqlite3", echo=True)
Base = declarative_base()


class House(Base):
    __tablename__ = "house"
    id = Column(Integer, primary_key=True)
    address = Column(String)
    okato = Column(Integer, unique=True)
    kadastor = Column(String, unique=True)
    kadastor_h = Column(String)
    year = Column(Integer)
    type_h = Column(String)
    floor = Column(Integer)

    def __init__(self, address, okato, kadastor, kadastor_h, year, type_h, floor):
        self.address = address
        self.okato = okato
        self.kadastor = kadastor
        self.kadastor_h = kadastor_h
        self.year = year
        self.type_h = type_h
        self.floor = floor

    def __repr__(self):
        return "<House('%s','%s','%s')>" % (self.address, self.kadastor_h, self.type_h)


class Flat(Base):
    __tablename__ = "flat"
    id = Column(Integer, primary_key=True)
    kadastor = Column(String, unique=True, nullable=True)
    type_f = Column(String, nullable=True)
    descrip = Column(String, nullable=True)
    floor = Column(Integer, nullable=True)
    area = Column(String, nullable=True)
    address = Column(String, nullable=True)

    def __init__(self, kadastor, type_f, descrip, floor, area, address):
        self.kadastor = kadastor
        self.type_f = type_f
        self.descrip = descrip
        self.floor = floor
        self.area = area
        self.address = address

    def __repr__(self):
        return "<flat('%s','%s','%s')>" % (self.kadastor, self.descrip, self.area)


class AddressNone(Base):
    __tablename__ = "addrnone"
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True, nullable=True)

    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return "<addrnNone('%s')>" % (self.address)


Base.metadata.create_all(engine)
