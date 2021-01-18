import socket
import os
import serial
import time

ser = serial.Serial('/dev/ttyUSB0',9600)
cmd = 'sudo fuser -k 5560/tcp'
host = ''
port = 5560

storedValue = "Yo, what's up?"

def setupServer():
    os.system(cmd)
    print("killed processes running on port 5560")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")
    return s

def valmap(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def setupConnection():
    s.listen(3) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    reply = 'Unknown Command'
    conn.sendall(str.encode(reply))
    print("sent " + reply)
    return conn

def GET():
    reply = storedValue
    return reply

def REPEAT(dataMessage):
    reply = dataMessage[1]
    return reply

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024) # receive the data
        #print(type(data))
        #data = data.split("x1a")
        #command = data[1]
        #print(data)
        data = data.decode('utf-8')
        print(type(data))
        # Split the data such that you separate the command
        # from the rest of the data.
        tab = data[2:].split(',')
        print(tab)
        command = tab[0]
        if command == 'GET':
            print(tab[1])
        elif command == '1':
            if (len(tab) == 3):
                testx = float(tab[1])
                testy = float(tab[2])*-1
                xval = str(int(valmap(testx,-1,1,220,440)))
                yval = str(int(valmap(testy,-1,1,320,470)))
                send = "1"+xval+""+yval
                ser.write(send.encode())
                print("x: "+xval+" y: "+yval)
            
        elif command == '2':
            print("Our client has left us :(")
            break
        elif command == '3':
            print("Our server is shutting down.")
            s.close()
            break
        elif command == '4':
            print("Closing eyes")
            send = "4000000"
            ser.write(send.encode())
        elif command == '5':
            print("Opening eyes")
            send = "5000000"
            ser.write(send.encode())
        else:
            reply = 'Unknown Command'
        # Send the reply back to the client
        #conn.sendall(str.encode(reply))
        #print("Data has been sent!")
    conn.close()
        

s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        s.close()
        break
