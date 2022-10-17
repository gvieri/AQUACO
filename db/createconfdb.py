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

engine = create_engine('sqlite:///confaquaco.sqlite')
connection = engine.connect()
metadata = MetaData()

class Configuration(Base):
    __tablename__ = 'configuration'

    id          = Column(Integer, primary_key=True)
#    dateandtime = Column(DateTime, nullable=True,  default=datetime.utcnow) #### default=datetime.utcnow()
    dateandtime = Column(DateTime, nullable=True,  server_default=func.now()) #### default=datetime.utcnow()
    templowth   = Column(Float, nullable=True)
    temphighth  = Column(Float, nullable=True)
    preslowth   = Column(Float, nullable=True)
    preshighth  = Column(Float, nullable=True)
    hum_lowth   = Column(Float, nullable=True)
    hum_highth  = Column(Float, nullable=True)
    gas_lowth   = Column(Float, nullable=True)
    gas_highth  = Column(Float, nullable=True)
    
Base.metadata.create_all(bind=engine)
metadata.create_all(engine)
for _t in metadata.tables:
   print("Table: ", _t)



engine.dispose()
