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
app.config['SQLALCHEMY_BINDS']        = {'sample': 'sqlite:///./sampleaquaco.sqlite'}
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

class Sample(db0.Model):  ### look for url class
    __bind_key__  = 'sample'
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




@app.route('/')
def hello():
    val=render_template("monitorhome.html")
    return val

@app.route('/monitor_T')
def monitor_T():
    dummyS=Sample.query.order_by(desc(Sample.id)).limit(1)
    dummyC=Confi.query.order_by(desc(Confi.id)).limit(1)
    hith = dummyC[0].temphighth
    lowth= str(dummyC[0].templowth)
    value= dummyS[0].T_av
    val=render_template("temp_syn.html", measurename="TEMPERATURE", lowth=lowth, hith=hith,value=value, title='average')
    return val

@app.route('/monitor_P')
def monitor_P():
    dummyS=Sample.query.order_by(desc(Sample.id)).limit(1)
    dummyC=Confi.query.order_by(desc(Confi.id)).limit(1)
    hith = dummyC[0].preshighth
    lowth= str(dummyC[0].preslowth)
    value= dummyS[0].P_av
    val=render_template("temp_syn.html", measurename="PRESSURE", lowth=lowth, hith=hith,value=value, title='average')
    return val

@app.route('/monitor_H')
def monitor_H():
    dummyS=Sample.query.order_by(desc(Sample.id)).limit(1)
    dummyC=Confi.query.order_by(desc(Confi.id)).limit(1)
    hith = dummyC[0].hum_highth
    lowth= str(dummyC[0].hum_lowth)
    value= dummyS[0].T_av
    val=render_template("temp_syn.html", measurename="HUMIDITY", lowth=lowth, hith=hith,value=value, title='average')
    return val

@app.route('/monitor_G')
def monitor_G():
    dummyS=Sample.query.order_by(desc(Sample.id)).limit(1)
    dummyC=Confi.query.order_by(desc(Confi.id)).limit(1)
    hith = dummyC[0].gas_highth
    lowth= str(dummyC[0].gas_lowth)
    value= dummyS[0].T_av
    val=render_template("temp_syn.html", measurename="GAS", lowth=lowth, hith=hith,value=value, title='average')
    return val


@app.route('/list_av')
def list_av():
    dummy=Sample.query.all()
    val=render_template("list_averageval.html", query=dummy, title='average')
    return val



@app.route('/show')
def show():
#### hereby the business logic 
    dummy=Confi.query.all()
    val=render_template("listall.html", query=dummy, title='prova')
    since = datetime.now() - timedelta(hours=8)
#    old = Confi.query.filter(Confi.timestamp > text('(NOW() - INTERVAL 8 HOURS)')).all()
    return val

@app.route('/insertform')
def insertform():
### it will increment quantity by one. 
    return render_template('insertwebconf.html')

@app.route('/insertconf', methods=['POST'])
def insertconf():
    msg=" problem on insertion" 
    if request.method == 'POST':
        try:
            msg="everything ok"
            tlow =float(request.form['tlow'])
            thigh=float(request.form['thigh'])
            plow =float(request.form['plow'])
            phigh=float(request.form['phigh'])
            hlow =float(request.form['hlow'])
            hhigh=float(request.form['hhigh'])
            glow =float(request.form['glow'])
            ghigh=float(request.form['ghigh'])

            dummy=Confi(templowth=tlow,
                    temphighth=thigh,
                    preslowth =plow,
                    preshighth=phigh,
                    hum_lowth =hlow,
                    hum_highth=hhigh,
                    gas_lowth =glow,
                    gas_highth=ghigh)
 
            db0.session.add(dummy)
            db0.session.commit()
        except Exception as e: 
            print ('type is:', e.__class__.__name__)
            print (e) 
            db0.session.rollback()
            msg="problem in db add" 
        finally:
            return render_template('resultinsert.html', msg=msg)

    return render_template('resultinsert.html', msg=msg)
