#
# (c) 2023 Vieri Giovambattista All Rights Reserved 
# License Affero GPL v.3 
#

# this code grap std out in json format coming from rtl_433 and, insert into a db .... 


import sys
import subprocess 
import argparse
import datetime
import time
import pprint

import json

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy import text


###################################

sensor_name="Oregon-v1"

###################################

def getOptions(args=sys.argv[1:]):
    parser=argparse.ArgumentParser(description='executes operations on Nordi Thingy:53')
    parser.add_argument('-d','--debug',help='enables debug info', default=False, action='store_true' )
    parser.add_argument('-r','--repeat',help='repetition numbers 0 for infinite loop.', type=int, default=0, action='store' )
    parser.add_argument('-f','--filename',help='output filename. ', action='store', default='external53log.txt' )
    parser.add_argument('-s','--sensorname',help='sensor name ', action='store', default="Oregon-v1" )

    parser.add_argument('-db','--database',help='sqlite3 database filename  ', action='store', default='externalsampleaquaco.sqlite' )
    opt=parser.parse_args(args)
    return(opt)

Base = declarative_base()

class Sample(Base):  ### look for url class
    __tablename__ = 'sampleR'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id          = Column(Integer, primary_key=True)
    dateandtime = Column(DateTime, nullable=True,  server_default=func.now()) #### default=datetime.utcnow()
   # dateandtime = Column(DateTime, nullable=True,  default=datetime.utcnow) #### default=datetime.utcnow()

    orig_sample = Column(Text, nullable=False) ## in json
    T_av       = Column(Float, nullable=True, default=9999)  ## temperature
    P_av       = Column(Float, nullable=True, default=9999)  ## Pressure
    H_av       = Column(Float, nullable=True, default=9999)  ## Humidity
    G_av       = Column(Float, nullable=True, default=999999999)  ## gas resistance




##########################################
###if __name__ == "__main__":

opt=getOptions()
pprint.pprint(opt)
if opt.debug: pprint.pprint(opt)

sensor_name=opt.sensorname
engine = create_engine('sqlite:///'+opt.database)
connection = engine.connect()
metadata = MetaData()


proc = subprocess.Popen(['rtl_433', '-F', 'json'], stdout=subprocess.PIPE)
while True:
    line = proc.stdout.readline()
    if not line:
        break
    if sensor_name in str(line):
        res=line.rstrip()
        res_dict = json.loads(res.decode('utf-8'))
        T_av=float(res_dict['temperature_C'])
        record=insert(Sample).values(orig_sample=str(res),T_av=T_av)
        connection.execute(record) 
        if opt.debug: print(str(res))

    else:
        if opt.debug: print('nok    ',line.rstrip())


engine.dispose()
print ("done")

