# 
# (C) giovambattista vieri 2022 all rights reserved
# License AFFERO GPL 3.0

### cookie database creation
import os
import sys
import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine 
from sqlalchemy import DateTime 

Base = declarative_base()

engine = create_engine('sqlite:///sampleaquaco.sqlite')
connection = engine.connect()
metadata = MetaData()


class Sample(Base):  ### look for url class
    __tablename__ = 'sample'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id          = Column(Integer, primary_key=True)
    dateandtime = Column(DateTime, nullable=True,  server_default=func.now()) #### default=datetime.utcnow()
   # dateandtime = Column(DateTime, nullable=True,  default=datetime.utcnow) #### default=datetime.utcnow()

    orig_sample = Column(Text, nullable=False) ## in json
    T_av       = Column(Float, nullable=True)  ## temperature
    P_av       = Column(Float, nullable=True)  ## Pressure
    H_av       = Column(Float, nullable=True)  ## Humidity
    G_av       = Column(Float, nullable=True)  ## gas resistance



    
Base.metadata.create_all(bind=engine)
metadata.create_all(engine)
for _t in metadata.tables:
   print("Table: ", _t)



engine.dispose()
