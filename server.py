import socket
from _thread import *
from time import time
from packet import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#for this to work on global conection need to put my public ip address google search: hat is my public ip adress
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

cursors = []

width=20
height=20
grid=[] #screen width, height array
for i in range(width*height):
    grid.append("#ffffff")


def threaded_client(conn):
    global pos,currentId

    _id="Thread_"+chr(currentId+48)+""
    conn.send(str.encode(_id))
    currentId+=1

    
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            
            #'id:mouseX,mouseY,color(hex)'
            input_data = data.decode('utf-8') #name,pos x,y of mouse in pixels of the screen not the grid, mode: draw-erace, scale int,RGB

            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Input data: ",input_data)
                client_id = input_data.split(':')[0] #same with _id theoreticly
                posX = int((input_data.split(':')[1]).split(",")[0])    #0-1000
                posY = int((input_data.split(':')[1]).split(",")[1])    #0-1000
                mode = (input_data.split(':')[1]).split(",")[2]         #'erase-draw'
                scale = int((input_data.split(':')[1]).split(",")[3])
                color = (input_data.split(':')[1]).split(",")[4]
                click = int((input_data.split(':')[1]).split(",")[5]) #0/1

                ok=False
                for i in range(len(cursors)):
                    if cursors[i].split(",")[0]==client_id:
                        ok=True
                        #edit cursor baces on input_data
                        #id:posx,posy,color
                        cursors[i]=client_id+":"+str(posX)+","+str(posY)+","+color
                        break
                if not ok:
                    #add cursor to cursors
                    cursors.append(client_id+":"+str(posX)+","+str(posY)+","+color)
                    pass
                








                
                #alpyChanges()


                output_data=''
                output_data+=str(width)+","+str(height)+":"

                for i in grid:
                    output_data+=i+","
                output_data=output_data[:-1]
                output_data+=':'

                for cursor in cursors:
                    output_data+=cursor+":"
                output_data=output_data[:-1]


                conn.sendall(str.encode(output_data)) # width,height:0,0,00,0,0,00,00,000,00,00,000,0,00,00,0,0:id,posx,posy,color:..

        except Exception as e:
            print("Exception: ",e)
            break

    print("Connection Closed")
    conn.close()
    for i in cursors:
        if i.split(',')[0]==_id:
            cursors.remove(i)
    

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))