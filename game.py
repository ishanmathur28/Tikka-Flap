with open('lyrics.txt','r') as fafe:
    temp_n=fafe.readlines()
    tempvar1=0
    temp_n3=[]
    for tempvr in temp_n:
        temp_n4=[]
        tempvar1+=1
        if tempvar1==2:
            temp_n4.append(tempvr.split('-->'))
        if tempvar1==3:
            temp_n4.append(tempvr)
        if tempvar1>3:
            tempvar1=0
        if tempvar1==2 or tempvar1==3:
            temp_n3.append(temp_n4)

import pygame
import random
pygame.init()
pygame.font.init()
pygame.mixer.init()

#
WIDTH, HEIGHT = 900, 524
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tikka Flap")

#Assets
#colours
score=0
score_font=pygame.font.SysFont('comicsans',35)
win_font=pygame.font.SysFont('comicsans',50)
lyri_font=pygame.font.SysFont('comicsans',30)
c1 = (235, 228, 228)
c2 = (181, 255, 224)
bg=pygame.transform.scale(pygame.image.load('background.png').convert(),(900,524))
bg_table=pygame.transform.scale(pygame.image.load('table.png').convert(),(898,355))
bg_object=pygame.transform.scale(pygame.image.load('object_straight.png').convert_alpha(),(70,123))
obstacle=pygame.transform.scale(pygame.image.load('obstacle.png').convert_alpha(),(85,112))
game_over=pygame.transform.scale(pygame.image.load('game_over.png').convert_alpha(),(250,212))
clock=pygame.time.Clock()

def timeconv(mils):
    s=mils/1000
    m,s=divmod(s,60)
    s=str(s)
    s=s.split('.')
    if len(s[0])==1:
        s[0]='0'+s[0]
    s=','.join(s)
    return ('00:0'+str(int(m))+':'+s)

def spawner(a,b):
  if a==0:
    obs_rec=obstacle.get_rect(center=(obs_pos+b,52))
  elif a>=1:
    obs_rec=obstacle.get_rect(center=(obs_pos+b,282))
  return obs_rec

def sec20():
    global obstacle_list
    t=0
    checker=[]
    while t<=20:
        obstacle_list2=[]
        jabs=0
        ba=random.randint(1,4)
        for i in range(0,ba):
           if jabs==800:
               break
           obstacle_list2.append(i)
           jabs+=200
        if obstacle_list2 in checker and len(checker)<=3:
            continue
        if len(checker)>3:
            checker.clear()
        checker.append(ba)
        for hass in obstacle_list2:
            obstacle_list.append(hass)
        t+=2.49

def rotate_tikka(tik):
	new_tik = pygame.transform.rotozoom(tik,-tikka_y * 3,1)
	return new_tik  

def tikka(a):
    global tikka_rect
    obj=a
    tikka_rect.centery+=tikka_y
    WIN.blit(obj,tikka_rect)
    
def obstacl(a):
    rand=random.randint(0,2)
    WIN.blit(obstacle,a)
    
def table():
    WIN.blit(bg_table,(table_pos,0))
    WIN.blit(bg_table,(table_pos+898,0))
   
def draw_window():
      global disqualified
      WIN.blit(bg,(0,0))
      score_text=score_font.render("Score: "+str(score),1,c1)
      WIN.blit(score_text,(30,450))
      if disqualified:
          with open('score.txt','r') as fosw23:
              hiscore=fosw23.readlines()
          hiscore=hiscore[0]
          hi_score=win_font.render('High Score: '+str(hiscore),1,c1)
          WIN.blit(hi_score,(320,380))
      
def animation(ohno):
    if ohno==0:
        tikka(bg_object)
        return
    tikka(rotate_tikka(bg_object))

