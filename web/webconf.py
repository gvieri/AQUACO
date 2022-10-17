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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./confaquaco.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True


db = SQLAlchemy(app)
engine = create_engine('sqlite:///confaquaco.sqlite')
Base = declarative_base(bind=engine)
class Confi(db.Model):
    __tablename__ = 'configuration'
#    __table_args__ = {'autoload':True}

    id          = db.Column(db.Integer, primary_key=True)

    dateandtime = db.Column(db.DateTime, nullable=True,  server_default=func.now()) #### default=datetime.utcnow()
    templowth   = db.Column(db.Float, nullable=True)
    temphighth  = db.Column(db.Float, nullable=True)
    preslowth   = db.Column(db.Float, nullable=True)
    preshighth  = db.Column(db.Float, nullable=True)
    hum_lowth   = db.Column(db.Float, nullable=True)
    hum_highth  = db.Column(db.Float, nullable=True)
    gas_lowth   = db.Column(db.Float, nullable=True)
    gas_highth  = db.Column(db.Float, nullable=True)

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

"""
try: 
    dummy=Confi(templowth=10.0,
            temphighth=11.0,
            preslowth =12.0,
            preshighth=13.0,
            hum_lowth =14.0,
            hum_highth=15.0,
            gas_lowth =16.0,
            gas_highth=17.0)
    print(dummy)
    db.session.add(dummy)
    db.session.commit()
except Exception as e:
    print('db init Except')
    print(str(e))

try: 
    conf=Confi.query.all()
    print(conf)
except Exception as e:
    print ('db query exception')
    print(str(e))
"""

@app.route('/')
def hello():
    val=render_template("webconfhome.html")
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
#            print ('getting parameters')
            tlow =float(request.form['tlow'])
            thigh=float(request.form['thigh'])
            plow =float(request.form['plow'])
            phigh=float(request.form['phigh'])
            hlow =float(request.form['hlow'])
            hhigh=float(request.form['hhigh'])
            glow =float(request.form['glow'])
            ghigh=float(request.form['ghigh'])
            """
            print ("tlow:",tlow)
            print ("thigh:",thigh)
            print ("plow:",plow)
            print ("phigh:",phigh)
            print ("hlow:",hlow)
            print ("hhigh:",hhigh)
            print ("glow:",glow)
            print ("ghigh:",ghigh)
            """

            dummy=Confi(templowth=tlow,
                    temphighth=thigh,
                    preslowth =plow,
                    preshighth=phigh,
                    hum_lowth =hlow,
                    hum_highth=hhigh,
                    gas_lowth =glow,
                    gas_highth=ghigh)
#            print(dummy)
 
            db.session.add(dummy)
            db.session.commit()
        except Exception as e: 
            print ('type is:', e.__class__.__name__)
            print (e) 
            db.session.rollback()
            msg="problem in db add" 
        finally:
            return render_template('resultinsert.html', msg=msg)

    return render_template('resultinsert.html', msg=msg)
