#import modules and initalise
import pygame
import time
import random
import math
import sys
import menu
import sys
sys.path.append('../ai_system')
import trained_ai

pygame.init()

#display logo of game in dock
logo=pygame.image.load("assets/minigolf.png")
pygame.display.set_icon(logo)

#level,stroke,par font
font = pygame.font.Font('freesansbold.ttf',16)

#Set up window
WINDOWX,WINDOWY=800,600
window=pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption('MINIGOLF!')

#set up backgorund and load in images
BACKGROUND=pygame.image.load('assets/background.jpg')
FLAG=pygame.image.load('assets/mgflag copy.png')
flag_dimensions=128
flag_centre=WINDOWX-(flag_dimensions-46)
SAND=pygame.image.load('assets/sand.png')
sand_dimensions=64

#obstacles positioning(brown blocks)
x1=200; y1=400; height1=200; width1=10
x2=0; y2=500; height2=10; width2=100
x3=300;y3=300;height3=10;width3=250
x4=600;y4=500;height4=100;width4=15
x5=670;y5=500;height5=100;width5=15

#Games frame rate
FPS=60

#globals
LEVEL_TOTAL=5
GRAVITY=-9.8
LEVEL_PAR=3

#colours
white=(255,255,255)
black=(0,0,0)
brown=(150,75,0)
dark_brown=(92,64,51)
sand_colour=(255,202,4)
red=(255,0,0)
yellow=(255,255,0)
green=(0,255,0)

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
            pygame.draw.line(window,white,(self.originpos),self.finalpos)
   
    #calculates the length of the line
    def calc_distance(self):
        bar_len=math.pow(((self.finalpos[0] - self.originpos[0])**2 + (self.finalpos[1] - self.originpos[1])**2),1/2)
        if bar_len>self.MAX_LEN: #cap the power
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
    ball_img=pygame.image.load('assets/golfball.png')
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
    
#instantiating surface objects(startx,starty,endx,endy,restitution,para vector,perp vector,friction)    
bottom_edge=surface(0,WINDOWY-ball.ball_dimensions+1,WINDOWX,WINDOWY*10,0.6,(1,0),(0,1),0.7) 
left_edge=surface(0-WINDOWX*10,-WINDOWY*10,0,WINDOWY*10,0.9,(0,1),(1,0),0)
right_edge=surface(WINDOWX,0,WINDOWX*10+ball.ball_dimensions,WINDOWY*10,0.9,(0,1),(-1,0),0)
top_edge=surface(0,0,WINDOWX,20,0.9,(1,0),(0,-1),0)
sand_edge=surface(WINDOWX-flag_dimensions-sand_dimensions+7,WINDOWY-sand_dimensions+5,WINDOWX-flag_dimensions,WINDOWY,0,(1,0),(0,1),10)
#wooden brown blocks
block_1=surface(x1-ball.ball_dimensions,y1,x1+ball.ball_dimensions,y1+height1,0.6,(0,1),(-1,0),0)
block_2=surface(x2,y2-ball.ball_dimensions,x2+width2,y2+ball.ball_dimensions,0.6,(1,0),(0,1),0.7)
block_3=surface(x3,y3-ball.ball_dimensions,x3+width3,y3+ball.ball_dimensions,0.6,(1,0),(0,1),0.7)
block_4=surface(x4-ball.ball_dimensions,y4,x4+width4,y4+height4,0.8,(0,1),(-1,0),0)
block_5=surface(x5,y5,x5+width4,y5+height5,0.8,(0,1),(-1,0),0)
edges=[left_edge,right_edge,top_edge,bottom_edge,block_1,block_2,block_3,block_4,block_5,sand_edge] #list of surface objects
roll_edges=[bottom_edge,block_2,block_3,sand_edge] #edges where rolling is allowed to happen

