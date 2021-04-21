from robot import *
from random import random

#create_polygon: n edge polygon centered xp,yp and has radius r0
poly = []
poly0 = randomPolygon(400,200,100.,9)
poly.append(poly0)
poly1 = randomPolygon(600,500,100.,20)
poly.append(poly1)

def action(self,duration=100,time=1): 
    def get_closest_coordinate(self): #p1 is the point
        dmin=10.0**10
        for poly in self.env:
            for edge in poly.edges:
                u = self.getLineU(edge)
                if u<0.0:#en yakın uç noktasını kullan
                    px = edge.p1
                elif u>1.0:
                    px = edge.p2
                else:              #en yakın ara noktayı kullan
                    px = self.getPx(edge)
                d=px.getDistance(self.sensor)

                if dmin>d:
                    dmin=d
                    result = px
                del u,px,d
            del edge
        del poly
        return result,dmin
    def get_LHS_point(self,poly):
        distmax = 0
        vmax = self.tether.end()
        for edge in poly.edges:
            tether = Line(self,self.tether.end())
            if tether.getIntersection(edge):
                for p in [edge.p1,edge.p2]:
                    side,dist = p.getSide(tether)
                    if side=="left": #nokta solda kalıyor ise açısını bul
                       if abs(dist)>distmax:
                           distmax = abs(dist)
                           vmax = p
                    del side,dist,p
        del distmax
        return vmax
    ###########################################
    for j in range(duration):
        xy = self.getUltrasonic()
        if not xy==False:
            distance = self.sensor.getDistance(xy)
            if(distance<=20):
                break
        self.move(time)
    for i in range(j,duration):
        px,d=get_closest_coordinate(self)
        print(i,px.getXY(),d)
        self.rotation = atan2(px.y-self.y,px.x-self.x) + pi/2
        
        snappoint=get_LHS_point(self,self.env[0])
        self.tether.addAnchor(snappoint)
        snappoint=get_LHS_point(self,self.env[1])
        self.tether.addAnchor(snappoint)
        '''
        snappoint=get_LHS_point(self,self.env[1])
        if snappoint>-1 :
            self.tether.addAnchor(self.env[1].vertices[snappoint])
        snappoint=get_LHS_point(self,self.env[0])
        if snappoint>-1 :
            self.tether.addAnchor(self.env[0].vertices[snappoint])
            '''
        self.move(time)

Robot.action = action


window = Tk()
limitw = 1280
limith = 720
base = Canvas(window, bg ="white",width=limitw, height=limith)
base.pack()

rob = Robot(1000,650,10,-pi/1.05,poly,base)
rob.setV(20)
rob.setW(pi/300)
rob.action(1000,1)
################################

window.mainloop()
