#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import thread
import os
import time
import serial


cmdList = []
serStatus = 0



def on_new_client(clientsocket,addr):
    while True:
        try:
            msg = clientsocket.recv(1024)
        except:
            break

        if len(msg) > 0:
            cmdList.append(msg)

        print addr, ' Rec ', msg
        msg = "serStatus: "+str(serStatus)
        time.sleep(1)

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

        if lastCmd > timeToSleep and len(cmdList) == 0:
            print "z"
            time.sleep(2)
            continue
        elif lastCmd > timeToSleep and len(cmdList) > 0:
            print "Wakeup"
            lastCmd = 0


        if serStatus == 0:

            ser = serial.Serial(
                port="/dev/rfcomm0",
                baudrate=9600,
                timeout=1.5)

            time.sleep(5)
            print "isOpen: "+str(ser.isOpen())
            serStatus = 1

        try:
            ans = ser.readline()
        except:
            ans = ""

        if len(ans)>0:
            print "<<"+ans
            lastAnswer = 0
            serStatus = 2

        time.sleep(1)
        lastAnswer = lastAnswer + 1
        lastCmd  = lastCmd + 1
        print "."

        if lastAnswer > 20:
            serStatus = 0
            lastAnswer = 0
            ser.close()
            print "Reset"
            time.sleep(5)
            continue


        if lastCmd > timeToSleep:
            serStatus = 0
            ser.close()
            print "To sleep"
            time.sleep(5)
            continue


        if lastAnswer > 10:
            #Check connection status
            serStatus = 1
            print ">>STATUS"
            try:
            	ser.write("STATUS")
            except:
                pass
            continue


        if len(cmdList) > 0 and serStatus == 2:
            lastCmd = 0
            cmd = cmdList.pop(0)
            print ">>"+cmd
            ser.write(cmd)




s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    os.remove("/tmp/channel0")
except OSError:
    pass



print 'Server started!'
thread.start_new_thread(serialServer,())


print 'Waiting for clients...'

s.bind("/tmp/channel0")
s.listen(5)                 # Now wait for client connection.


while True:
    c, addr = s.accept()     # Establish connection with client.
    thread.start_new_thread(on_new_client,(c,addr))


s.close()

