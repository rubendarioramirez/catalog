import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Restaurant(Base):
    __tablename__ = 'restaurant'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class MenuItem(Base):
    __tablename__ = 'menu_item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) 


engine = create_engine('sqlite:///restaurantmenu.db')
 

Base.metadata.create_all(engine)

#### https://www.udacity.com/course/viewer#!/c-ud088-nd/l-3621198668/m-3630068948 
#### Crud review con todos los casos: ADD, DELETE, UPDATE, RETRIEVE