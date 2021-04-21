from math import pi, sin, cos, atan2, sqrt
from tkinter import *
from geom import *


################################
#tkinter drawing functions######
################################
def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvas.create_oval(x0, y0, x1, y1,fill="white",width=3)

    # canvas.create_line(rob.ultrasonic.x,rob.ultrasonic.y,500,500,fill="gray",dash=(4, 2))
    
    

class Tether(object):
    def __init__(self, x, y):
        self.anchors = [Point(x,y)]
    def move(self, x, y):
        self.end = Point(x,y)
    def end(self):
        return self.anchors[-1]
    def addAnchor(self,anc):
        self.anchors.append(anc)
        self.length = self.getLength()
    def getLength(self):
        length = 0
        for a in range(len(self.anchors)):
            length += self.anchors[a].getDistance(self.anchors[a-1])
        return length
    def draw(self,canvas):
        count = len(self.anchors)-1
        for a in range(count):
            Line(self.anchors[a],self.anchors[a+1]).draw(canvas)
class Robot(Point):
    def __init__(self, x, y,radius,rotation,env,canvas):
        Point.__init__(self, x, y, radius)
        self.rotation = rotation
        self.sensor = Point(self.x+self.radius*cos(self.rotation), self.y+self.radius*sin(self.rotation))
        self.tether = Tether(x,y);
        self.env = env
        self.canvas = canvas
    def setV(self,velocity):
        self.velocity = velocity
    def setW(self,angular_velocity):
        self.angular_velocity = angular_velocity
    def getV(self):
        return self.velocity
    def getW(self):
        return self.angular_velocity
    def getRot(self):
        return self.rotation
    def stop(self):
        self.velocity = 0
        self.angular_velocity = 0
    def move(self,time=1):
        self.x = self.x + time*self.velocity*cos(self.rotation)
        self.y = self.y + time*self.velocity*sin(self.rotation)
        self.sensor = Point(self.x+self.radius*cos(self.rotation), self.y+self.radius*sin(self.rotation))
        self.rotation = self.rotation + time*self.angular_velocity
        self.redraw_scene()
    def action(self):
        pass
    def getRange(self,urange,angle):
        distance = urange
        p2 = Point(self.sensor.x + urange*cos(angle), self.sensor.y+urange*sin(angle))
        result = p2
        dline = Line(self.sensor,p2)
        for poly in self.env:
            cross_points,ind= dline.getPolygonIntersection(poly)
            for p in cross_points:
                if self.sensor.getDistance(p) < distance:
                    distance = self.sensor.getDistance(p)
                    result = p
        return result
    def getLaser(self,urange=200):
        return self.getRange(urange,self.rotation)
    
    def getUltrasonic(self,urange=200,cone_width=30):
        distance = urange
        result = self.getRange(urange,self.rotation)
        step = 1
        for degree in range(0,cone_width+1,step):
            angle = degree-cone_width/2
            angle = pi*(angle/180)
            angle = self.rotation - angle
            rpoint = self.getRange(urange,angle)
            rdistance = self.sensor.getDistance(rpoint)
            if rdistance < distance:
                distance = rdistance
                result = rpoint
            del angle, rpoint, rdistance
        del step, degree
        return result
          
    def getLIDAR(self,n,lrange=200):
        distances = []
        
        return distances
        
    def draw(self):
        urange=200
        create_circle(self.x, self.y, self.radius, self.canvas)
        create_circle(self.x + self.radius*cos(self.rotation), self.y + self.radius*sin(self.rotation), 3, self.canvas)
        #red line in robot to show rotation
        self.canvas.create_line(self.x,
                                self.y,
                                self.x+self.radius*cos(self.rotation),
                                self.y+self.radius*sin(self.rotation),
                                fill="red",
                                width=3)
        #dashed line to show ultrasonic detection###############
        xy = self.getLaser()
        if not xy==False:
            self.canvas.create_line(self.sensor.x, self.sensor.y,
                                    xy.x, xy.y,
                                    fill="gray",
                                    dash=(4, 2))
        else:
            self.canvas.create_line(self.sensor.x, self.sensor.y,
                                    self.sensor.x + urange*cos(self.rotation), self.sensor.y+urange*sin(self.rotation),
                                    fill="gray",
                                    dash=(4, 2))
        cone_width=30
        angle = self.rotation - pi*((cone_width/2)/180)
        xy = self.getRange(urange, angle)
        if not xy==False:
            self.canvas.create_line(self.sensor.x, self.sensor.y,
                                    xy.x, xy.y,
                                    fill="gray",
                                    dash=(4, 2))
        else:
            self.canvas.create_line(self.sensor.x, self.sensor.y,
                                    self.sensor.x + urange*cos(angle), self.sensor.y+urange*sin(angle),
                                    fill="gray",
                                    dash=(4, 2))
        angle = self.rotation + pi*((cone_width/2)/180)
        xy = self.getRange(urange, angle)
        if not xy==False:
            self.canvas.create_line(self.sensor.x, self.sensor.y,
                                    xy.x, xy.y,
                                    fill="gray",
                                    dash=(4, 2))
        else:
            self.canvas.create_line(self.sensor.x, self.sensor.y,
                                    self.sensor.x + urange*cos(angle), self.sensor.y+urange*sin(angle),
                                    fill="gray",
                                    dash=(4, 2))
        #tether lines############################################
        self.tether.draw(self.canvas)
        Line(self, self.tether.anchors[-1]).draw(self.canvas)
    def redraw_scene(self):
        self.canvas.delete("all")
        for p in self.env:
            p.draw(self.canvas,"red")
        xy = self.getUltrasonic()
        if not xy==False:
            xy.draw(self.canvas)
        self.draw()
        self.canvas.update()
    def afterAction(self):
        pass
    def track(self):
        pass
    

