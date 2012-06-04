import pygame
from pygame.locals import *
import sys
import os

from const import *
from Mallet import *
from Disc import *
import cv

            
def init(angle=0):
    player1.set_pos_xy(PLAYER1_START)
    player1.set_speed_magnitude(0)
    player2.set_pos_xy(PLAYER2_START)
    player2.set_speed_magnitude(0)    
    disc.set_pos_xy((DISC_START_POS[0],DISC_START_POS[1]+disc.get_width()*0.5))
    disc.set_speed_angle(DISC_START_ANGLE+angle)
    disc.set_speed_magnitude(DISC_START_SPEED)
    if angle == 0:
        player1.set_point(0)
        player2.set_point(0)
        
def game():
    init()
    while 1:
        screen.blit( bg, (0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
          
        keys = pygame.key.get_pressed()
        if keys[ K_LEFT]: x1 = -1.0    
        elif keys[ K_RIGHT]: x1 = 1.0  
        else: x1 = 0.0                  
        if keys[ K_UP]: y1 = -1.0          
        elif keys[ K_DOWN]: y1 = 1.0       
        else: y1 = 0.0     
        if keys[ K_a]: x2 = -1.0    
        elif keys[ K_d]: x2 = 1.0  
        else: x2 = 0.0                  
        if keys[ K_w]: y2 = -1.0          
        elif keys[ K_s]: y2 = 1.0       
        else: y2 = 0.0
        if keys[ K_SPACE]: break
        if keys[K_q]:sys.exit()
        
        dt = clock.tick(60)
        camera()
        x1,y1=center_point
        x1=((2.39)*x1)-player1.get_pos_xy()[0]
        y1=((2.56)*y1)-player1.get_pos_xy()[1]
        x2,y2=center_point2
        x2=((2.39)*x2)-player2.get_pos_xy()[0]
        y2=((2.56)*y2)-player2.get_pos_xy()[1]
        #print count
        print (player1.get_pos_xy()[0]),(player1.get_pos_xy()[1])
        #print x1/dt,y1/dt
        player1.mod(x1/dt,y1/dt,dt)
        player2.mod(x2/dt,y2/dt,dt)
        disc.mod(dt)
        
        
        disc.collision(player1,dt)
        disc.collision(player2,dt)
        player1.move(dt)
        player2.move(dt)
        result = disc.move(dt)
        #result=0
    
        if result <> 0:
            goal(result)
        disc.blit(screen)
        player1.blit(screen,font1)
        player2.blit(screen,font1)
        pygame.display.update()
        
def goal(result):
    if result == 1:
        player2.inc_point()
        init(20)
    elif result == 2:
        player1.inc_point()
        init(-20)
    goal_message = "GOOOOOOOOLLLLLLL!!!"
    goal_label = font2.render(goal_message, 1, (255,0,0))
    screen.blit(goal_label,(WIDTH*0.5-goal_label.get_width()*0.5,HEIGHT*0.5))
    pygame.display.update()
    pygame.time.wait(2000)
    clock.tick(60) 
        
def end_game():
    if player1.get_point()>player2.get_point():
        end = "Player 1 win the game"
        end_label = font2.render(end, 1, (255,0,0))
    else: 
        end = "Player 1 win the game"
        end_label = font2.render(end, 1, (0,0,255))
    screen.blit(end_label,(WIDTH*0.5-end_label.get_width()*0.5,HEIGHT*0.5))
    pygame.display.update()
    pygame.time.wait(3000)     
    clock.tick(60)
def camera():
    global center_point
    global center_point2
    global count
    frame1=cv.QueryFrame(capture)
    #cv.Flip(frame1, None, 1)
    image_size = cv.GetSize(frame1)
    cv.CvtColor(frame1, hsv, cv.CV_BGR2YCrCb )
    cv.Split(hsv, h_plane, s_plane, None, None)
    cv.Threshold(h_plane, h_plane,180, 255, cv.CV_THRESH_BINARY)
    #cv.AbsDiff(h_plane3,h_plane2, h_plane)
    h_plane2=cv.CloneImage(h_plane3)
    cv.Dilate(h_plane, h_plane, None,10)
    cv.Erode(h_plane, h_plane, None, 1)

    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(h_plane, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    points = []
    count = 0
    while contour:
        count+=1
        bound_rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()

        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        points.append(pt1)
        points.append(pt2)
        if (bound_rect[0] + bound_rect[2]/2)>(image_size[0]/2):
            center_point=(bound_rect[0] + bound_rect[2]/2,bound_rect[1] + bound_rect[3]/2)
            cv.Circle(s_plane,center_point , 20, cv.CV_RGB(255, 255, 255), 1)
            print 1
        else:
            print 2
            center_point2=(bound_rect[0] + bound_rect[2]/2,bound_rect[1] + bound_rect[3]/2)
            cv.Circle(s_plane,center_point2 , 20, cv.CV_RGB(255, 255, 255), 1)
        #print '{0:4d} {1:4d} '.format(bound_rect[0] + bound_rect[2]/2, bound_rect[1] + bound_rect[3]/2)
        
    cv.ShowImage("h_plane", s_plane)
    #return center_point
    
        
pygame.init()


screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
bg = pygame.image.load(BG_PATH).convert()
clock = pygame.time.Clock()

player1 = Mallet(PLAYER1_START,MALLET_MASS,MALLET_RED_PATH,MALLET_MAX_SPEED,MALLET_ACCELERATION,MALLET_FRICTION,1)
player2 = Mallet(PLAYER2_START,MALLET_MASS,MALLET_BLUE_PATH,MALLET_MAX_SPEED,MALLET_ACCELERATION,MALLET_FRICTION,2)
disc = Disc(DISC_START_POS,DISC_START_ANGLE,DISC_START_SPEED,DISC_MASS,DISC_PATH,DISC_MAX_SPEED,DISC_FRICTION)

font1 = pygame.font.SysFont("Verdana", 16,True)
font2 = pygame.font.SysFont("Verdana", 40,True)

titlegame = "Press 1 to Start"
titlegamelabel = font2.render(titlegame, 1, (0,0,0))

cv.NamedWindow("h_plane", 1)
capture = cv.CaptureFromCAM(0)
frame1=cv.QueryFrame(capture)
#cv.Flip(frame1, None, 1)
hsv=cv.CreateImage(cv.GetSize(frame1), 8, 3)
h_plane=cv.CreateImage(cv.GetSize(frame1), 8, 1)
h_plane2=cv.CreateImage(cv.GetSize(frame1), 8, 1)
h_plane3=cv.CreateImage(cv.GetSize(frame1), 8, 1)
s_plane=cv.CreateImage(cv.GetSize(frame1), 8, 1)
center_point=PLAYER1_START
center_point2=PLAYER2_START
count=0
    
while 1:
    screen.blit( bg, (0,0))
    screen.blit(titlegamelabel,(WIDTH*0.5-titlegamelabel.get_width()*0.5,300))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            cv.DestroyWindow("camera")
            sys.exit()
    keys = pygame.key.get_pressed()
    dt = clock.tick(60)
    time = 0
    if keys[ K_1]: time = 1
    if time<>0:
         game()
                    
