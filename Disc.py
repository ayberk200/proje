import Collusions
from const import *
class Disc(Collusions.Collusions):
    def __init__(self,pos,angle,magnitude,mass,path,maxspeed,friction):
        Collusions.Collusions.__init__(self,pos,angle,magnitude,mass,path,maxspeed)
        self.__friction = friction   
    def get_friction(self):
        return self.__friction   
    def set_friction(self,friction):
        self.__friction = friction           
    def friction( self, dt):
        if self.get_speed_magnitude()>0:
            self.set_speed_magnitude(self.get_speed_magnitude()-self.get_friction()*dt)
        if self.get_speed_magnitude()<0:
            self.set_speed_magnitude(0)  
    def mod( self, dt):
        self.friction(dt)  
    def move( self, dt):
        new_pos = self.get_pos()+dt*self.get_speed()
        px,py = new_pos.get_xy()
        if not (GOAL_START<py<GOAL_END):
            if px < LIMIT_LEFT+self.get_width()*0.5:
                px = LIMIT_LEFT+self.get_width()*0.5
                self.set_speed_angle (180-self.get_speed_angle())
            elif px > LIMIT_RIGHT-self.get_width()*0.5:
                px = LIMIT_RIGHT-self.get_width()*0.5
                self.set_speed_angle (180-self.get_speed_angle())
        if (py < LIMIT_TOP+self.get_height()*0.5):
            py = LIMIT_TOP+self.get_height()*0.5
            self.set_speed_angle(360-self.get_speed_angle())   
        elif (py > LIMIT_BOTTOM-self.get_height()*0.5):
            py = LIMIT_BOTTOM-self.get_height()*0.5
            self.set_speed_angle(360-self.get_speed_angle())  
        self.set_pos_xy((px,py))
        
        if px < LIMIT_LEFT-self.get_width()*0.5:
            return 1
        elif px > LIMIT_RIGHT+self.get_width()*0.5:
            return 2
        return 0
