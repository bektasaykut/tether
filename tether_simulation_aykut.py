from robot import *

poly = []
poly0 = randomPolygon(400,200,100.,9)
poly.append(poly0)
poly1 = randomPolygon(600,500,100.,20)
poly.append(poly1)

def action(self,duration,time=1):
    t=0
    hitted = False
    w = pi/100
    while(t<duration):
        xy = self.getUltrasonic()
        distance = self.sensor.getDistance(xy)
        
        if not hitted:
            if distance>=41:
                self.setV(20)
                self.setW(0)
            else:
                hitted = True
                self.setV(0)
                self.setW(w)
        else:
            if distance<=41:
                self.setV(0)
                self.setW(-w)
            else:
                self.setV(0)
                self.setW(w)
            
            


        print(hitted, xy.getXY(), distance)     
        t+=1
        self.move(time)
        

    
    

window = Tk()
limitw = 1280
limith = 720
base = Canvas(window, bg ="white",width=limitw, height=limith)
base.pack()
Robot.action = action

rob = Robot(1000,650,10,-pi/1.1,poly,base)

rob.setV(20)
rob.setW(pi/360)
rob.action(5000,0.2)
################################

window.mainloop()
