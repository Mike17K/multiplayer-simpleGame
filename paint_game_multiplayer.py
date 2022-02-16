import tkinter as tk
from tkinter.colorchooser import askcolor
import math as m
from network import Network


class paint_game():
    def __init__(self, root):

        self.net = Network()

        self.root = root
        self.root.title("Paint")
        self.root.geometry("+0+0")
        self.root.resizable(False, False)

        self.mouse = [0,0,0] #x,y pos of the mouse , state


        self.playground_height = self.root.winfo_screenheight()* 2 / 4
        self.playground_width = 1.5 * self.playground_height

        self.scaleFactor = [self.playground_width/1000,self.playground_height/1000]

        self.menu_background = tk.Frame(self.root, width = 100, height = int(100*self.scaleFactor[1]), bg = "black")
        self.menu_background.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.playground = tk.Canvas(self.root, width = self.playground_width, height = self.playground_height, bg = "white")
        self.playground.grid(row = 1, column = 0, sticky = tk.NSEW)
        
        
        self.canvas_color = "white"
        self.fill_pen_color = "black"
        self.outline_color = "black"
        self.pen_mode = "draw"
        self.widths_matrix = [1, 2, 3, 4, 5, 10, 20, 50]
        self.width = self.widths_matrix[0]
        self.playground.bind("<B1-Motion>", self.draw_with_pen)
        self.playground.bind("<MouseWheel>", self.adjust_width)
        self.playground.bind("<ButtonRelease-1>", self.unclick)
        self.playground.bind("<Button-1>", self.click)
        self.playground.bind("<Motion>",self.motion)
        self.create_menu()
        self.network()
        
    def create_menu(self):
        self.game_menu_raws = 12
        self.pen_eraser_button = menu_button(self.menu_background, "🖊", "Calibri "+str(int(25*self.scaleFactor[0]))+" bold", "white", "black", int(50*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_pen_eraser).button
        menu_label(self.menu_background, "Width:", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "red", "black", int(140*self.scaleFactor[0]), self.menu_background["height"] / 2)
        self.widths_button = menu_button(self.menu_background, self.width, "Arial "+str(int(28*self.scaleFactor[0]))+" bold", "white", "black", int(200*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_drawing_width).button
        menu_label(self.menu_background, "Canvas\nfill:", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "red", "black", int(280*self.scaleFactor[0]), self.menu_background["height"] / 2)
        self.canvas_color_button = menu_button(self.menu_background, "⬛", "Calibri "+str(int(28*self.scaleFactor[0]))+" bold", self.canvas_color, "grey", int(360*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_canvas_color).button
        menu_label(self.menu_background, "Pen color:", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "red", "black", int(480*self.scaleFactor[0]), self.menu_background["height"] / 2)
        self.fill_pen_color_button = menu_button(self.menu_background, "⬛", "Calibri "+str(int(28*self.scaleFactor[0]))+" bold", self.fill_pen_color, "grey", int(580*self.scaleFactor[0]), self.menu_background["height"] / 2, self.change_fill_pen_color).button
        self.clean_canvas_button = menu_button(self.menu_background, "clean\ncanvas", "Arial "+str(int(15*self.scaleFactor[0]))+" bold", "white", "black", int(920*self.scaleFactor[0]), self.menu_background["height"] / 2, self.clean_canvas).button

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
        self.pen_eraser_color = self.fill_pen_color
        self.fill_pen_color_button.configure(fg = self.fill_pen_color)
    def change_outline_color(self, event):
        color = askcolor(title = "Color Chooser")
        self.outline_color = color[1]
        self.outline_color_button.configure(fg = self.outline_color)
    def clean_canvas(self, event):
        self.playground.delete("all")
    def change_pen_eraser(self, event):
        if self.pen_mode == "draw":
            self.pen_mode = "erase"
            self.pen_eraser_button.configure(text = "⨂")
        elif self.pen_mode == "erase":
            self.pen_mode = "draw"
            self.pen_eraser_button.configure(text = "🖊")
    def click(self):
        self.mouse[2]=1
    def unclick(self):
        self.mouse[2]=0
    def draw_with_pen(self, event):
        # self.cellx = int(event.x * self.grid_columns / self.playground_width)
        # self.pen_xcor = (self.cellx + 0.5) * self.playground_width / self.grid_columns
        # self.celly = int(event.y * self.grid_raws / self.playground_height)
        # self.pen_ycor = (self.celly + 0.5) * self.playground_height / self.grid_raws
        ###########################
        self.cellx = int(event.x / (2 * self.width))
        self.pen_xcor = (self.cellx + 0.5) * (2 * self.width)
        self.celly = int(event.y / (2 * self.width))
        self.pen_ycor = (self.celly + 0.5) * (2 * self.width)
        ###########################
        # self.pen_xcor = event.x
        # self.pen_ycor = event.y
        if self.pen_mode == "draw":
            self.new_shape = self.playground.create_rectangle(self.pen_xcor - self.width, self.pen_ycor - self.width, self.pen_xcor + self.width, self.pen_ycor + self.width, fill = self.fill_pen_color, outline = self.fill_pen_color)
        elif self.pen_mode == "erase":
            self.new_shape = self.playground.create_rectangle(self.pen_xcor - self.width, self.pen_ycor - self.width, self.pen_xcor + self.width, self.pen_ycor + self.width, fill = self.canvas_color, outline = self.canvas_color)
        
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
        data += str(self.mouse[0])+","+str(self.mouse[1])+","
        data += self.pen_mode +","
        data += str(self.width) +","
        data += self.fill_pen_color+","
        data += str(self.mouse[2])
        

        #print("Data: "+data)
        reply = self.net.send(data)
        print("Data: ",reply)
        return reply

    def parse_data(self,data): # grid,mousepos of each player

        # width,height:0,0,00,0,0,00,00,000,00,00,000,0,00,00,0,0:id,posx,posy,color:..
        
        try:
            data=data.split(":")
            width = int(data[0].split(",")[0])
            height = int(data[0].split(",")[1])
            
            grid_pixel_dimentions = [self.playground_width/width,self.playground_height/height]

            grid_data = data[1].split(",") #array of colors of each pixel 
            for i in range(width*height):
                tmp_pos = [i%width,i//height]
                posX = tmp_pos[0]*self.playground_width/width
                posY = tmp_pos[1]*self.playground_height/height

                
                self.playground.create_rectangle(posX,posY,posX+grid_pixel_dimentions[0],posY+grid_pixel_dimentions[1],fill=grid_data[i],outline=grid_data[i])
                

            for cursor in data[2]:
                a=cursor.split(",")
                
                id=a[0]
                pos = [int(a[1])/1000*self.playground_width,int(a[2])/1000*self.playground_height]
                color = a[3]
                
                self.playground.create_oval(pos[0]-grid_pixel_dimentions[0],pos[1]-grid_pixel_dimentions[1],pos[0]+grid_pixel_dimentions[0],pos[1]+grid_pixel_dimentions[1],fill=color,outline=color)
                


            return True
        except Exception as e:
            print(e)
            return False
    
    def network(self):
        self.parse_data(self.send_data())
        self.root.after(200, self.network)



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

