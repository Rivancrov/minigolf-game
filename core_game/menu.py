#import modules
import pygame
import sys
import game
from datetime import date
import csv
pygame.init()

#initialise window
WINDOWX,WINDOWY=800,600
window=pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption('MINIGOLF!')

#colours
light_green=(144,238,144)
gold=(255,223,0)
light_blue=(130,238,253)

#images
BACKGROUND=pygame.image.load('assets/menu_bg.jpeg')

#menu buttons defined
class button:
    def __init__(self,x,y,text):
        self.x=x
        self.y=y
        self.font=pygame.font.Font('freesansbold.ttf',32)
        self.colour=game.black
        self.txt_colour=game.white
        self.btn_text=self.font.render(text,True,self.txt_colour)
        self.button=self.btn_text.get_rect(center=(self.x,self.y))
    #draw buttons to screen 
    def draw(self,window):
        window.blit(self.btn_text,self.button)
        pygame.draw.rect(window,game.white,(self.x-120,self.y-18,250,36),2)

    #check if mouse on button
    def is_select(self,x,y):
        if x in range(self.button.left,self.button.right): #if x between box
            if y in range(self.button.top, self.button.bottom):#if y beteween box
                return True
        else:
            return False

#main menu game state
def main():
    running=True
    while running:
        #draw background and titlebo
        window.blit(BACKGROUND,(0,0)) #draw background
        player_pos=pygame.mouse.get_pos()
        title_font=pygame.font.Font('freesansbold.ttf',100)
        title=title_font.render("Minigolf",True,game.white)
        title_rect=title.get_rect(center=(WINDOWX/2,150)) #title 
        #draw buttons
        play_btn=button(WINDOWX/2,300,' Single player')
        ai_btn=button(WINDOWX/2,400,' VS AI')
        info_btn=button(WINDOWX/2,500,' information') #button instantiation
        play_btn.draw(window)
        ai_btn.draw(window)
        info_btn.draw(window)
        window.blit(title,title_rect) #draw title and buttons

        #event loop depending on button response
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if play_btn.is_select(int(player_pos[0]),int(player_pos[1]))==True: #if over game button
                    mg_game()
                if ai_btn.is_select(int(player_pos[0]),int(player_pos[1]))==True: #if over AI button
                    ai_game()
                if info_btn.is_select(int(player_pos[0]),int(player_pos[1]))==True: #if over info button
                    information()
        pygame.display.update()
    pygame.quit()
    sys.exit()

#main game state
def mg_game():
        game.main(1,[]) #start on level 1 with empty stats list

#AI vs human game state  
def ai_game():
        game.main_ai(1,[]) #start AI game on level 1

#information state
def information():
    running=True
    while running:
        window.fill(game.black)
        info=pygame.image.load('assets/information_state.png') #draw information image to screen
        window.blit(info,(0,0))
        #controls event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()

        pygame.display.update()
    pygame.quit()

#draws a grid of lines
def draw_grid(columns,rows,colour):
    for i in range(columns-1):
        x_pos=(i+1)*WINDOWX/(columns) #at n*window_width/columns intervals for integer n
        pygame.draw.line(window,colour,(x_pos,0),(x_pos,WINDOWY)) #draw lines going down down
    for i in range(rows-1):
        y_pos=(i+1)*WINDOWY/(rows) #at n*window_height/rows intervals for integer n
        pygame.draw.line(window,colour,(0,y_pos),(WINDOWX,y_pos))#draw lines across

#changes the index pos in a list of lists to that in another list
def change_list_item(list1,list2,index):
    i=0
    for list in list1: #loop over sublists
        list[index]=list2[i] #put list2 values into list in list1 at index pos
        i+=1
    return(list1)

