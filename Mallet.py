import Disc
from const import *
from calculation import *

class Mallet(Disc.Disc):

    def __init__( self, pos, mass, path, max_speed, acceleration, friction, player):
        Disc.Disc.__init__( self, pos, 0, 0, mass, path, max_speed, friction)
        self.__acceleration = acceleration
        self.__player = player
        self.__point = 0    
    def get_acceleration(self):
        return self.__acceleration
    def get_player(self):
        return self.__player
    def get_point(self):
        return self.__point       
    def set_acceleration(self,acceleration):
        self.__acceleration = acceleration
    def set_player(self,player):
        self.__player = player
    def set_point(self,point):
        self.__point = point      
    def inc_point(self):
        self.__point += 1
    def mod( self, x, y, dt):
       
        Disc.Disc.friction(self,dt)
        vx,vy = self.get_speed_xy()
        vx += x*self.get_acceleration()*dt
        vy += y*self.get_acceleration()*dt
        self.set_speed_angle(angle_from_O((vx,vy)))
        new_speed = distance_from_O((vx,vy))
        if new_speed<=self.get_max_speed():
            self.set_speed_magnitude (new_speed)
    def move( self, dt):
        touched = 0
        new_pos = self.get_pos()+dt*self.get_speed()
        px,py = new_pos.get_xy()
        if (py < LIMIT_TOP+self.get_height()*0.5):
            touched = 1
            py = LIMIT_TOP+self.get_height()*0.5
        elif (py > LIMIT_BOTTOM-self.get_height()*0.5):
            touched = 1
            py = LIMIT_BOTTOM-self.get_height()*0.5
            
        if self.get_player() == 1:
            limit_left = LIMIT_LEFT+0.5*(FIELD_WIDTH+self.get_width())
            limit_right = LIMIT_LEFT+FIELD_WIDTH-0.5*self.get_width()
        else:
            limit_left = LIMIT_LEFT+0.5*self.get_width()
            limit_right = LIMIT_LEFT+0.5*(FIELD_WIDTH-self.get_width())
        
        if (px < limit_left):
            touched = 1
            px = limit_left
        elif (px > limit_right):
            touched = 1
            px = limit_right
            
        if (touched==1):
            old_pos = self.get_pos_xy()
            self.set_speed_angle(angle(old_pos,(px,py)))
            self.set_speed_magnitude(distance(old_pos,(px,py))/dt)
        
        self.set_pos_xy((px,py))
        
    def __str__(self):
        if self.get_player()==1:
            return playername[0]+": "+str(self.get_point())
        else:return playername[1]+": "+str(self.get_point())
    
    def blit( self, screen, font):
        Disc.Disc.blit( self, screen)
        screen.blit( font.render( self.__str__(), 1, PLAYER_LABEL_COLOR[self.get_player()-1]), PLAYER_LABEL_POS[self.get_player()-1])
