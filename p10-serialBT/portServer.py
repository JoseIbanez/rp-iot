#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import os
import time
import serial
import threading
import logging


cv = threading.Condition()

cmdList = []
serStatus = 0

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


def on_new_client(clientsocket,addr):
    while True:
        try:
            msg = clientsocket.recv(1024)
        except:
            break

        if len(msg) > 0:
            with cv:
                cmdList.append(msg)
                cv.notify()

        logging.debug('Addr:'+addr + ' Rec: ' + msg)
        msg = "serStatus: "+str(serStatus)
        #time.sleep(1)

        try:
            clientsocket.send(msg)
        except:
            break

    clientsocket.close()



def serialServer():

    lastAnswer = 10
    lastCmd = 0
    timeToSleep = 30
    serStatus = 0

    while True:

        #Message timeout
        if lastCmd > timeToSleep and len(cmdList) == 0:
            #print "z"
            with cv:
                cv.wait(10)
            #time.sleep(2)
            continue

        elif lastCmd > timeToSleep and len(cmdList) > 0:
            logging.debug("New command. Wakeup")
            lastCmd = 0

        elif serStatus == 1:
            time.sleep(1)

        elif len(cmdList) == 0:
            with cv:
                cv.wait(1)

        #Port was closed
        if serStatus == 0:
            ser = serial.Serial(
                            port="/dev/rfcomm0",
                            baudrate=9600,
                            timeout=1.5)
            time.sleep(1)
            logging.debug("Port isOpen: "+str(ser.isOpen()))
            # Now port is opened but inactive
            serStatus = 1

        #Try to read a message
        try:
            ans = ser.readline()
        except:
            ans = ""

        if len(ans)>0:
            logging.debug("<<"+ans)
            lastAnswer = 0
            serStatus = 2

        #time.sleep(1)
        lastAnswer = lastAnswer + 1
        lastCmd  = lastCmd + 1
        #print "."


        # Much time without answers
        if lastAnswer > 20:
            serStatus = 0
            lastAnswer = 0
            ser.close()
            logging.debug("Reset port")
            time.sleep(5)
            continue

        # Time to spleep
        if lastCmd > timeToSleep:
            serStatus = 0
            ser.close()
            logging.debug("No commands, to sleep")
            #time.sleep(5)
            continue

        #Check connection status
        if lastAnswer > 10:
            serStatus = 1
            logging.debug(">>STATUS")
            try:
            	ser.write("STATUS")
            except:
                pass
            continue

        # If ok and there is any command, send it
        if len(cmdList) > 0 and serStatus == 2:
            lastCmd = 0
            cmd = cmdList.pop(0)
            logging.debug(">>"+cmd)
            ser.write(cmd)



#######################################

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    os.remove("/tmp/channel0")
except OSError:
    pass

logging.debug('Server started!')
t1 = threading.Thread(name='serialSrv', target=serialServer)
t1.start()
#thread.start_new_thread(serialServer,())


logging.debug('Waiting for clients...')
s.bind("/tmp/channel0")
s.listen(5)                 # Now wait for client connection.


while True:
    c, addr = s.accept()     # Establish connection with client.

    t2 = threading.Thread(name='socket', target=on_new_client, args=(c,addr))
    t2.start()
    #thread.start_new_thread(on_new_client,(c,addr))


s.close()

