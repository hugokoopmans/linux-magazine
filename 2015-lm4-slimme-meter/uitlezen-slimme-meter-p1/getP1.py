# 
# dit script leest de p1 slimme meter uit en slaat de data op in een database
# hugo koopmans hugo.koopmans@gmail.com
# 
# veel dank aan GE Janssen
# http://gejanssen.com/howto/Slimme-meter-uitlezen/index.html
# DSMR P1 uitlezer
# (c) 10-2012 - GJ - gratis te kopieren en te plakken

import sys,syslog
import serial

from postmessage import postMessage

versie = "1.0"
debug = True

def getP1():
        
    # Main program
    if debug:
        print ("DSMR P1 uitlezen",  versie)
        print("_____________________________")

    #Set COM port config
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.bytesize = serial.SEVENBITS
    ser.parity = serial.PARITY_EVEN
    ser.stopbits = serial.STOPBITS_ONE
    ser.xonxoff = 0
    ser.rtscts = 0
    ser.timeout = 20
    ser.port = "/dev/ttyUSB0"

    #Open COM port
    try:
        ser.open()
    except:
        syslog.syslog(syslog.LOG_CRIT,"p1: error, cannot open: %s. Full stop."  % ser.name)
        sys.exit()

    #Initialize
    stack = []

    # we expect 20 lines of data
    for l in range(20):
        line=''
        #Read line
        raw = ser.readline()
        p1_str = str(raw)
        p1_line=p1_str.strip()
        stack.append(p1_line)
    # als je alles wil zien moet je de volgende line uncommenten
        if debug:
            print (p1_line)
    if debug:
        print("______________end raw message________________")

    #Close port and show status
    try:
        ser.close()
    except:
        syslog.syslog(syslog.LOG_CRIT,"p1: cannot close connection to %s. Exit." % ser.name )
    return stack

def parseStack2Message(stack):
    
    # message from P1 is fixed size
    message = {}
    
    
    # flag needed whenw e go iterate over all lines in message
    # if we find gas code the next line holds the gas value
    next_line_is_gas = False
    
    try:
        for r in stack:
            if next_line_is_gas:
                # this is only true after we found a gas line
                message['gas'] = r[1:10] # line following 0-1:24.3.0
                next_line_is_gas = False 
                if debug:
                    print "Gas          ", int(float(r[1:10])*1000), " dm3"
            elif r[0:9] == "1-0:1.8.1":
                message['daldag'] = r[10:19]
                if debug:
                    print "daldag     :", r[10:15]
            elif r[0:9] == "1-0:1.8.2":
                message['piekdag'] = r[10:19] # 1-0:1.8.2
                if debug:
                    print "piekdag    ", r[10:15]
            # Daltarief, teruggeleverd vermogen 1-0:2.8.1
            elif r[0:9] == "1-0:2.8.1":
                message['dalterug'] = r[10:19] # 1-0:2.8.1
                if debug:
                    print "dalterug   ", r[10:15]
            # Piek tarief, teruggeleverd vermogen 1-0:2.8.2
            elif r[0:9] == "1-0:2.8.2":
                message['piekterug'] = r[10:19] # 1-0:2.8.2
                if debug:
                    print "piekterug  ", r[10:15]
            # Huidige stroomafname: 1-0:1.7.0
            elif r[0:9] == "1-0:1.7.0":
                message['afgenomen_vermogen'] = r[10:17] # 1-0:1.7.0
                if debug:
                    print "afgenomen vermogen      ", int(float(r[10:17])*1000), " W"
            # Huidig teruggeleverd vermogen: 1-0:1.7.0
            elif r[0:9] == "1-0:2.7.0":
                message['teruggeleverde_vermogen'] = r[10:17] # 1-0:2.7.0
                if debug:
                    print "teruggeleverd vermogen  ", int(float(r[10:17])), " W"
            # Gasmeter: 0-1:24.3.0
            elif r[0:10] == "0-1:24.3.0":
                next_line_is_gas = True
            else:
                pass

    except :
        syslog.syslog(syslog.LOG_CRIT,"p1: cannot parse stack to message")

    return message

if __name__ == '__main__':
    try:
        s = getP1()
        syslog.syslog(syslog.LOG_CRIT,"p1: succesfull communication with p1 port.")
        has_s = True
    except:
        syslog.syslog(syslog.LOG_CRIT,"p1: failed to get message from p1 port.")
        has_s = False

    if has_s:
        try:
            m = parseStack2Message(s)
            syslog.syslog(syslog.LOG_CRIT,"p1: succesfully writen message to database.")
        except:
            syslog.syslog(syslog.LOG_CRIT,"p1: failed to write message to database.")
    if debug:
        print("_____________start messsage_____________")
        print m
        print("______________end message_______________")
    postMessage(m)

    
