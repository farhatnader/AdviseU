from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String)
	firstname = Column(String)
	lastname = Column(String)
	password = Column(String)

	def __init__(self, username, firstname, lastname, password):
		self.username = username
		self.firstname = firstname
		self.lastname = lastname
		self.password = password


Base.metadata.create_all(engine)