#scoreboard state(after each level this will display)
def scoreboard_ai(level, all_scores,name):
    running=True
    level+=1 #increment level
    rows=game.LEVEL_TOTAL+1 #rows is levels + row for headings
    columns=4  # Add AI column
    column_headings=["level","human","AI","par"]
    red=(255,0,50)
    green=(0,255,50)
    blue=(0,150,255)
    
    while running:
        window.fill(game.black)
        #draw grid lines
        draw_grid(columns,rows,game.white)
        
        # Get AI scores
        ai_scores = getattr(sys.modules[__name__], 'ai_scores', [])
        
        #fills grid
        for i in range(columns):
            headings=game.font.render(column_headings[i],True,game.white) #draw the headings
            window.blit(headings,(i*WINDOWX/columns+WINDOWX/8,0+WINDOWY/(rows*2))) #offset position within a box to centre text
            
            #populate table with scores
            for j in range(len(all_scores)):
                if i == 0:  # Level column
                    item=game.font.render(str(all_scores[j][0]),True,game.white)
                elif i == 1:  # Human strokes
                    strokes=all_scores[j][1]
                    par=all_scores[j][2]
                    colour = green if strokes <= par else red
                    item=game.font.render(str(strokes),True,colour)
                elif i == 2:  # AI strokes
                    if j < len(ai_scores):
                        ai_strokes = ai_scores[j][1]
                        par=all_scores[j][2]
                        colour = green if ai_strokes <= par else red
                        item=game.font.render(str(ai_strokes),True,colour)
                    else:
                        item=game.font.render("-",True,game.white)
                else:  # Par column
                    item=game.font.render(str(all_scores[j][2]),True,game.white)
                
                window.blit(item,(i*WINDOWX/columns + WINDOWX/8,(j+1)*WINDOWY/rows + WINDOWY/(rows*2)))

        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()
                if event.key==pygame.K_c: #continuing ends game 
                    if level<=game.LEVEL_TOTAL: #if not at end go to AI game
                        game.main_ai(level,all_scores)
                    else: #if at end go to leaderboard
                        # Include AI in leaderboard
                        ai_scores = getattr(sys.modules[__name__], 'ai_scores', [])
                        if ai_scores:
                            ai_total = sum(score[1] for score in ai_scores)
                            # Add both human and AI to leaderboard
                            leaderboard_with_ai(name, all_scores, ai_total)
                        else:
                            leaderboard(name,all_scores)

        pygame.display.update()
    sys.exit()

def scoreboard(level, all_scores,name):
    running=True
    level+=1 #increment level
    rows=game.LEVEL_TOTAL+1 #rows is levels + row for headings
    columns=3
    column_headings=["level","strokes","par"]
    red=(255,0,50)
    green=(0,255,50)
    while running:
        window.fill(game.black)
        #draw grid lines
        draw_grid(columns,rows,game.white)
        #fills grid
        for i in range(columns):
            headings=game.font.render(column_headings[i],True,game.white) #draw the headings
            window.blit(headings,(i*WINDOWX/columns+WINDOWX/8,0+WINDOWY/(rows*2))) #offset position within a box to centre text
            #populate table with scores
            for j in range(len(all_scores)):
                strokes=all_scores[j][1]
                par=all_scores[j][2]
                if strokes<=par:
                    colour=green #green if strokes less or equal to par
                else:
                    colour=red #red if strokes more than par
                item=game.font.render(str(all_scores[j][i]),True,colour) #draw each item in the list of lists
                window.blit(item,(i*WINDOWX/columns + WINDOWX/8,(j+1)*WINDOWY/rows + WINDOWY/(rows*2))) #within box but offset to centre text

        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()
                if event.key==pygame.K_c: #continuing ends game 
                    if level<=game.LEVEL_TOTAL: #if not at end go to scoreboard
                        game.main(level,all_scores)
                    else: #if at end go to leaderboard
                        leaderboard(name,all_scores)

        pygame.display.update()
    sys.exit()

#function to rank a list of sublists by an index pos of sublist
def rank_leaderboard(list,index):
    sum_list=([int(x[index]) for x in list]) 
    list=change_list_item(list,sum_list,index) # change index pos item in each list to int
    list.sort(key=lambda x: x[index]) #sort list by index pos item in each list
    sum_list=([str(x[index]) for x in list])
    list=change_list_item(list,sum_list,index)#convert index pos item back to string
    return(list)

