#import modules and initalise
import pygame
import time
import random
import math
import sys
import menu
GRAVITY=-9.8

pygame.init()

#display logo of game in dock
logo=pygame.image.load("minigolf.png")
pygame.display.set_icon(logo)

font = pygame.font.Font('freesansbold.ttf',16)

#Set up window
WINDOWX,WINDOWY=800,600
window=pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption('MINIGOLF!')

#set up backgorund and load in images
BACKGROUND=pygame.image.load('background.jpg')
FLAG=pygame.image.load('mgflag.png')
flag_dimensions=128
SAND=pygame.image.load('sand.png')
sand_dimensions=64
brown=(150,75,0)
dark_brown=(92,64,51)
sand_colour=255,202,4
#obstacles
x1=200; y1=400; height1=200; width1=10
x2=0; y2=500; height2=10; width2=100
x3=300;y3=300;height3=10;width3=250
x4=600;y4=500;height4=100;width4=15
x5=670;y5=500;height5=100;width5=15

#Games frame rate
FPS=60

#globals
level=5
all_scores = []

#class for aiming line/bar
class aimbar:
    WIDTH=10
    def __init__(self,originpos,finalpos):
        self.originpos=originpos
        self.finalpos=finalpos
        self.MAX_LEN=math.pow(2*(200)**2,1/2)
        self.draw_state=True

    def draw(self,window):
        if self.draw_state==True:           
            pygame.draw.line(window,(255,255,255),(self.originpos),self.finalpos)
   
    #calculates the length of the line
    def calc_distance(self):
        bar_len=math.pow(((self.finalpos[0] - self.originpos[0])**2 + (self.finalpos[1] - self.originpos[1])**2),1/2)
        if bar_len>self.MAX_LEN:
            bar_len=self.MAX_LEN
        return bar_len
    
    #calculates the angle of the ball
    def calc_angle(self):
        if self.finalpos[0]-self.originpos[0]==0: #if no change in x 
            if self.finalpos[1]>self.originpos[1]: #if going down
                angle=3*(math.pi)/2
            else:
                angle=(math.pi)/2
        else:
            x_change=self.finalpos[0]-self.originpos[0]
            y_change=self.finalpos[1]-self.originpos[1]
            perp_ratio=(-y_change/x_change) #get ratio of right angled triangle
            angle=math.atan(perp_ratio) #get the angle
            angle=self.fix_angle(angle) #correct the angle
        return(angle)
#converts angle to cartesian system
    def fix_angle(self,angle):
        new_angle=0
        if self.finalpos[0]-self.originpos[0]>0: #if quadrant 1 or 4
            if self.finalpos[1]-self.originpos[1]>0: #if quadrant 4
                new_angle=angle+2*math.pi
            else:
                new_angle=angle #quadrant 1
        elif self.finalpos[0]-self.originpos[0]<0: #if quadrant 2 or 3
                new_angle=angle+(math.pi)
        return new_angle

#ball object
class ball:
    ball_dimensions=16
    ball_img=pygame.image.load('golfball.png')
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.x_vel=0
        self.y_vel=0
        self.fire_state=False
        self.rolling_state=False
        self.draw_state=True
  
   #draws the ball onto the window
    def draw(self):
        if self.draw_state==True:
            window.blit(self.ball_img,(self.x,self.y))

    #defines the balls movement in air
    def ball_projectile(self,time,start_x,start_y,start_x_vel,start_y_vel):
        #SUVAT equations
        new_y_vel= int(start_y_vel+ GRAVITY*time)
        y=int(start_y - (start_y_vel*time +(GRAVITY/2 *(time)**2)))
        x=int(start_x_vel*time + start_x)
        return(x,y,int(start_x_vel),new_y_vel)
    
    #defines how the velocity changes when the ball rolls
    def roll(self,surface,time,start_x,start_v):
        acceleration=surface.coeff_of_friction*GRAVITY #finds accleration
        if start_v>0: #checks which way ball originally travels
            x=(start_v*time + (time**2)*acceleration/2) +start_x #SUVAT for new x
            new_v_sqred=(start_v)**2 +2*acceleration*(abs(x-start_x)) #Conservation of energy for new velocity squared
            if new_v_sqred<0:
                new_v_sqred=0 
            new_v=math.sqrt(new_v_sqred) #assigns direction based on that
        elif start_v<0:
            x=(start_v*time - (time**2)*acceleration/2) +start_x #SUVAT for new x
            new_v_sqred=(start_v)**2 +2*acceleration*(abs(x-start_x)) #Conservation of energy for new velocity squared
            if new_v_sqred<0:
                new_v_sqred=0             
            new_v=-math.sqrt(new_v_sqred)
        else:
            x=start_x
            new_v=start_v #if start_v 0 then return original x and velocity
        return(int(x),int(new_v))

