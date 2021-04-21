from math import pi, sin, cos, atan2, sqrt
from random import random
'''
http://paulbourke.net/geometry/pointlineplane/
Credits:
Point and line geometry theories by Paul Bourke
http://paulbourke.net/geometry/pointlineplane/DistancePointLine.delphi
'''
class Point(object):
    def __init__(self,x, y,radius=1):
        self.x = x
        self.y = y
        self.radius = radius
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getXY(self):
        return self.x, self.y
    def getDistance(self,p2):
        return sqrt((p2.x-self.x)**2 +(p2.y-self.y)**2)
        #return sqrt((p2.x-self.x)**2 +(p2.y-self.y)**2)-self.radius-p2.radius
    def getLineU(self,ln):
        x1,y1 = ln.p1.getXY()
        x2,y2 = ln.p2.getXY()
        px,py = self.getXY()
        return ((px-x1)*(x2-x1) + (py-y1)*(y2-y1)) / ln.getLength()**2
    def getPx(self,ln):
        u = self.getLineU(ln)
        if u==0:
            return self
        x1, y1, x2, y2 = ln.getXY()
        xc = x1 + u*(x2 - x1)
        yc = y1 + u*(y2 - y1)
        return Point(xc,yc)
    def lineDistance(self,ln):
        return self.getDistance(self.getPx(ln))
    def getSide(self, ln):
    #https://stackoverflow.com/a/3461499/2091924
        x1,y1 = ln.p1.getXY()
        x2,y2 = ln.p2.getXY()
        px,py = self.getXY()    
        check = ((x2 - x1)*(py - y1) - (y2 - y1)*(px - x1))
        if check > 0:
            return "right", check
        elif check<0:
            return "left", check
        else:
            return "on", check
    def draw(self,canvas,fill="white",r=2,width=1):
        canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill=fill,width=width)
class Line(object):
    def __init__(self, p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.length= self.p1.getDistance(self.p2)
    def getLength(self):
        self.length= self.p1.getDistance(self.p2)
        return self.length
    def getXY(self):
        return self.p1.x,self.p1.y, self.p2.x, self.p2.y
    def getPoints(self):
        return self.p1, self.p2
    def getIntersection(self,line):
        #http://paulbourke.net/geometry/pointlineplane/pdb.c
        x1,y1 = self.p1.getXY()
        x2,y2 = self.p2.getXY()
        x3,y3 = line.p1.getXY()
        x4,y4 = line.p2.getXY()
        ####################33
        #Check if none of the lines are of length 0
        if ((x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4)): 
            return False
        denominator  = ((y4-y3) * (x2-x1) - (x4-x3) * (y2-y1))
        #Lines are parallel
        if denominator == 0: 
            return  False
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator
        #is the intersection along the segments
        if (ua < 0 or ua > 1 or ub < 0 or ub > 1):
            return False
        #Return an object with the x and y coordinates of the intersection
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return Point(x, y)
    def getPolygonIntersection(self,poly):
        intersected = []
        ind = []
        for i in range(poly.number):
            intersection = self.getIntersection(poly.edges[i])
            if not intersection==False:
                intersected.append(intersection)
                ind.append(i)
        return intersected,ind
    def getDir(self):     
        #https://stackoverflow.com/a/49004181/2091924
        dx = (self.p2.x - self.p1.x) / self.getLength()
        dy = (self.p2.y - self.p1.y) / self.getLength()
        return Point(dx,dy)
    def getAngle(self):
        return atan2(self.p2.y - self.p1.y, self.p2.x - self.p1.x)
    def getAngleX(self,line):
        angle1 = self.getAngle()
        angle2 = line.getAngle()
        pass
    def draw(self,canvas,color='black',width=2):
        canvas.create_line(self.p1.x,
                           self.p1.y,
                           self.p2.x,
                           self.p2.y,
                           fill=color,
                           width=width)
    def getReverse(self):
        return Line(self.p2,self.p1)
class Polygon(object):
    def __init__(self,vertices):
        self.vertices = vertices
        self.edges = []
        self.number = len(vertices)
        if(len(vertices)>0):
            for i in range(len(vertices)):
                self.edges.append(Line(vertices[i],vertices[i-1]))
    def getEdges(self):
        return self.edges
    def getVertices(self):
        return self.vertices
    def draw(self,canvas,color="black"):
        for edge in self.edges:
            edge.draw(canvas,color)
            edge.p1.draw(canvas)
#create_polygon: n edge polygon centered xp,yp and has radius r0
def randomPolygon(xp,yp,r0,n):
    points = []
    for i in range(n):
        teta = pi * i*2.0/n
        r = r0+60.0*random()
        points.append(Point(xp+ r * cos(teta),yp+ r * sin(teta)))
    return Polygon(points)            
            