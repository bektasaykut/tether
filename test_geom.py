from geom import *
from tkinter import *
def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvas.create_oval(x0, y0, x1, y1,fill="white",width=3)
p1 = Point(200,200)
p2 = Point(200,600)
p  = Point(400,300)
p4 = Point(100,300)
line = Line(p1,p2)
line2 = Line(p,p4)
px=p.getPx(line)
#px = line.getIntersection(line2)
print(px.getXY())
print(Line(p4,px).getLength())
print(px.getSide(line))

window = Tk()
limitw = 1280
limith = 1000
base = Canvas(window, bg ="white",width=limitw, height=limith)
base.pack()
p1.draw(base,"red",10,1)
p2.draw(base,"red",10,1)
del px,p
p.draw(base,"red",10,1)
px.draw(base,"blue",10,1)

line.draw(base,"black",5)
line2.draw(base,"black",5)


window.mainloop()