#VECTORS functions
#gets the scalar product of two vectors
def scalar_product(v1,v2):
    x_comp=v1[0]*v2[0]
    y_comp=v1[1]*v2[1]
    scalar_product=x_comp+y_comp
    return(scalar_product)

#gets the magnitude of a vector
def get_magnitude(v):
    magnitude=math.sqrt((v[0])**2 + (v[1])**2)
    return magnitude

#finds a unit vector from the original vector
def get_unit_v(vector):
    magnitude=get_magnitude(vector)
    if magnitude!=0: #precondition 
        x=vector[0]/magnitude
        y=vector[1]/magnitude
    else:
        x=0
        y=0
    return(x,y)

#class for surfaces e.g. walls, or obstacles
class surface:
    def __init__(self,start_x,start_y,end_x,end_y,restitution,para_v,perp_v,cof):
        self.restitution=restitution
        self.start_x=start_x
        self.start_y=start_y
        self.end_x=end_x
        self.end_y=end_y
        self.para_vector=para_v
        self.perp_vector=perp_v
        self.coeff_of_friction=cof

    #check if the ball has collided
    def is_collided(self,x,y):
        if x in range(self.start_x,self.end_x): #check lies in width
            if y in range(self.start_y,self.end_y): #check lies in height
                return True
        return False
    
    #change speed of ball upon a collision with a surface
    def bounce(self,ball):
        ball_vector=(ball.x_vel,ball.y_vel) # convert vel components to a single vector
        para_projection=scalar_product(ball_vector,self.para_vector)
        perp_projection=scalar_product(ball_vector,self.perp_vector)
        v1_x=para_projection*self.para_vector[0]
        v1_y=para_projection*self.para_vector[1] # conserve velocity parallel
        v2_x=-self.restitution*perp_projection*self.perp_vector[0]
        v2_y=-self.restitution*perp_projection*self.perp_vector[1] # resitution on velocity perpendicular
        x_vel=v1_x+v2_x
        y_vel=v1_y+v2_y # get new velocity
        return(x_vel,y_vel)
    
    #finds how much to change the coordinates of the ball by to make it reset its position after a collision
    def add_after_collision(self,ball,difference):
        amount_to_add=abs(difference)
        ball_vector=(ball.x_vel,ball.y_vel)  
        perp_projection=scalar_product(ball_vector,self.perp_vector)
        v_x=-perp_projection*self.perp_vector[0]
        v_y=-perp_projection*self.perp_vector[1] # finds displacement vector needed to go to edge
        ball_vector=get_unit_v((v_x,v_y))
        x_addition=amount_to_add*ball_vector[0] + ball_vector[0]
        y_addition=amount_to_add*ball_vector[1] + ball_vector[1] #gets displacement vector to add to uncollide
        return(x_addition,y_addition)
    
