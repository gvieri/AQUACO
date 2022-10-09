#
#
#  explorer.py (for thingy) 
#
#  (C) Giovambattista Vieri 2022
#  All Rights Reserved
#  License Affero GPL V3.0 
#


#####

import base64
import time
import serial 
import cbor2 
import sys 
import argparse 
import pprint

#####

terminal='/dev/ttyACM0'

#####


# configuration & parameters

def getOptions(args=sys.argv[1:]):
    parser=argparse.ArgumentParser(description='executes operations on Nordi Thingy:53')
    parser.add_argument('-t','--terminal',help='choose a different terminal from /dev/ttyACM0', default='/dev/ttyACM0', action='store_true' )
    parser.add_argument('-d','--debug',help='enables debug info', default=False, action='store_true' )
    parser.add_argument('-g','--gethelp', help='get help from thingy the exit', default=False, action='store_true')
    parser.add_argument('-b','--base64', help='dump result as base64 decoded  ', default=False, action='store_true')
    parser.add_argument('-i','--interval', help='sampling interval', action='store', type=int, default=250 )
    parser.add_argument('-l','--lenght', help='sampling length', action='store', type=int, default=2000)
    parser.add_argument('-R','--raw',help='dump result as raw', action='store_true' )
    parser.add_argument('-H','--HELP',help='dump of AT+HELP command on thingy', action='store_true' )
    parser.add_argument('-c','--cbor',help='dump result as CBOR decoded', action='store_true' )
    parser.add_argument('-j','--json', help='dump result as json', action='store_true' ) 
    parser.add_argument('-r','--reset',help='it execute a reset on the thingy:53', action='store_true' )
    opt=parser.parse_args(args)
    return(opt) 





# end conf & par management

#################### global var ##########################

ser=0
opt=0

def init():
   ser = serial.Serial(terminal, baudrate=115200,
   timeout=10, 
   bytesize=serial.EIGHTBITS,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE) 
   return(ser)


def askHelp(ser):
    ser.write(b'AT+HELP\r')
    while True:
        txt=ser.readline()
        print(txt)
  ###      if (txt==b'OK\r\r\n') : 
        if (txt==b'> ') : 
            if opt.debug: print("find ok!\n")
            break

def makeClearConfig(ser):
    ser.write(b'AT+CLEARCONFIG\r')
    txt=ser.readline()
    if opt.debug:    print(txt)

#time.sleep(1)

def makeSampleSettings(ser, filename='',period=250, len=2000,key=''):
#    ser.write(b'AT+SAMPLESETTINGS=,250,2000\r')
    command='AT+SAMPLESETTINGS=,'+str(period)+','+str(len)+'\r'
    ser.write(str.encode(command))
    while True:
        txt=ser.readline()
        if opt.debug: print(txt)
        txt=ser.readline()
        if opt.debug: print(txt)
        if (txt==b'OK\r\r\n') : 
            if opt.debug: print("find ok!\n")
            break

def makeSampleStart(ser, sensor='Environment'):
    ser.write(b'AT+SAMPLESTART=Environment\r')
    #txt=ser.read(2000)
    txt=""
    fr=to=""
    while True:
        oldtxt=txt
        txt= ser.readline()
        if opt.debug:print(txt)
        if (txt==b'OK\r\r\n') :
            ### extract start position and final position of message. 
            dummy= str(oldtxt).split(', ')
            if opt.debug:print ("==================================")
            if opt.debug:print( dummy)
            if opt.debug:print ("==================================")
            fr  =dummy[2][5:]
            if opt.debug:print(fr + "\n")
            to  =dummy[3][3:-8]
            if opt.debug:print(to + "\n")

            txt= ser.readline()
            if opt.debug:print(txt)
            break

    return fr,to

##########################################
###if __name__ == "__main__":
opt=getOptions()
if opt.debug: pprint.pprint(opt)
terminal=opt.terminal

ser=init()
txt=ser.readline()


if opt.HELP:
    askHelp(ser)
    exit(0)

if (opt.reset):
    makeClearConfig(ser)

makeSampleSettings(ser)
if opt.debug: print("--------------------------------------------\n")
fr,to=makeSampleStart(ser)
if opt.debug: print("--------------------------------------------\n")
#time.sleep(6.0)
txt= ser.readline()
if opt.debug: print(txt)
ser.write(('AT+READBUFFER='+fr+','+to+'\r').encode('utf-8'))
txt= ser.readline()
if opt.debug: print(txt)
txt= ser.readline()
if opt.debug: print (len(txt))
content=txt[:-3]
if opt.debug: print(txt)

txt= ser.readline()
if opt.debug: print(txt)
if opt.debug: print("--------------------------------------------\n")
if(opt.raw): print(content)

#print ("============ decode base 64 =================")
b64dec = base64.b64decode(content)
if opt.base64: print (b64dec)
#print (b64dec)
if opt.debug: print("++++++++++++++++++++++++++++++++++++++++++++++")
#cbordec=cbor2.decoder.loads(content)
#cbordec=cbor2.loads(content)
cbordec=cbor2.loads(b64dec)
if opt.cbor: print(cbordec)
if opt.debug: print ("||||||||||||||||||||||||||||||||||||||||||||||")
if opt.debug or opt.json: pprint.pprint(cbordec)
if opt.debug: print ("||||||||||||||||||||||||||||||||||||||||||||||")



