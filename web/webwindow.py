#  (c) Giovambattista Vieri 2022
#  All Rights Reserved
#  License AGPL 
#  No guarantee/warranty on this alpha code. 
# 
#

from flask import Flask 
from flask import render_template
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import requests
import csv
from flask import send_file
from sqlalchemy import desc 

import pprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./confaquaco.sqlite'
app.config['SQLALCHEMY_BINDS']        = {'internalsample': 'sqlite:///./sampleaquaco.sqlite', 'externalsample': 'sqlite:///./externalsampleaquaco.sqlite'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True


db0 = SQLAlchemy(app)
engine = create_engine('sqlite:///confaquaco.sqlite')
Base = declarative_base(bind=engine)
class Confi(db0.Model):
    __tablename__ = 'configuration'
#    __table_args__ = {'autoload':True}

    id          = db0.Column(db0.Integer, primary_key=True)

    dateandtime = db0.Column(db0.DateTime, nullable=True,  server_default=func.now()) #### default=datetime.utcnow()
    templowth   = db0.Column(db0.Float, nullable=True)
    temphighth  = db0.Column(db0.Float, nullable=True)
    preslowth   = db0.Column(db0.Float, nullable=True)
    preshighth  = db0.Column(db0.Float, nullable=True)
    hum_lowth   = db0.Column(db0.Float, nullable=True)
    hum_highth  = db0.Column(db0.Float, nullable=True)
    gas_lowth   = db0.Column(db0.Float, nullable=True)
    gas_highth  = db0.Column(db0.Float, nullable=True)

    def __repr__(self):
        return '<Confi %r>' % self.id

    def __init__(self, templowth   , temphighth  , preslowth, preshighth , hum_lowth  , hum_highth, gas_lowth , gas_highth):
        self.templowth   = templowth
        self.temphighth  = temphighth
        self.preslowth   = preslowth
        self.preshighth  = hum_lowth
        self.hum_lowth   = hum_lowth
        self.hum_highth  = hum_highth
        self.gas_lowth   = gas_lowth
        self.gas_highth  = gas_highth

class SampleInternal(db0.Model):  ### look for url class
    __bind_key__  = 'internalsample'
    __tablename__ = 'sample'

    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id          = db0.Column(db0.Integer, primary_key=True)
    dateandtime = db0.Column(db0.DateTime, nullable=True,  server_default=func.now()) #### default=datetime.utcnow()
   # dateandtime = Column(DateTime, nullable=True,  default=datetime.utcnow) #### default=datetime.utcnow()

    orig_sample = db0.Column(db0.Text, nullable=False) ## in json
    T_av       = db0.Column(db0.Float, nullable=True)  ## temperature
    P_av       = db0.Column(db0.Float, nullable=True)  ## Pressure
    H_av       = db0.Column(db0.Float, nullable=True)  ## Humidity
    G_av       = db0.Column(db0.Float, nullable=True)  ## gas resistance

class SampleExternal(db0.Model):  ### look for url class
    __bind_key__  = 'externalsample'
    __tablename__ = 'sampleR'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id          = db0.Column(db0.Integer, primary_key=True)
    dateandtime = db0.Column(db0.DateTime, nullable=True,  server_default=func.now()) #### default=datetime.utcnow()
   # dateandtime = Column(DateTime, nullable=True,  default=datetime.utcnow) #### default=datetime.utcnow()

    orig_sample = db0.Column(db0.Text, nullable=False) ## in json
    T_av       = db0.Column(db0.Float, nullable=True)  ## temperature
    P_av       = db0.Column(db0.Float, nullable=True)  ## Pressure
    H_av       = db0.Column(db0.Float, nullable=True)  ## Humidity
    G_av       = db0.Column(db0.Float, nullable=True)  ## gas resistance





@app.route('/')
def monitor_T():
    Si=SampleInternal.query.order_by(desc(SampleInternal.id)).limit(1)
    Se=SampleExternal.query.order_by(desc(SampleExternal.id)).limit(1)
    dummyC=Confi.query.order_by(desc(Confi.id)).limit(1)
    exttemperature = Se[0].T_av
    inttemperature = Si[0].T_av
    delta = exttemperature - inttemperature
    hint="wait... "
    if delta > 1.0: hint="open NOW!"
    if delta < -1.0: hint="CLOSE!!! "
    val=render_template("windows_syn.html", hint=hint,measurename="may I open the WINDOW?", exttemperature=exttemperature, inttemperature=inttemperature, title='about window')
    return val