#instantiating surface objects    
bottom_edge=surface(0,WINDOWY-ball.ball_dimensions+1,WINDOWX,WINDOWY*10,0.6,(1,0),(0,1),0.7)
left_edge=surface(0-WINDOWX*10,-WINDOWY*10,0,WINDOWY*10,0.9,(0,1),(1,0),0)
right_edge=surface(WINDOWX,0,WINDOWX*10+ball.ball_dimensions,WINDOWY*10,0.9,(0,1),(-1,0),0)
top_edge=surface(0,0,WINDOWX,20,0.9,(1,0),(0,-1),0)
sand_edge=surface(WINDOWX-flag_dimensions-sand_dimensions+7,WINDOWY-sand_dimensions+5,WINDOWX-flag_dimensions,WINDOWY,0,(1,0),(0,1),10)
block_1=surface(x1-ball.ball_dimensions,y1,x1+ball.ball_dimensions,y1+height1,0.6,(0,1),(-1,0),0)
block_2=surface(x2,y2-ball.ball_dimensions,x2+width2,y2+ball.ball_dimensions,0.6,(1,0),(0,1),0.7)
block_3=surface(x3,y3-ball.ball_dimensions,x3+width3,y3+ball.ball_dimensions,0.6,(1,0),(0,1),0.7)
block_4=surface(x4-ball.ball_dimensions,y4,x4+width4,y4+height4,0.8,(0,1),(-1,0),0)
block_5=surface(x5,y5,x5+width4,y5+height5,0.8,(0,1),(-1,0),0)
edges=[left_edge,right_edge,top_edge,bottom_edge,block_1,block_2,block_3,block_4,block_5,sand_edge]
roll_edges=[bottom_edge,block_2,block_3,sand_edge]
#draws obstacles,balls,background and other objects
def maindraw(window,ball,aimbar,power,stroke_counter,score_state,display,par,level):
    window.blit(BACKGROUND,(0,0))
    aimbar.draw(window)
    ball.draw()
    draw_power(aimbar,power)
    window.blit(FLAG,(WINDOWX-flag_dimensions,WINDOWY-flag_dimensions))
    window.blit(SAND,(WINDOWX-flag_dimensions-sand_dimensions,WINDOWY-sand_dimensions))
    pygame.draw.rect(window,brown,(x1,y1,width1,height1))
    pygame.draw.rect(window,brown,(x2,y2,width2,height2))
    pygame.draw.rect(window,brown,(x3,y3,width3,height3))
    pygame.draw.rect(window,brown,(x4,y4,width4,height4))
    pygame.draw.rect(window,brown,(x5,y5,width5,height5))
    pygame.draw.rect(window,sand_colour,(x4+width4,WINDOWY-sand_dimensions/2,x5-x4-width4,sand_dimensions/2))
    strokes=font.render(f"strokes: {str(stroke_counter)}",True,(255,255,255))
    par=font.render(f"par: {par}",True,(255,255,255))
    level=font.render(f"level: {level}",True,(255,255,255))
    window.blit(strokes,(10,10))
    window.blit(par,(10,30))
    window.blit(level,(WINDOWX-70,10))
    if score_state==True:
        window.blit(display,(WINDOWX/4,WINDOWY-WINDOWY/3))
    pygame.display.update()

#roll the ball on the ground
def roll_ball(roll_surface,ball,time,start_x,start_v):
    hit=False
    edge=0
    for surface in edges:
        if surface.is_collided(int(ball.x),int(ball.y))==True: #if ball hit any surface except roll surface
            hit=True
            edge=surface
            break
    #roll ball if hasnt collided
    if hit==False and roll_surface.is_collided(int(ball.x),int(ball.y)+10)==True:
        stats=ball.roll(roll_surface,time,start_x,start_v)
        ball.x=stats[0]
        ball.x_vel=stats[1]
    elif hit==False and roll_surface.is_collided(int(ball.x),int(ball.y)+10)==False:
        ball.rolling_state=False
        ball.fire_state=True #change to fire ball via projectile
        time=0
        start_v=ball.x_vel
        start_x=ball.x
    
    #if has collided then modify position and velocity
    else:
        difference=find_difference(ball,edge)    
        sum=edge.add_after_collision(ball,difference)
        ball.x=int(ball.x+sum[0])
        ball.y=int(ball.y-sum[1]) #reset position
        stats=edge.bounce(ball)
        ball.x_vel=stats[0] 
        ball.y_vel=stats[1]
        start_x=ball.x
        start_v=ball.x_vel
        time=0
    return(time,start_x,start_v)