#draws obstacles,ball and other objects,background,stroke counter,displays and more
def maindraw(window,ball,aimbar,power,stroke_counter,score_state,display,par,level,draw_box_state,player_name):
    window.blit(BACKGROUND,(0,0))
    aimbar.draw(window)
    ball.draw()
    draw_power(aimbar,power) #power bar drawn
    window.blit(FLAG,(WINDOWX-flag_dimensions,WINDOWY-flag_dimensions))
    window.blit(SAND,(WINDOWX-flag_dimensions-sand_dimensions,WINDOWY-sand_dimensions))
    pygame.draw.rect(window,brown,(x1,y1,width1,height1)) #drawing wooden blocks
    pygame.draw.rect(window,brown,(x2,y2,width2,height2))
    pygame.draw.rect(window,brown,(x3,y3,width3,height3))
    pygame.draw.rect(window,brown,(x4,y4,width4,height4))
    pygame.draw.rect(window,brown,(x5,y5,width5,height5))
    pygame.draw.rect(window,sand_colour,(x4+width4,WINDOWY-sand_dimensions/2,x5-x4-width4,sand_dimensions/2))
    strokes=font.render(f"strokes: {str(stroke_counter)}",True,white) #draw current strokes,par,level 
    par=font.render(f"par: {par}",True,white)
    level=font.render(f"level: {level}",True,white)
    window.blit(strokes,(10,10))
    window.blit(par,(10,30))
    window.blit(level,(WINDOWX-70,10))
    if score_state==True:
        window.blit(display,(WINDOWX/4,WINDOWY-WINDOWY/3)) #popups at end of game
    if draw_box_state==True:
        box=pygame.Rect(WINDOWX/3,WINDOWY-100,140,50)
        box_text=font.render(player_name,True,black)
        box.w=max(200,box_text.get_width()+10) #expand box to text size
        pygame.draw.rect(window,black,box,2) #draw text box
        window.blit(box_text,(box.x+5,box.y+5)) #draw players name text
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
    #roll ball if hasnt collided and on top of something
    if hit==False and roll_surface.is_collided(int(ball.x),int(ball.y)+10)==True:
        stats=ball.roll(roll_surface,time,start_x,start_v)
        ball.x=stats[0]
        ball.x_vel=stats[1]
    #call fire state if hasnt collided and nothing below it
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
        stats=edge.bounce(ball) #change velocity
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
    
    #when theres a collision and conditions met
    elif abs(ball.y_vel)>10 or (edge not in roll_edges): #bouncing conditions
        difference=find_difference(ball,edge)
        sum=edge.add_after_collision(ball,difference)
        ball.x=ball.x+sum[0]
        ball.y=ball.y-sum[1] #reset position
        stats=edge.bounce(ball) #change velocity like a bounce
        ball.x_vel=stats[0]
        ball.y_vel=stats[1] #update stats
        start_x_vel=ball.x_vel
        start_y_vel=ball.y_vel 
        start_x=ball.x #give stats needed for redoing the algorithm
        start_y=ball.y
        time=0 #reset time to 0
   
   #when theres a collision and conditions not met
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
    pygame.draw.rect(window,red,(0,start_y,BAR_LEN,BAR_WIDTH))
    pygame.draw.rect(window,yellow,(0,start_y,BAR_LEN*(2/3),BAR_WIDTH))
    pygame.draw.rect(window,green,(0,start_y,BAR_LEN*(1/3),BAR_WIDTH))
    pygame.draw.line(window,black,(power*conversion_ratio,start_y),(power*conversion_ratio,start_y+BAR_WIDTH))

#hide the aimbar if ball is moving   
def hide_aimbar(gball,aimbar):
    magnitude=get_magnitude((gball.x_vel,gball.y_vel))
    if magnitude==0: #if no speed
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

#check if ball has been scored
def is_score(ball):
    x_change=ball.x-(flag_centre-ball.ball_dimensions/2)
    y_change=ball.y-(WINDOWY-ball.ball_dimensions)
    distance=get_magnitude((x_change,y_change)) #get distnace from ball to hole
    speed=get_magnitude((ball.x_vel,ball.y_vel))#find magnitude of velocity
    if distance<15 and speed<80:#conditions to score
        return True
    return False

