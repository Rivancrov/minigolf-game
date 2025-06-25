import pygame
import sys
import game
from datetime import date
import csv
pygame.init()

WINDOWX,WINDOWY=800,600
window=pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption('MINIGOLF!')
light_green=(144,238,144)
BACKGROUND=pygame.image.load('menu_bg.jpeg')
#menu buttons defined
class button:
    def __init__(self,x,y,text):
        self.x=x
        self.y=y
        self.font=pygame.font.Font('freesansbold.ttf',32)
        self.colour=(0,0,0)
        self.txt_colour=(255,255,255)
        self.btn_text=self.font.render(text,True,self.txt_colour)
        self.button=self.btn_text.get_rect(center=(self.x,self.y))
    #draw buttons to screen 
    def draw(self,window):
        window.blit(self.btn_text,self.button)
        pygame.draw.rect(window,(255,255,255),(self.x-120,self.y-18,250,36),2)

    #check if mouse on button
    def is_select(self,x,y):
        if x in range(self.button.left,self.button.right):
            if y in range(self.button.top, self.button.bottom):
                return True
        else:
            return False

#main menu game state
def main():
    running=True
    while running:
        #draw background and title
        window.fill(light_green)
        window.blit(BACKGROUND,(0,0)) #draw background
        player_pos=pygame.mouse.get_pos()
        title_font=pygame.font.Font('freesansbold.ttf',100)
        title=title_font.render("Minigolf",True,(255,255,255))
        title_rect=title.get_rect(center=(WINDOWX/2,150)) #title 
        #draw buttons
        play_btn=button(WINDOWX/2,350,' Single player')
        info_btn=button(WINDOWX/2,500,' information') #button instantiation
        play_btn.draw(window)
        info_btn.draw(window)
        window.blit(title,title_rect) #draw title and buttons

        if play_btn.is_select(int(player_pos[0]),int(player_pos[1]))==True:
            #play_btn.txt_colour=
            pass
        #event loop depending on button response
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if play_btn.is_select(int(player_pos[0]),int(player_pos[1]))==True:
                    mg_game()
                if info_btn.is_select(int(player_pos[0]),int(player_pos[1]))==True:
                    information()
        pygame.display.update()
    pygame.quit()
    sys.exit()

#main game state
def mg_game():
        game.main(1,[])

#information state
def information():
    running=True
    while running:
        player_pos=pygame.mouse.get_pos()
        window.fill((0,0,0))

        font = pygame.font.Font('freesansbold.ttf',12)
        info_1=font.render("The objective is to put the ball into the hole in as few shots as possible,Aim by moving the mouse.Press down on the mouse once to shoot",True,(255,255,255))
        info_1_rect=info_1.get_rect(center=(WINDOWX/2,WINDOWY/2))
        window.blit(info_1,info_1_rect)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()

        pygame.display.update()
    pygame.quit()

#draws a grid of lines
def draw_grid(a,b,colour):
    for i in range(a):
        pygame.draw.line(window,colour,((i+1)*WINDOWX/(a+1),0),((i+1)*WINDOWX/(a+1),WINDOWY))
        for j in range(b):
            pygame.draw.line(window,colour,(0,(j+1)*WINDOWY/(b+1)),(WINDOWX,(j+1)*WINDOWY/(b+1)))

#scoreboard state(after each level this will display)
def scoreboard(level, all_scores):
    running=True
    level+=1
    game.level+=1
    column_headings=["level","strokes","par"]
    while running:
        window.fill((0,0,0))
        #draw grid lines
        draw_grid(2,5,(255,255,255))
        #print headings
        for i in range(3):
            headings=game.font.render(column_headings[i],True,(255,255,255))
            window.blit(headings,(i*WINDOWX/3+WINDOWX/8,0+WINDOWY/12))
            #populate table with scores
            for j in range(len(all_scores)):
                if all_scores[j][1]<=all_scores[j][2]:
                    colour=(0,255,50)
                else:
                    colour=(255,0,50)
                item=game.font.render(str(all_scores[j][i]),True,colour)
                window.blit(item,(i*WINDOWX/3+WINDOWX/8,(j+1)*WINDOWY/6 + WINDOWY/12))

        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()
                if event.key==pygame.K_c:
                    game.main(level,all_scores)

        pygame.display.update()
    pygame.quit()
    sys.exit

#leaderboard displaying best scores
def leaderboard(name,score_list):
    list_to_sort=[]
    sum=0
    dat=date.today()
    for i in range(len(score_list)):
        sum+=score_list[i][1]
    player_stats=[name,sum,dat]
    list_to_sort.append(player_stats)

    #read or write from file
    try:
        myFile = open("leader_board.txt", "r")
        text = myFile.read()
        rows = text.split("\n")
        for row in rows:
            curPlayerStats = row.split(",")
            list_to_sort.append(curPlayerStats)

    except:
        myFile = open("leader_board", "w")
        myFile.write("name,score,date")
        myFile.close()

    sorted_list = sorted(list_to_sort, key=lambda x: x[1])

    # write back sortedList
    myFile = open("leader_board.txt", "w")
    for row in sorted_list:
        rowStr = ""
        for i in range(len(row)):
            item = row[i]
            rowStr += item
            if i >= len(row):
                pass
            rowStr += ","
        myFile.write(rowStr + "\n")
    myFile.close()
        

    #rank csv and player_stats in terms of sum, sort list_to_sort.
    #display top 9 scores by iterating through list_to_sort and blitting text.
    
    #event loop
    running=True
    while running:
        window.fill((0,0,0))
        draw_grid(2,10,(255,255,255))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    main()
                if event.key==pygame.K_c:
                    main()

        pygame.display.update()
    pygame.quit()
    sys.exit
        
if __name__ == '__main__':
    main()
