#! /usr/bin/env python3
'''\
Serial scanning module.
'''

import serial
import glob

def scan():
    '''scan for avaiable ports. return a list of tuples (num, name)'''
    available = []
    ttySs = glob.glob('/dev/ttyUSB*')
    ttySs.extend(glob.glob('/dev/ttyS*'))
    #print(ttySs)
    if len(ttySs)==0:
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append( (i,s.portstr))
                s.close()   # explicit close 'caue of delayed GC in java
            except serial.SerialException:
                pass
    else:
        for i in range(0,len(ttySs)):
            try:
                s = serial.Serial(ttySs[i])
                available.append( (i,ttySs[i]))
                s.close()
            except serial.SerialException:
                pass
    return available

#testapp
#print(scan())
