from logging import exception
from turtle import delay
import pygame
from network import Network
from packet import *
import time

class Player():
    width = height = 50

    def __init__(self, startx, starty, _id ,color=(255,0,0)):
        self.id = _id
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color
    
    def aplyPacket(self, packet):
        self.id=packet.id
        self.x=packet.x
        self.y=packet.y

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def __init__(self, w, h):
        
        self.net = Network()
        self.width = w
        self.height = h

        
        self.players = [] 
        
        self.canvas = Canvas(self.width, self.height, "Testing...")
        
        self.createPlayer(50, 50, self.net.id) #create this player
        print("ID: ",self.net.id)
        time.sleep(2)

    def createPlayer(self,posX,posY,_id,color=(255,0,0)): #i can add more args later here and in the class above
        self.players.append(Player(posX,posY,_id,color))

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            self.player = self.players[0]
            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)

            # Send Network Stuff
            
            
            self.parse_data(self.send_data()) #sending all the other players the arguments
            

            
            # Update Canvas
            self.canvas.draw_background()
            for i in self.players: i.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        p=Packet(0,0,0)
        p.id=self.net.id
        p.x=self.players[0].x
        p.y=self.players[0].y
        #add more adributes if needed

        data = p.toString()

        #print("Data: "+data)
        reply = self.net.send(data)    #problemmm
        print("Reply: ",reply)
        return reply

    def parse_data(self,data): #data in form : ...@...@...@.. for each player
        #find the number by len if there are fewer player add one with the cordinates and id
        try:
            data=data.split("@")[:-1]
            print(data)
            for i in data:    
                p=Packet.toObject(i)
                
                ok=False
                for j in self.players:
                    if j.id==p.id:
                        j.aplyPacket(p)
                        ok=True
                        break

                    
                if not ok and len(data)>=len(self.players)+1:
                    #create new player
                    self.createPlayer(100,100,p.id)
                    self.players[-1].aplyPacket(p)

                    print("player spawned")

                

                del p
            
            if len (data)<len(self.players):
                for k in self.players:
                    ok =False
                    for h in data:
                        if k.id==h.split(":")[0]:
                            ok=True
                    if not ok:
                        self.players.remove(k)

            return True
        except Exception as e:
            print(e)
            return False


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)
        pygame.display.flip()


    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
