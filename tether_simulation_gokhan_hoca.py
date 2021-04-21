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
        return result,dmin
    def get_LHS_point(self,poly):
        x0,y0 = self.tether.end().getXY() #last pivot point, last tether anchor
        x1,y1 = self.getXY()
        tline = Line(self.tether.end(),self)
        a=y0-y1
        b=x1-x0
        c=(x0-x1)*y0+(y1-y0)*x0
        e=Line(self,self.tether.end()).getLength()
      
        angle0=atan2(y1-y0,x1-x0) #tether angle, line between robot and last pivot point
        anglemax=0.0
        imax=-1
        flag1=0
        flag2=0
        for i,v in enumerate(poly.vertices):
            tx,ty = v.getXY()
            d=(a*tx+b*ty+c)/e
            u=((tx-x0)*(x1-x0)+(ty-y0)*(y1-y0))/((x1-x0)**2+(y1-y0)**2)
            u = v.getLineU(tline)
            if d<0.0 and (u>0.001 and u<1.0): flag1=1
            if d>0.0 and (u>0.001 and u<1.0): flag2=1
            if d<=0.0: continue
            if u>0.001 and u<1.0: #nokta solda kalıyor ise açısını bul
                angle1=atan2(ty-y0,tx-x0)
                angle=angle1-angle0
                if angle>anglemax:
                    anglemax=angle
                    imax=i
        if flag1==0 or flag2==0:
            imax=-1
        return imax
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
      

        snappoint=get_LHS_point(self,self.env[1])
        if snappoint>-1 :
            self.tether.addAnchor(self.env[1].vertices[snappoint])
        snappoint=get_LHS_point(self,self.env[0])
        if snappoint>-1 :
            self.tether.addAnchor(self.env[0].vertices[snappoint])
        self.move(time)

Robot.action = action


window = Tk()
limitw = 1280
limith = 720
base = Canvas(window, bg ="white",width=limitw, height=limith)
base.pack()

rob = Robot(1000,650,10,-pi/1.1,poly,base)
rob.setV(20)
rob.setW(pi/300)
rob.action(1000,1) 
################################

window.mainloop()
