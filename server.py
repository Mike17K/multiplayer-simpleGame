from pdb import line_prefix
import socket
from _thread import *
from time import time

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

cursors = [] #[id:x,y,0,22,color,0],[...] ...


backgroundColor="#ffff8f"
width=500
height=500
grid=(width*height)*[backgroundColor] #screen width, height array

#                   x-width   
#      x-1            x         x+1
#                   x+width
#
# pos = [x%width,x//height]


def threaded_client(conn):
    global pos,currentId

    _id="Thread_"+str(currentId)+""
    conn.send(str.encode(_id))
    currentId+=1

    configed=False
    while True:
        try:
            data = conn.recv(128)
            
            input_data = data.decode('utf-8') #name,pos x,y of mouse in pixels of the screen not the grid, mode: draw-erace, scale int,RGB

            if not configed:
                if input_data==_id+":configuration":
                    configed=True
                    configMessage=''
                    for i in grid:
                        configMessage+=i+","
                    configMessage = configMessage[:-1]
                    #print(configMessage)
                    conn.send(str.encode(configMessage))
                    del configMessage
                    continue

                    
                    
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                

                #print("Input data: ",input_data)
                input_data=input_data.split(':')
                client_id = input_data[0] #same with _id theoreticly
                input_data=input_data[1].split(',')

                posX = int(input_data[0])    #0-1000
                posY = int(input_data[1])    #0-1000
                mode = input_data[2]         #'erase-draw'
                scale = int(input_data[3])
                color = input_data[4]
                click = int(input_data[5]) #0/1

                ok=False
                for i in range(len(cursors)):
                    if cursors[i].split(",")[0]==client_id:
                        ok=True
                        #edit cursor baces on input_data
                        #id,posx,posy,color
                        cursors[i]=client_id+","+str(posX)+","+str(posY)+","+mode+","+str(scale)+","+color+","+str(click)
                        break
                
                if not ok:
                    #add cursor to cursors
                    cursors.append(client_id+","+str(posX)+","+str(posY)+","+mode+","+str(scale)+","+color+","+str(click))
                    print("Added cursor... ",cursors)
                    pass
                
                

                #write to array with the screen of everyone so at the start if they conect for the first time u send the hole image for configuration
                if click: 
                    if(mode=='erase'): color=backgroundColor

                    x0 = int(posX/1000*width)+width*int(posY/1000*height)
                    grid[x0]=color
                    #handle scale 
                    #scale to grind pixels
                    
                    #print(scale, int(scale*width/1000))
                    
                    x_grid = int(posX/1000*width)
                    y_grid = int(posY/1000*height)

                    s = int(scale*width/1000)
                    if s>0:
                        for raw in range(-s,s+1):
                            if x_grid-raw<0 or x_grid-raw>=width:
                                continue
                            for line in range(-s,s+1):
                                if y_grid-line<0 or y_grid-line>=height:
                                    continue
                                if x0+line+raw*width<width*height:
                                    grid[x0+line+raw*width]= color
                        


                        



                






                output_data=''
                output_data+=str(width)+","+str(height)+":"


                for cursor in cursors:
                    output_data+=cursor+":"
                output_data=output_data[:-1]
                #print(".")

                #print(output_data)
                conn.sendall(str.encode(output_data)) # width,height:id,posx,posy,mode,scale,color,click:..

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