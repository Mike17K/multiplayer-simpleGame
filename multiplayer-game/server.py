import socket
from _thread import *
from time import time
from packet import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.1.3'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(40)
print("Waiting for a connection")

currentId = 0

pos = []
def threaded_client(conn):
    global pos,currentId

    _id="Thread_"+chr(currentId+48)+""
    conn.send(str.encode(_id))
    currentId+=1
    
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            
            print("Data Received: ",reply)

            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                p = Packet.toObject(reply)
                
                print("Recieved: " + reply)

                id = p.id
                reply = p.toString()
                ok=False
                for i in range(len(pos)):
                    if pos[i].split(':')[0] == id:
                        ok = True
                        pos[i] = reply
                        break
                if not ok: #if its not in the list (new player)
                    pos.append(reply)
                
                    
                

                #updating the server data

                sepChar = '@'
                reply=""
                #nid = [x for x in range(len(pos)) if pos[x].split(':')[0]!=id]
                
                for i in range(len(pos)): # nid:
                    reply+=pos[i]+sepChar
                
                print("Sending: " + reply)
                conn.sendall(str.encode(reply))

        except Exception as e:
            print("Exception: ",e)
            break

    print("Connection Closed")
    conn.close()
    for i in pos:
        if i.split(':')[0]==_id:
            pos.remove(i)
    

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))