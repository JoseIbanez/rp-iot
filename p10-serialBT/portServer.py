#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import os
import time
import serial
import threading
import logging


class SerialDevice:

    def __init__(self, port):
        self.cv = threading.Condition()
        self.cmdList = []
        self.port = port


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



def serialServer(id,x):

    serStatus = 0
    lastAnswer = 10
    lastCmd = 0
    timeToSleep = 30

    while True:

        cmdAvailable = len(sd[id].cmdList)

        #Message timeout
        if lastCmd > timeToSleep and cmdAvailable == 0:
            with sd[id].cv:
                sd[id].cv.wait(10)
            continue

        elif lastCmd > timeToSleep and cmdAvailable > 0:
            logging.debug("New command. Wakeup")
            lastCmd = 0

        elif cmdAvailable == 0:
            with sd[id].cv:
                sd[id].cv.wait(1)

        #Port was closed
        if serStatus == 0:
            try:
                ser = serial.Serial(
                            port=sd[id].port,
                            baudrate=9600,
                            timeout=1.5)
                logging.debug("Port isOpen: "+str(ser.isOpen()))
                # Now port is opened but inactive
                serStatus = 1
                time.sleep(1)


            except Exception as e:
                logging.error(e)
                ser = None
                serStatus = 0
                time.sleep(5)
                continue


        #Check connection status
        if serStatus == 1:
            logging.debug(">>STATUS")
            try:
            	ser.write("STATUS")
            except Exception as e:
                logging.error(e)

        #Try to read a message
        try:
            ans = ser.readline()
        except Exception as e:
            logging.error(e)
            ans = ""

        if len(ans)>0:
            logging.debug("<<"+ans)
            lastAnswer = 0
            serStatus = 2

        elif serStatus == 1:
            time.sleep(5)

        lastAnswer = lastAnswer + 1
        lastCmd  = lastCmd + 1

        # Much time without answers
        if lastAnswer > 10:
            serStatus = 1

        # Much time without answers
        if lastAnswer > 20:
            serStatus = 0
            lastAnswer = 0
            logging.debug("Reset port")
            try:
                ser.close()
            except Exception as e:
                logging.error(e)

            time.sleep(5)
            continue

        # Time to spleep
        if lastCmd > timeToSleep:
            serStatus = 0
            ser.close()
            logging.debug("No commands, time to sleep")
            #time.sleep(5)
            continue

        # If ok and there is any command, send it
        if cmdAvailable > 0 and serStatus == 2:
            lastCmd = 0
            cmd = sd[id].cmdList.pop(0)
            logging.debug(">>"+cmd)
            ser.write(cmd)



#######################################

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    os.remove("/tmp/channel0")
except OSError:
    pass

logging.debug('Server started!')

sd = {}
id = 'D1'
sd[id] = SerialDevice("/dev/rfcomm0")
t1 = threading.Thread(name='serialSrv'+id, target=serialServer, args=(id,1))
t1.start()

id = 'D2'
sd[id] = SerialDevice("/dev/rfcomm1")
t2 = threading.Thread(name='serialSrv'+id, target=serialServer, args=(id,1))
t2.start()


logging.debug('Waiting for clients...')
s.bind("/tmp/channel0")
s.listen(5)                 # Now wait for client connection.


while True:
    c, addr = s.accept()     # Establish connection with client.

    ts = threading.Thread(name='socket', target=on_new_client, args=(c,addr))
    ts.start()
    #thread.start_new_thread(on_new_client,(c,addr))


s.close()