#check how many strokes to display the correct popup
def which_popup(stroke_counter,par):
    popup_font=pygame.font.Font('freesansbold.ttf',50)#makes large popup text
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

#main and event loop
def main(level,all_scores):
    running=True
    clock=pygame.time.Clock()
    gball=ball(100,WINDOWY-ball.ball_dimensions) #instantiate ball
    time=0
    stroke_counter=0
    score_state=False
    display=0
    draw_box_state=False
    player_name='name:'
    while running:
        clock.tick(FPS)
        window.fill(black)
        #user input
        playerpos=pygame.mouse.get_pos()
        aimer=aimbar((gball.x+ball.ball_dimensions/2,gball.y),playerpos)#instantiate aimbar line
        hide_aimbar(gball,aimer) 
        power=aimer.calc_distance() #get power for power bar
        #draw stuff
        maindraw(window,gball,aimer,power,stroke_counter,score_state,display,LEVEL_PAR,level,draw_box_state,player_name)

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
            display=which_popup(stroke_counter,LEVEL_PAR)
        
        #change to scoreboard
        if score_state==True:
            time+=0.15
            if level>=5: #on last level get player name
                draw_box_state=True 
            else: #before last level go to scoreboard
                if time>27: #after time has passed
                    all_scores.append([level,stroke_counter,LEVEL_PAR])
                    menu.scoreboard(level,all_scores,player_name)

        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit game
                running=False
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e and draw_box_state==False:
                    menu.main() #escape to menu
                #gets players name
                if draw_box_state==True:
                    if event.key==pygame.K_BACKSPACE:
                        player_name=player_name[0:-1] # remove last character from name
                    elif event.key==pygame.K_RETURN:
                        player_name=player_name[5:] #get rid of name:
                        all_scores.append([level,stroke_counter,LEVEL_PAR])
                        menu.scoreboard(level,all_scores,player_name) #enter scoreboard state if return pressed
                    else:
                        player_name+=event.unicode #append to player name string

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
                                    break #once edge is detected break out of loop
                                else:
                                    edge=bottom_edge #pseudo edge so function can run
                    elif gball.fire_state==False: #if angle large and fire state false
                            gball.fire_state=True
                            #inputs for shoot function
                            start_x=gball.x
                            start_y=gball.y
                            start_x_vel=math.cos(angle1)*power1/3
                            start_y_vel=math.sin(angle1)*power1/3 
    sys.exit()