#finds the difference between ball coordinates to an edge for the perp axis
def find_difference(ball,edge):
    if edge==bottom_edge:
        difference=ball.y-(bottom_edge.start_y)
    if edge==left_edge:
        difference=ball.x-left_edge.end_x
    if edge==right_edge:
        difference=ball.x-right_edge.start_x
    if edge==top_edge:
        difference=ball.y-top_edge.end_y
    if edge==sand_edge:
        difference=ball.y-(sand_edge.start_y)
    if edge==block_1:
        if ball.x_vel>0:
            difference=ball.x-block_1.start_x
        else:
            difference=ball.x-block_1.end_x
    if edge==block_2:
        if ball.y_vel>0:
            difference=ball.y-block_2.end_y
        else:
            difference=ball.y-block_2.start_y
    if edge==block_3:
        if ball.y_vel>0:
            difference=ball.y-block_3.end_y
        else:
            difference=ball.y-block_3.start_y
    if edge==block_4:
        if ball.x_vel>0:
            difference=ball.x-block_4.start_x
        else:
            difference=ball.x-block_4.end_x
    if edge==block_5:
        if ball.x_vel>0:
            difference=ball.x-block_5.start_x
        else:
            difference=ball.x-block_5.end_x
    return(difference)

#shoots the ball through air
def shoot_ball(ball,time,start_x,start_y,start_x_vel,start_y_vel):
    hit=False
    edge=0
    #check for a collision
    for surface in edges:
        if surface.is_collided(int(ball.x),int(ball.y))==True:
            hit=True
            edge=surface
   #when there is no collision call the projectile
    if hit==False:
        stats=ball.ball_projectile(time,start_x,start_y,start_x_vel,start_y_vel)
        ball.x=stats[0]
        ball.y=stats[1]
        ball.x_vel=stats[2] #update all the ball attributes following projectile movement.
        ball.y_vel=stats[3]
    elif abs(ball.y_vel)>10 or (edge not in roll_edges): #bouncing conditions
        difference=find_difference(ball,edge)
        sum=edge.add_after_collision(ball,difference)
        ball.x=ball.x+sum[0]
        ball.y=ball.y-sum[1] #reset position
        stats=edge.bounce(ball) #bounce
        ball.x_vel=stats[0]
        ball.y_vel=stats[1] #update stats
        start_x_vel=ball.x_vel
        start_y_vel=ball.y_vel 
        start_x=ball.x #give stats needed for redoing the algorithm
        start_y=ball.y
        time=0 #reset time to 0
    else:
        ball.fire_state=False 
        ball.rolling_state=True #set rolling state to true
        difference=find_difference(ball,edge)
        sum=edge.add_after_collision(ball,difference) #reset coordinates
        ball.y=ball.y-sum[1]
        ball.x=ball.x+sum[0] #update stats
        ball.y_vel=0
        start_x=ball.x
        start_y=ball.y
        start_x_vel=ball.x_vel
        start_y_vel=ball.y_vel 
        time=0 #reset time and pass in stats needed for redoing the algorithm
    return(time,start_x,start_y,edge,start_x_vel,start_y_vel)

#draw power bar and make line move corresponding to power
def draw_power(aimbar,power):
    BAR_LEN=100
    BAR_WIDTH=5
    start_y=580
    conversion_ratio=BAR_LEN/(aimbar.MAX_LEN)
    pygame.draw.rect(window,(255,0,0),(0,start_y,BAR_LEN,BAR_WIDTH))
    pygame.draw.rect(window,(255,255,0),(0,start_y,BAR_LEN*(2/3),BAR_WIDTH))
    pygame.draw.rect(window,(0,255,0),(0,start_y,BAR_LEN*(1/3),BAR_WIDTH))
    pygame.draw.line(window,(0,0,0),(power*conversion_ratio,580),(power*conversion_ratio,585))

#hide the aimbar if ball is moving   
def hide_aimbar(gball,aimbar):
    magnitude=get_magnitude((gball.x_vel,gball.y_vel))
    if magnitude==0:
        aimbar.draw_state=True
    else:
        aimbar.draw_state=False

#check angle range for rolling
def is_roll_angle(angle):
    if angle>=0 and angle<math.pi*1/36: # angle up at 5 degree max right side
        return True
    if angle>math.pi*71/36 and angle<=math.pi*2: #angle down at 5 degree max righ side
        return True
    if angle>math.pi*35/36 and angle<math.pi*37/36: #angle between 5 degree fluctuation left side
        return True
    return False

