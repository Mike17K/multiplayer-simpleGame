import time


class Packet:
    def __init__(self,x,y,_id):
        self.id=_id
        self.x=x
        self.y=y

    def toString(self):
        return str(self.id)+":"+str(self.x)+","+str(self.y)

    @classmethod
    def toObject(cls,string):

        data=string.split(":")

        id=data[0]
        data=data[1].split(",")
        #print(data[0],data[1],id)
        return Packet(int(data[0]),int(data[1]),id)

    def copy(self,_packet):
        self.id=_packet.id
        self.x=_packet.x
        self.y=_packet.y

