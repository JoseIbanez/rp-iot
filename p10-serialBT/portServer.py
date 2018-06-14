

####


#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import thread
import os
import time
import serial


cmdList = []

def on_new_client(clientsocket,addr):
    while True:
        try:
            msg = clientsocket.recv(1024)
        except:
            break

        if len(msg) > 0:
            cmdList.append(msg)

        #do some checks and if msg == someWeirdSignal: break:
        print addr, ' Rec ', msg
        msg = "bye"
        time.sleep(1)

        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        try:
            clientsocket.send(msg)
        except:
            break

    clientsocket.close()



def serialServer():

    serStatus = 0
    lastAnswer = 10
    lastCmd = 0
    timeToSleep = 30

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

        time.sleep(1)
        lastAnswer = lastAnswer + 1
        lastCmd  = lastCmd + 1
        print "."

	if lastAnswer > 20:
	    serStatus = 0
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
            #Just for test
	    print ">>STATUS"
            ser.write("STATUS")
            continue


        if len(cmdList) > 0:
            lastCmd = 0
            cmd = cmdList.pop(0)
            print ">>"+cmd
            ser.write(cmd)





#s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
#port = 50000                # Reserve a port for your service.


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

try:
    os.remove("/tmp/channel1")
except OSError:
    pass



print 'Server started!'
thread.start_new_thread(serialServer,())


print 'Waiting for clients...'

s.bind("/tmp/channel1")
#s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

#print 'Got connection from', addr
while True:
    c, addr = s.accept()     # Establish connection with client.
    thread.start_new_thread(on_new_client,(c,addr))
    #Note it's (addr,) not (addr) because second parameter is a tuple
    #Edit: (c,addr)
    #that's how you pass arguments to functions when creating new threads using thread module.
s.close()