#check if ball can go in holl
def is_score(ball):
    x_change=ball.x-(WINDOWX-flag_dimensions+2*ball.ball_dimensions)
    y_change=ball.y-(WINDOWY-ball.ball_dimensions)
    distance=get_magnitude((x_change,y_change))
    speed=get_magnitude((ball.x_vel,ball.y_vel))
    if distance<15 and speed<100:
        return True
    return False

def which_popup(stroke_counter,par):
    popup_font=pygame.font.Font('freesansbold.ttf',50)
    white=(255,255,255)
    if stroke_counter==1:
        display=popup_font.render('hole in one!',True,white)
    elif stroke_counter==par-1:
        display=popup_font.render('birdie!',True,white)
    elif stroke_counter==par:
        display=popup_font.render('par!',True,white)
    elif stroke_counter==par+1:
        display=popup_font.render('bogey!',True,white)
    else:
        display=popup_font.render('congrats!',True,white)
    return(display)

#main event loop
def main(level,all_scores):
    running=True
    clock=pygame.time.Clock()
    gball=ball(100,WINDOWY-ball.ball_dimensions)
    time=0
    stroke_counter=0
    par=3
    score_state=False
    display=0
    while running:
        clock.tick(FPS)
        window.fill((0,0,0))
        #user input
        playerpos=pygame.mouse.get_pos()
        aimer=aimbar((gball.x+ball.ball_dimensions/2,gball.y),playerpos)
        hide_aimbar(gball,aimer)
        power=aimer.calc_distance()
        #draw stuff
        maindraw(window,gball,aimer,power,stroke_counter,score_state,display,par,level)
        #fire the ball
        if gball.fire_state==True:
            time+=0.15
            stats=shoot_ball(gball,time,start_x,start_y,start_x_vel,start_y_vel)
            time=stats[0]
            start_x=stats[1]
            start_y=stats[2]
            start_x_vel=stats[4]
            start_y_vel=stats[5]
            edge=stats[3]
       
       #roll the ball
        if gball.rolling_state==True:
            time+=0.15
            stats=roll_ball(edge,gball,time,start_x,start_x_vel)
            time=stats[0]
            start_x=stats[1]
            start_y_vel=0
            start_x_vel=stats[2]
            start_y=gball.y
            if abs(gball.x_vel)<2: #check if vel <2, if yes stop rolling
                gball.x_vel=0
                gball.rolling_state=False
                time=0

        #check if scored
        if is_score(gball)==True:
            gball.draw_state=False #stop drawing ball
            gball.x_vel=0
            gball.y_vel=1 # loophole to turn off aimbar draw
            gball.fire_state=False
            gball.rolling_state=False #stop moving ball
            score_state=True
            display=which_popup(stroke_counter,par)
        
        #change to leaderboard
        if score_state==True:
            time+=0.15
            if time>36:
                all_scores.append([level,stroke_counter,par])
                if level<5:
                    menu.scoreboard(level,all_scores)
                else:
                    name=random.choices(["rivan","rc_7","chanian"])
                    menu.leaderboard(name[0],all_scores)

        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    menu.main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                magnitude=get_magnitude((gball.x_vel,gball.y_vel))
                if magnitude==0: #check ball stationary
                    stroke_counter+=1
                    angle1=aimer.calc_angle()
                    power1=aimer.calc_distance() #find power and angle
                    if is_roll_angle(angle1)==True: #if angle is small then roll
                        if gball.rolling_state==False:
                            gball.rolling_state=True
                            start_x=gball.x
                            start_y=gball.y
                            if math.cos(angle1)>=0: #if going right
                                start_x_vel=power1/2
                            else:
                                 start_x_vel=-power1/2
                            time=0
                            start_y_vel=0 #inputs for roll function
                            for surface in edges:
                                if surface.is_collided(gball.x,gball.y+5)==True:
                                    edge=surface
                                    break
                                else:
                                    edge=bottom_edge #pseudo edge
                    elif gball.fire_state==False: #if angle large and fire state false
                            gball.fire_state=True
                            start_x=gball.x
                            start_y=gball.y
                            start_x_vel=math.cos(angle1)*power1/3
                            start_y_vel=math.sin(angle1)*power1/3 #inputs for shoot function
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main(level,all_scores)