#leaderboard displaying 10 best scores with player name,score,date
def leaderboard(name,score_list):
    column_headings=["level","score","date"]
    list_to_sort=[]
    sum=0
    columns=3
    rows=11
    dat=str(date.today()) #get todays date
    for i in range(len(score_list)):
        sum+=score_list[i][1] #sum the strokes

    player_stats=[name,sum,dat] #make list with name,score,date

    #read csv file containing scores,names,dates and append to a list
    with open('core_game/leader_board.csv','r') as f:
        reader=csv.reader(f)
        for line in reader:
            list_to_sort.append(line)
    list_to_sort.append(player_stats)
    #reorders list so fewest stroke sum is first
    list_to_sort=rank_leaderboard(list_to_sort,1)
    #rewrites ranked list to csv for perma storage
    with open('core_game/leader_board.csv','w') as f:
        writer=csv.writer(f)
        for list in list_to_sort:
            writer.writerow(list)

    #event loop
    running=True
    while running:
        window.fill(game.black)
        draw_grid(columns,rows,game.white)
        for i in range(columns):
            headings=game.font.render(column_headings[i],True,gold) 
            window.blit(headings,(i*WINDOWX/columns+WINDOWX/8,0+WINDOWY/(rows*2))) #output headings
            #populate table with scores
            for j in range(min(len(list_to_sort),rows-1)): # at most 10 scores on leaderboard
                item=game.font.render(list_to_sort[j][i],True,game.white)
                window.blit(item,(i*WINDOWX/columns + WINDOWX/8,(j+1)*WINDOWY/rows + WINDOWY/(rows*2)))#draw leaderboard contents

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()
                if event.key==pygame.K_c:
                    main()

        pygame.display.update()
    sys.exit()

def leaderboard_with_ai(name, score_list, ai_total):
    """Leaderboard that includes both human and AI scores"""
    column_headings=["name","score","date"]
    list_to_sort=[]
    sum=0
    columns=3
    rows=11
    dat=str(date.today())
    
    # Calculate human total
    for i in range(len(score_list)):
        sum+=score_list[i][1]

    player_stats=[name,sum,dat]
    ai_stats=["AI",ai_total,dat]

    #read csv file containing scores,names,dates and append to a list
    with open('core_game/leader_board.csv','r') as f:
        reader=csv.reader(f)
        for line in reader:
            if line:  # Skip empty lines
                list_to_sort.append(line)
    
    # Add both human and AI
    list_to_sort.append(player_stats)
    list_to_sort.append(ai_stats)
    
    #reorders list so fewest stroke sum is first
    list_to_sort=rank_leaderboard(list_to_sort,1)
    
    #rewrites ranked list to csv for perma storage
    with open('core_game/leader_board.csv','w') as f:
        writer=csv.writer(f)
        for list in list_to_sort:
            writer.writerow(list)

    #event loop
    running=True
    while running:
        window.fill(game.black)
        draw_grid(columns,rows,game.white)
        for i in range(columns):
            headings=game.font.render(column_headings[i],True,gold) 
            window.blit(headings,(i*WINDOWX/columns+WINDOWX/8,0+WINDOWY/(rows*2))) #output headings
            #populate table with scores
            for j in range(min(len(list_to_sort),rows-1)): # at most 10 scores on leaderboard
                # Highlight AI entries
                if j < len(list_to_sort) and list_to_sort[j][0] == "AI":
                    color = light_blue
                else:
                    color = game.white
                item=game.font.render(list_to_sort[j][i],True,color)
                window.blit(item,(i*WINDOWX/columns + WINDOWX/8,(j+1)*WINDOWY/rows + WINDOWY/(rows*2)))#draw leaderboard contents

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()
                if event.key==pygame.K_c:
                    main()

        pygame.display.update()
    sys.exit()
        
if __name__ == '__main__':
    main()
