# Note: Before running for the first time, the following command from terminal 
# could be necessary to avoid errors, depending on your OS and on installed libraries:
#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

# build environment
import os
os.chdir('/home/davide/Desktop/Reinforcement_L/exam')
import pygame
import time
import random

pygame.init()
red=(255,0,0)
black=(0,0,0) 

TESTING=False # if True, the game will run in test mode, with the parameters defined below
PLAYING=not TESTING # if True, the game will run in play mode, with the parameters defined below

# environment parameters:
if PLAYING:
    CAR_SPEED=1 # speed of your car. 1 is human speed
    POLICE_SPEED=3 # speed of the police cars. 3 is human speed
    DISPLAY_RESULT=True # do you want the results to be displayed at the end of the game?
    GAME_DIFF=0.1 # difficulty of the game: how much cars increase their speed. 0.1 is human difficulty
    DISPLAY_DEF=(840,650) # size of the display
    CAR_DEF=(104,200) # size of the car image
    EDGE=130 # size of the road edge
    
elif TESTING:
    CAR_SPEED=10
    POLICE_SPEED=30
    DISPLAY_RESULT=False
    GAME_DIFF=0.3
    DISPLAY_DEF=(20,10)
    CAR_DEF=(1,2)
    EDGE=0


display=pygame.display.set_mode(DISPLAY_DEF) 
pygame.display.set_caption("Play")  

#load car images
def policecar(police_x,police_y,police):
    if TESTING:
        police_come=pygame.image.load("car_images/car00.png").convert_alpha()
    elif PLAYING:
        if police==0:
            police_come=pygame.image.load("car_images/car2.png").convert_alpha()
        if police==1: 
            police_come=pygame.image.load("car_images/car3.png").convert_alpha()
        if police==2:
            police_come=pygame.image.load("car_images/car4.png").convert_alpha()
        if police==3:
            police_come=pygame.image.load("car_images/car5.png").convert_alpha()
        if police==4:
            police_come=pygame.image.load("car_images/car6.png").convert_alpha() 
        if police==5:
            police_come=pygame.image.load("car_images/car7.png").convert_alpha()
        if police==6:
            police_come=pygame.image.load("car_images/car8.png").convert_alpha()
    display.blit(police_come,(police_x,police_y))      #display the police car
 
# create the background
if TESTING:
    bg=pygame.image.load("car_images/background0.png")
elif PLAYING:
    bg=pygame.image.load("car_images/background.png")
def background():
    display.blit(bg,(0,0))
        
#create car function
if TESTING:
    carimg=pygame.image.load("car_images/car00.png").convert_alpha()
elif PLAYING:
    carimg=pygame.image.load("car_images/car0.png").convert_alpha()
def car(x,y): 
    """
    Displays the car in the position (x,y)
    """
    display.blit(carimg,(x,y))     #set position of the car
    
def crash(score): 
    """
    Displays the message "Game Over" with the game score, and restarts the game after 3 seconds
    """
    if DISPLAY_RESULT:      
        message_display("Game Over",score)
        time.sleep(3)           # Wait 3 seconds before starting a new game
    loop()                      #call the loop function to restart the game

def message_display(text,score): 
    """"
    Displays a message on the screen
    """    
    large_text=pygame.font.Font("freesansbold.ttf",DISPLAY_DEF[1]//8) # font style and size
    textsurf,textrect=text_object(text,large_text,red)     #set function to edit the message
    textsurf2,textrect2=text_object("Score: "+str(score),large_text,black)
    textrect.center=((DISPLAY_DEF[0]//2),(0.4*DISPLAY_DEF[1]))                      #set the position of the messages on the screen
    textrect2.center=((DISPLAY_DEF[0]//2),(0.6*DISPLAY_DEF[1]))
    display.blit(textsurf,textrect)                    #display the messages
    display.blit(textsurf2,textrect2)
    pygame.display.update()
    
# display the message after the car has crashed
def text_object(text,font,color):    
    text_surface=font.render(text,True,color)     #set color of the message
    return text_surface,text_surface.get_rect()   #after that restart the game & ready to give some input 



# main loop
def loop(): 
    score=0
    car_x=(DISPLAY_DEF[0]-CAR_DEF[0])/2   # initial position of the car
    car_y=DISPLAY_DEF[1]-CAR_DEF[1] 
    x_change=0                          #set changing position of the car
    policecar_speed=POLICE_SPEED             # starting speed of the police car
    police=random.randrange(0,6)        #starting stage for the police car 
    police_x=random.randrange(EDGE,(DISPLAY_DEF[0]-EDGE-CAR_DEF[0])) # police car will comes in x axis in random value 
    police_y=-DISPLAY_DEF[1]                       # police car will comes in y axis in negative value because car is coming from opposite side 
    police_width=0.8*CAR_DEF[0]                     # width of the police car
    police_height=0.85*CAR_DEF[1]                   # height of the police car
    
    while True:                   # start the game 
        for event in pygame.event.get():  # define the events
            if event.type==pygame.QUIT:          # quit
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:       # pressure of arrow keys
                if event.key==pygame.K_LEFT:        # left arrow:
                    x_change=-CAR_SPEED                     # car will move left side 1
                if event.key==pygame.K_RIGHT:       # right arrow:
                    x_change=CAR_SPEED                      # car will move right side 1
            if event.type==pygame.KEYUP:         # no pressure of arrow keys  
                x_change=0                          # stand still
        car_x+=x_change                       # move the car
        background()                      # display the background
        policecar(police_x,police_y,police) # display the police car
        police_y+=policecar_speed         # move the police car
        car(car_x,car_y)                          # display the car
        if car_x<EDGE or car_x>DISPLAY_DEF[0]-EDGE-CAR_DEF[0]:    # if the car is out of the road    
            crash(score)   # display game over and restart the game
        
        if police_y>DISPLAY_DEF[1]:     # if the police car is out of the screen
            score+=1
            policecar_speed+=GAME_DIFF*policecar_speed      # increases the speed of the police car at each iteration
            police_y=0-police_height  #only one car will cross the road in one time
            police_x=random.randrange(EDGE,(DISPLAY_DEF[0]-EDGE-CAR_DEF[0]))  #then other car will come in random position
            police=random.randrange(0,6)  # generate a new police car
            
        if car_y<police_y+police_height:
            if (police_x>=car_x and police_x<=car_x+CAR_DEF[0]) or (police_x+police_width>=car_x and police_x+police_width<=car_x+CAR_DEF[0]):
                crash(score)   
        
        pygame.display.update() # update the display
loop() # start the game
pygame.quit() 
quit()     