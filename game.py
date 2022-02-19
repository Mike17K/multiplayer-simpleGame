from ast import Pass
from email.mime import message
from logging import exception
import tkinter as tk
from tkinter.colorchooser import askcolor
import math as m
from xml.dom.expatbuilder import parseString

from matplotlib import image
from network import Network
import time

import threading
from PIL import Image,ImageTk
import numpy as np

class paint_game():
    def __init__(self, root):

        self.net = Network()

        self.root = root
        self.root.title("Paint")
        self.root.geometry("+0+0")
        self.root.resizable(False, False)
        
        self.frames=0
        self.tk_image=None

        self.mouse = [0,0,0] #x,y pos of the mouse , state
        self.screen_grid_width=500
        self.screen_grid_height=500
        self.dataCursors=[]
        self.cursors_pointers = 100*[0]

        self.playground_height = self.root.winfo_screenheight()* 2 / 4
        self.playground_width = 1.5 * self.playground_height

        self.scaleFactor = [self.playground_width/1000,self.playground_height/1000]

        self.grid_pixel_dimentions = [self.playground_width/self.screen_grid_width,self.playground_height/self.screen_grid_height]

        self.menu_background = tk.Frame(self.root, width = 100, height = int(100*self.scaleFactor[1]), bg = "#000000")
        self.menu_background.pack(side = tk.TOP,fill=tk.X)
        
        #self.menu_background.grid(row = 0, column = 0, sticky = tk.NSEW)


        self.playground = tk.Canvas(self.root, width = self.playground_width, height = self.playground_height,bg="#ffffff")

        #self.playground.grid(row = 1, column = 0, sticky = tk.NSEW)
        
        self.canvas_color = "#ffffff"
        self.fill_pen_color = "#000000"
        self.outline_color = "#000000"
        self.pen_mode = "draw"
        self.widths_matrix = [1, 2, 3, 4, 5, 10, 20, 50]
        self.width = self.widths_matrix[0]

        

        self.playground.bind("<MouseWheel>", self.adjust_width)
        self.playground.bind("<ButtonRelease-1>", self.unclick)
        self.playground.bind("<Button-1>", self.click)
        self.playground.bind("<Button-3>", self.change_pen_eraser)
        self.playground.bind("<Motion>",self.motion)

        self.configScreen()
        self.create_menu()
        
        
        

        
        self.network()


        self.screenLoop()
        self.playground.mainloop()
        
        
        

    def configScreen(self):
        
        print("Loading Image...",end = ' ')

        data = self.net.send_config(self.net.id+":configuration").split(",")
        
        try:
            def hex_to_rgb(value):
                value = value.lstrip('#')
                lv = len(value)
                return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

            for i in range(len(data)):
                #print(data[i])
                
                if data[i] != 'black':
                    data[i]=hex_to_rgb(data[i])
                else:
                    data[i]='#000000'

            #print(data)
            copy_data=np.zeros((self.screen_grid_width,self.screen_grid_height, 3), dtype=np.uint8)

            for i in range(len(data)):
                x=i%self.screen_grid_width
                y=i//self.screen_grid_height
                copy_data[y,x]=data[i]
            PIL_image = Image.fromarray(copy_data, 'RGB')
            

            PIL_image.save("image.png") 

            print(PIL_image)

            
        




            img=Image.open("image.png")
            tk_image=img.resize((int(self.playground_width),int(self.playground_height)), Image.ANTIALIAS)
            self.tk_image = ImageTk.PhotoImage(tk_image)

            self.playground.create_image(0,0,image= self.tk_image,anchor=tk.NW)
            self.playground.pack()

            


            #self.label = tk.Label(self.playground, image = tk_image)
            #self.label.image = tk_image
            # self.label.grid(row=1)

            

            print("Image loaded!")
        except Exception as e:
            print(e)
            
        del data
        

            
        
            
        
    def create_menu(self):
        self.game_menu_raws = 12
        self.pen_eraser_button = menu_button(self.menu_background, "🖊", "Calibri "+str(int(25*self.scaleFactor[0]))+" bold", "white", "black", int(50*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_pen_eraser).button
        menu_label(self.menu_background, "Width:", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "red", "black", int(140*self.scaleFactor[0]), self.menu_background["height"] / 2)
        self.widths_button = menu_button(self.menu_background, self.width, "Arial "+str(int(28*self.scaleFactor[0]))+" bold", "white", "black", int(200*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_drawing_width).button
        menu_label(self.menu_background, "Canvas\nfill:", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "red", "black", int(280*self.scaleFactor[0]), self.menu_background["height"] / 2)
        self.canvas_color_button = menu_button(self.menu_background, "⬛", "Calibri "+str(int(28*self.scaleFactor[0]))+" bold", self.canvas_color, "grey", int(360*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_canvas_color).button
        menu_label(self.menu_background, "Pen color:", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "red", "black", int(480*self.scaleFactor[0]), self.menu_background["height"] / 2)
        self.fill_pen_color_button = menu_button(self.menu_background, "⬛", "Calibri "+str(int(28*self.scaleFactor[0]))+" bold", self.fill_pen_color, "grey", int(580*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_fill_pen_color).button
        self.clean_canvas_button= menu_button(self.menu_background, "clean\ncanvas", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "white", "black", int(920*self.scaleFactor[0]), self.menu_background["height"] / 2, self.clean_canvas).button
    
        

    def change_drawing_width(self, event = None, direction = +1):
        self.width = (self.widths_matrix[1:] + [self.widths_matrix[0]])[self.widths_matrix.index(self.width) + (direction - 1)]
        self.widths_button.configure(text = self.width)
    def adjust_width(self, event):
        if event.delta == 120:
            self.change_drawing_width(event = None, direction = +1)
        elif event.delta == -120:
            self.change_drawing_width(event = None, direction = -1)
    def change_canvas_color(self, event):
        color = askcolor(title = "Color Chooser")
        self.canvas_color = color[1]
        self.playground.configure(bg = self.canvas_color)
        self.canvas_color_button.configure(fg = self.canvas_color)
    def change_fill_pen_color(self, event):
        color = askcolor(title = "Color Chooser")
        self.fill_pen_color = color[1]
        print(color[1])
        self.pen_eraser_color = self.fill_pen_color        
        self.fill_pen_color_button.configure(fg = self.fill_pen_color)
    def change_outline_color(self, event):
        color = askcolor(title = "Color Chooser")
        self.outline_color = color[1]
        self.outline_color_button.configure(fg = self.outline_color)
    def clean_canvas(self, event = None):
        self.playground.delete("all")
    def change_pen_eraser(self, event):
        if self.pen_mode == "draw":
            self.pen_mode = "erase"
            self.pen_eraser_button.configure(text = "⨂")
        elif self.pen_mode == "erase":
            self.pen_mode = "draw"
            self.pen_eraser_button.configure(text = "🖊")
    
    def click(self,event):
        self.mouse[2]=1
    def unclick(self,event):
        self.mouse[2]=0

    def draw_with_pen(self, posx, posy, mode, scale, color):
        # self.mouse[0] = int(event.x/self.playground_width*1000)
        # self.mouse[1] = int(event.y/self.playground_height*1000)
        '''
        self.cellx = int(posx / (2 * scale))
        self.pen_xcor = (self.cellx + 0.5) * (2 * scale)
        self.celly = int(posy / (2 * scale))
        self.pen_ycor = (self.celly + 0.5) * (2 * scale)
        '''

        self.pen_ycor=posy
        self.pen_xcor=posx

        surface=self.playground
        scaleX = scale*self.scaleFactor[0]
        scaleY = scale*self.scaleFactor[1]
        if mode == "draw":
            surface.create_rectangle(max(self.pen_xcor - scaleX,0), max(self.pen_ycor - scaleY,0), min(self.pen_xcor + scaleX,self.playground_width-1),min(self.pen_ycor + scaleY,self.playground_height-1), fill = color, outline = color)
        elif mode == "erase":
            surface.create_rectangle(max(self.pen_xcor - scaleX,0), max(self.pen_ycor - scaleY,0), min(self.pen_xcor + scaleX,self.playground_width-1),min(self.pen_ycor + scaleY,self.playground_height-1), fill = self.canvas_color, outline = self.canvas_color) 

    def motion(self,event):
        self.mouse[0] = int(event.x/self.playground_width*1000)
        self.mouse[1] = int(event.y/self.playground_height*1000)

    def send_data(self):
        
        """
        Send position to server
        :return: None
        """
        
        #sent data: name,pos x,y of mouse in pixels of the screen not the grid, mode: draw-erace, scale int,RGB

        #   'id:mouseX,mouseY,Mode(erase-draw),scale,color(hex),click'
        #   'id:x,y,0,22,color,0'

        data=''
        data += str(self.net.id)+":"
        data += str(min(self.mouse[0],999))+","+str(min(self.mouse[1],999))+","
        data += self.pen_mode +","
        data += str(self.width) +","
        data += self.fill_pen_color+","
        data += str(self.mouse[2])
        
        

        #print("Data: "+data)
        reply = self.net.send(data)
        #print("Data: ",reply)
        return reply

    def parse_data(self,data):
        #message
        #width,height:id,posx ,posy,mode,scale,color,click:...
        try:
            data=data.split(":")
            
            #print(data)
            self.screen_grid_width = int(data[0].split(",")[0])
            self.screen_grid_height = int(data[0].split(",")[1])


            self.dataCursors=data[1:]     
            for cursor in self.dataCursors:
                a=cursor.split(",")
                #print(a)

                id=a[0]
                posx = int(min(int(a[1])/1000,0.998)*self.playground_width)
                posy = int(min(int(a[2])/1000,0.998)*self.playground_height)
                mode = a[3]
                scale = int(a[4])
                color = a[5]
                click=int(a[6])
                
                #print(posx, posy, mode, scale, color,click)
                
                if click: #self.updateScreen(posx,posy,mode,scale,color)     
                    self.draw_with_pen(posx, posy, mode, scale, color)
                    
                    
                
            

            return True
        except Exception as e:
            print(e)
            time.sleep(15)
            return False
    
    def network(self):
        self.parse_data(self.send_data())
        self.root.after(20, self.network)

    def screenLoop(self):
        # self.frames+=1
        self.screenDraw()
        self.root.after(40, self.screenLoop)

    def screenDraw(self):
        for cursor in self.dataCursors:

                a=cursor.split(",")
                
                id=a[0].split("_")[1]
                posx = int(min(int(a[1])/1000,0.998)*self.playground_width)
                posy = int(min(int(a[2])/1000,0.998)*self.playground_height)
                mode = a[3]
                scale = int(a[4])
                color = a[5]
                click=int(a[6])
                scaleOfCursor=int(1*self.playground_width/100)
                
                try:
                    # self.playground.delete(self.cursors_pointers[int(id[-1])])
                    self.playground.delete(self.cursors_pointers[2*int(id)])
                    self.playground.delete(self.cursors_pointers[2*int(id)+1])
                except:
                    pass

                    
                
                self.cursors_pointers[2*int(id)] = self.playground.create_oval(posx-scaleOfCursor,posy-scaleOfCursor,posx+scaleOfCursor,posy+scaleOfCursor,fill=color,outline=color)
                self.cursors_pointers[2*int(id)+1] = self.playground.create_text(posx + 10, posy - 10, fill = "black", font = "Arial 10 bold", text = id)
                

class menu_button():
    def __init__(self, background, button_text, button_font, button_fg, button_bg, button_xcor, button_ycor, button_func):
        self.button = tk.Label(background, text = button_text, font = button_font, fg = button_fg, bg = button_bg)
        self.button.place(x = button_xcor, y = button_ycor, anchor = "center")
        self.button.bind("<Enter>", lambda event, button = self.button: button.configure(font = "Arial {} bold".format(int(button["font"].split(" ")[1]) + 5)))
        self.button.bind("<Leave>", lambda event, button = self.button: button.configure(font = button_font))
        self.button.bind("<Button-1>", lambda event: button_func(event))

class menu_label():
    def __init__(self, background, label_text, label_font, label_fg, label_bg, label_xcor, label_ycor):
        self.label = tk.Label(background, text = label_text, font = label_font, fg = label_fg, bg = label_bg)
        self.label.place(x = label_xcor, y = label_ycor, anchor = "center")

root = tk.Tk()
paint_game = paint_game(root)

root.mainloop()

