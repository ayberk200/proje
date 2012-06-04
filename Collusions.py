import math
import pygame
import Vector
from calculation import *

class Collusions:

    def __init__( self, pos, speed_angle, speed_magnitude, mass, path, max_speed):
        pos_angle = angle_from_O(pos)
        pos_magnitude = distance_from_O(pos)
        self.__pos = Vector.Vector(pos_angle,pos_magnitude)
        self.__image = pygame.image.load(path).convert_alpha()
        self.__width,self.__height = self.get_image().get_size()
        self.__radius = (self.get_width()+self.get_height())*0.25
        self.__speed = Vector.Vector(speed_angle,speed_magnitude)
        self.__mass = mass
        self.__max_speed = max_speed
        
        
    def get_pos(self):
        return self.__pos    
    def get_pos_angle(self):
        return self.get_pos().get_angle()    
    def get_pos_magnitude(self):
        return self.get_pos().get_magnitude()     
    def get_pos_xy(self):
        return self.get_pos().get_xy()  
    def get_image(self):
        return self.__image
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
    def get_radius(self):
        return self.__radius
    def get_speed(self):
        return self.__speed
    def get_speed_angle(self):
        return self.get_speed().get_angle()
    def get_speed_magnitude(self):
        return self.get_speed().get_magnitude()
    def get_speed_xy(self):
        return self.get_speed().get_xy()
    def get_mass(self):
        return self.__mass
    def get_max_speed(self):
        return self.__max_speed
      
    def set_pos(self,pos):
        self.__pos = pos
    def set_pos_angle(self,angle):
        self.get_pos().set_angle(angle)
    def set_pos_magnitude(self,magnitude):
        self.get_pos().set_magnitude(magnitude)
    def set_pos_xy(self,pos):
        self.get_pos().set_xy(pos)
    def set_image(self,image):
        self.__image = image
    def set_width(self,width):
        self.__width = width
    def set_height(self,height):
        self.__height = height
    def set_radius(self,radius):
        self.__radius = radius
    def set_speed(self,speed):
        self.__speed = speed
    def set_speed_angle(self,angle):
        self.get_speed().set_angle(angle)
    def set_speed_magnitude(self,magnitude):
        self.get_speed().set_magnitude(magnitude)
    def set_speed_magnitude(self,magnitude):
        self.get_speed().set_magnitude(magnitude)
    def set_speed_xy(self,speed):
        self.get_speed().set_xy(speed)
    def set_mass(self,m):
        self.__mass = m
    def set_max_speed(self,max_speed):
        self.__max_speed = max_speed
    def get_rect( self):
        px,py = self.get_pos_xy()
        return (px-(self.get_width()*0.5), py-(self.get_height()*0.5), self.get_width(),self.get_height())   
           
    def collision(self, B, dt):
    
        A = self
        if A.get_speed_magnitude()==0:
            (A,B)=(B,A)
        S = A.get_speed()-B.get_speed()
        dist = distance( A.get_pos_xy(), B.get_pos_xy())
        sumRadii = A.get_radius() + B.get_radius()
        dist -= sumRadii
        if S.get_magnitude()*dt < dist:
            return False
            
        N = S.copy()
        N.normalize()
        C = B.get_pos()-A.get_pos()
        D = N*C
        if D <= 0:
            return False
    
        N = C.copy()
        N.normalize()
        a1 = A.get_speed()*N
        a2 = B.get_speed()*N
        
        P = (2*(a1-a2))/(A.get_mass()+B.get_mass())
        newA = A.get_speed() - P*B.get_mass()*N
        newB = B.get_speed() + P*A.get_mass()*N
        
        A.set_speed(newA)
        B.set_speed(newB)
        
        if A.get_speed_magnitude()>A.get_max_speed():
            A.set_speed_magnitude(A.get_max_speed())
        if B.get_speed_magnitude()>B.get_max_speed():
            B.set_speed_magnitude(B.get_max_speed())
        
        return True

    def blit( self, screen):
        screen.blit( self.get_image(), self.get_rect())