#AI vs Human game mode
def main_ai(level, all_scores):
    running = True
    clock = pygame.time.Clock()
    gball = ball(100, WINDOWY - ball.ball_dimensions)
    ai_player = trained_ai.PreTrainedAI()  # Use trained AI with learned strategies
    
    time = 0
    stroke_counter = 0
    ai_stroke_counter = 0
    score_state = False
    display = 0
    draw_box_state = False
    player_name = 'name:'
    current_player = 'human'  # 'human' or 'ai'
    ai_thinking = False
    ai_action = None
    ai_think_start_time = 0
    human_just_shot = False
    ai_just_shot = False
    ai_has_thought = False  # Prevent AI from thinking multiple times
    human_scored = False
    ai_scored = False
    
    while running:
        clock.tick(FPS)
        window.fill(black)
        
        # User input (only for human player)
        if current_player == 'human':
            playerpos = pygame.mouse.get_pos()
            aimer = aimbar((gball.x + ball.ball_dimensions/2, gball.y), playerpos)
            hide_aimbar(gball, aimer)
            power = aimer.calc_distance()
        else:
            # AI player - create dummy aimbar for display
            aimer = aimbar((gball.x + ball.ball_dimensions/2, gball.y), (gball.x, gball.y))
            aimer.draw_state = False
            power = 0
        
        # AI thinking logic - only when ball is completely stopped
        ball_speed = get_magnitude((gball.x_vel, gball.y_vel))
        if (current_player == 'ai' and not ai_thinking and not ai_has_thought and 
            ball_speed == 0 and not gball.fire_state and not gball.rolling_state):
            ai_thinking = True
            ai_has_thought = True
            import time as time_module
            ai_think_start_time = time_module.time()
            # Get AI action
            game_state = trained_ai.GameState(gball.x, gball.y, gball.x_vel, gball.y_vel, ai_stroke_counter)
            ai_action = ai_player.get_best_action(game_state)
        
        # Execute AI action after thinking time
        if ai_thinking and ai_action:
            import time as time_module
            if time_module.time() - ai_think_start_time > 1.0:  # 1 second thinking time
                ai_thinking = False
                ai_stroke_counter += 1
                
                angle1 = ai_action.angle
                power1 = ai_action.power
                
                if is_roll_angle(angle1):
                    if gball.rolling_state == False:
                        gball.rolling_state = True
                        start_x = gball.x
                        start_y = gball.y
                        if math.cos(angle1) >= 0:
                            start_x_vel = power1 / 2
                        else:
                            start_x_vel = -power1 / 2
                        time = 0
                        start_y_vel = 0
                        for surface in edges:
                            if surface.is_collided(gball.x, gball.y + 5) == True:
                                edge = surface
                                break
                            else:
                                edge = bottom_edge
                elif gball.fire_state == False:
                    gball.fire_state = True
                    start_x = gball.x
                    start_y = gball.y
                    start_x_vel = math.cos(angle1) * power1 / 3
                    start_y_vel = math.sin(angle1) * power1 / 3
                
                ai_just_shot = True  # Mark that AI just took a shot
        
        # Check if we need to switch players after ball stops
        ball_stopped = (get_magnitude((gball.x_vel, gball.y_vel)) == 0 and 
                       not gball.fire_state and not gball.rolling_state)
        
        if ball_stopped and not ai_thinking:
            if ai_just_shot:  # AI just finished shot
                current_player = 'human'
                ai_action = None
                ai_just_shot = False
                ai_has_thought = False  # Reset for next AI turn
            elif human_just_shot:  # Human just finished shot
                current_player = 'ai'
                human_just_shot = False
                ai_has_thought = False  # Allow AI to think on its turn
        
        # Draw current player indicator
        player_font = pygame.font.Font('freesansbold.ttf', 20)
        if current_player == 'human' and ball_stopped:
            player_text = player_font.render('Your Turn', True, white)
        elif ai_thinking:
            player_text = player_font.render('AI Thinking...', True, yellow)
        elif current_player == 'ai':
            player_text = player_font.render('AI Turn', True, red)
        else:
            player_text = player_font.render('Ball Moving...', True, white)
        
        # Draw everything
        maindraw(window, gball, aimer, power, stroke_counter, score_state, display, LEVEL_PAR, level, draw_box_state, player_name)
        window.blit(player_text, (WINDOWX - 150, 30))
        
        # AI stroke counter
        ai_strokes_text = font.render(f"AI strokes: {str(ai_stroke_counter)}", True, white)
        window.blit(ai_strokes_text, (10, 50))
        
        # Ball physics (same as original)
        if gball.fire_state == True:
            time += 0.15
            stats = shoot_ball(gball, time, start_x, start_y, start_x_vel, start_y_vel)
            time = stats[0]
            start_x = stats[1]
            start_y = stats[2]
            start_x_vel = stats[4]
            start_y_vel = stats[5]
            edge = stats[3]
       
        if gball.rolling_state == True:
            time += 0.15
            stats = roll_ball(edge, gball, time, start_x, start_x_vel)
            time = stats[0]
            start_x = stats[1]
            start_y_vel = 0
            start_x_vel = stats[2]
            start_y = gball.y
            if abs(gball.x_vel) < 2:
                gball.x_vel = 0
                gball.rolling_state = False
                time = 0

        # Check if scored
        if is_score(gball) == True and not score_state:
            if current_player == 'human' and not human_scored:
                human_scored = True
                # Reset ball for AI to continue
                gball.x = 100
                gball.y = WINDOWY - ball.ball_dimensions
                gball.x_vel = 0
                gball.y_vel = 0
                gball.fire_state = False
                gball.rolling_state = False
                gball.draw_state = True
                current_player = 'ai'
                ai_has_thought = False
                
            elif current_player == 'ai' and not ai_scored:
                ai_scored = True
                # Reset ball for human to continue (if they haven't scored)
                if not human_scored:
                    gball.x = 100
                    gball.y = WINDOWY - ball.ball_dimensions
                    gball.x_vel = 0
                    gball.y_vel = 0
                    gball.fire_state = False
                    gball.rolling_state = False
                    gball.draw_state = True
                    current_player = 'human'
                    
            # End level if both have scored or max strokes reached
            if (human_scored and ai_scored) or stroke_counter >= 8 or ai_stroke_counter >= 8:
                score_state = True
                gball.draw_state = False
                
                # Determine winner
                popup_font = pygame.font.Font('freesansbold.ttf', 40)
                if human_scored and ai_scored:
                    # Both scored - compare strokes (fewer strokes wins)
                    if stroke_counter < ai_stroke_counter:
                        display = popup_font.render('You Win!', True, green)
                    elif stroke_counter > ai_stroke_counter:
                        display = popup_font.render('AI Wins!', True, red)
                    else:
                        display = popup_font.render('Tie Game!', True, yellow)
                elif human_scored and not ai_scored:
                    # Only human scored - human wins
                    display = popup_font.render('You Win!', True, green)
                elif ai_scored and not human_scored:
                    # Only AI scored - AI wins
                    display = popup_font.render('AI Wins!', True, red)
                else:
                    # Nobody scored - it's a tie
                    display = popup_font.render('Nobody Scored!', True, white)
        
        # Change to scoreboard
        if score_state == True:
            time += 0.15
            if level >= 5:
                draw_box_state = True
            else:
                if time > 27:
                    all_scores.append([level, stroke_counter, LEVEL_PAR])
                    # Also track AI scores
                    ai_scores = getattr(menu, 'ai_scores', [])
                    ai_scores.append([level, ai_stroke_counter, LEVEL_PAR])
                    menu.ai_scores = ai_scores
                    menu.scoreboard_ai(level, all_scores, player_name)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and draw_box_state == False:
                    menu.main()
                if draw_box_state == True:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[0:-1]
                    elif event.key == pygame.K_RETURN:
                        player_name = player_name[5:]
                        all_scores.append([level, stroke_counter, LEVEL_PAR])
                        # Also track AI scores
                        ai_scores = getattr(menu, 'ai_scores', [])
                        ai_scores.append([level, ai_stroke_counter, LEVEL_PAR])
                        menu.ai_scores = ai_scores
                        menu.scoreboard_ai(level, all_scores, player_name)
                    else:
                        player_name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'human':
                magnitude = get_magnitude((gball.x_vel, gball.y_vel))
                if magnitude == 0:
                    stroke_counter += 1
                    angle1 = aimer.calc_angle()
                    power1 = aimer.calc_distance()
                    
                    if is_roll_angle(angle1) == True:
                        if gball.rolling_state == False:
                            gball.rolling_state = True
                            start_x = gball.x
                            start_y = gball.y
                            if math.cos(angle1) >= 0:
                                start_x_vel = power1 / 2
                            else:
                                start_x_vel = -power1 / 2
                            time = 0
                            start_y_vel = 0
                            for surface in edges:
                                if surface.is_collided(gball.x, gball.y + 5) == True:
                                    edge = surface
                                    break
                                else:
                                    edge = bottom_edge
                    elif gball.fire_state == False:
                        gball.fire_state = True
                        start_x = gball.x
                        start_y = gball.y
                        start_x_vel = math.cos(angle1) * power1 / 3
                        start_y_vel = math.sin(angle1) * power1 / 3
                    
                    human_just_shot = True  # Mark that human just took a shot
        
        pygame.display.update()
    sys.exit()