def checkcollision(lol):
    if lol==0:
        obsss=obstacle.get_rect(center=(obs_pos,52))
    elif lol>=1:
      obsss=obstacle.get_rect(center=(obs_pos,282))
    collisiondetector.append(tikka_rect.colliderect(obsss))
    if len(collisiondetector)>16 and collisiondetector[-1:-14:-1].count(1)>12:
        global disqualified
        if disqualified!=1:
            pygame.mixer.Sound('sfx_eat.wav').play()
        pygame.time.wait(960)
        global space_pressed
        global score
        global ltime
        space_pressed=0
        disqualified=1
        ltime=pygame.time.get_ticks()
        score_refresh(score)
        pygame.mixer.music.load('dead.mp3')
        pygame.mixer.music.play(0, 0.0)
    if len(collisiondetector)>16:
        collisiondetector.clear()
        
def score_refresh(sca):
    with open('score.txt','+r') as forsw:
      x=forsw.readlines()
    if x!=[]:
      if int(x[0])<sca:
        with open('score.txt','w') as forsw2:
            forsw2.write(str(score))
    else:
      with open('score.txt','w') as forsw2:
          forsw2.write('0')
          
def lyri(txt):
    taxt=lyri_font.render(txt.strip(),1,c2)
    WIN.blit(taxt,(315,460))
    
def main():
  global ltime
  global table_pos
  global space_pressed
  global obs_pos
  global obstacle_list
  global time
  global score
  global tikka_x
  global tikka_y
  global disqualified
  sec20()
  run = True
  lyricopy=temp_n3.copy()
  checker=0
  bob=len(obstacle_list)
  while run:
    if bob==0:
        bob=len(obstacle_list)
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        pygame.quit()
        exit()
      if event.type==pygame.KEYDOWN:
          if event.key==pygame.K_UP and space_pressed==1:
            tikka_y=0
            tikka_y-=6
            pygame.mixer.Sound('wing.mp3').play()
            checker=1   
            
          if event.key==pygame.K_SPACE and space_pressed==0:
              space_pressed=1
          elif event.key==pygame.K_SPACE and space_pressed==1:
              space_pressed=0
       
    if disqualified==1 and space_pressed==1:
        pygame.mixer.music.stop()
        break
    draw_window()
    if space_pressed:
        table_pos-=1
        obs_pos-=2
        tikka_y+=gravity
    
    table()
    if table_pos<=-898:
        table_pos=0
    
    if time>19 or len(obstacle_list)<4:
        time=0
        sec20()
        
                
    if obstacle_list != []:
        bbb=0
        for j in obstacle_list:
          obstacl(spawner(j,bbb))
          bbb+=200
  
    if obs_pos<=-20 and space_pressed:
        obs_pos=obs_pos+200
        bob-=1
        score+=10
        pygame.mixer.Sound('point.mp3').play()
        plsnoo=obstacle_list.pop(0)
    if disqualified!=1 and space_pressed==1: 
      animation(space_pressed)
    elif disqualified!=1:
        WIN.blit(bg_object,tikka_rect)
    if not disqualified:
     if tikka_rect.centery>350 or tikka_rect.centery<0:
        space_pressed=0
        if disqualified!=1:
            pygame.mixer.music.load('dead.mp3')
            ltime=pygame.time.get_ticks()
            score_refresh(score)
            pygame.mixer.music.play(0, 0.0)
        disqualified=1
     else:
      checkcollision(obstacle_list[0])
    if disqualified==1 and space_pressed==0:
        WIN.blit(game_over,(320,120))
        pstime=pygame.time.get_ticks()-ltime
        pstime=timeconv(pstime)
        if len(lyricopy)<2:
            break
        tfra=lyricopy[0][0][0].strip()
        tfra2=lyricopy[0][0][1].strip()
        if pstime>=tfra and pstime<=tfra2:
            lyri(lyricopy[1][0])
        elif pstime>tfra2:
           plsnoooo=lyricopy.pop(0)
           plsnoooo2=lyricopy.pop(0)
    pygame.display.update()
    clock.tick(60)
    if space_pressed:
      time+=0.015
      
while True:  
  ltime=None
  table_pos=0
  space_pressed=0
  obj_pos=15
  obs_pos=827
  obstacle_list=[]
  score=0
  time=0
  gravity=0.25
  tikka_x,tikka_y=80,0
  tikka_rect=bg_object.get_rect(center=(tikka_x,115))
  collisiondetector=[]
  disqualified=0
  main()