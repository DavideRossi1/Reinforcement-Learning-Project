import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import Constants as C

class game():
    def __init__(self,length,width,car_length,car_width): # initialize the environment
        self.length=length # height of the environment
        self.width=width # width of the environment
        self.car_length=car_length # height of the car
        self.car_width=car_width # width of the car
        self.env=np.zeros((length,width),dtype=int)
        self.carposw=(self.width-self.car_width)//2 # position car in the center of the last row
        self.rendercar(1) # generate car
        self.generatepol() # generate police car
        self.score=0     
        self.maxscore=0
        
    def car_dist(self):
        return min((self.polposw-self.carposw)%self.width,(self.carposw-self.polposw)%self.width)
        
        
    def rendercar(self,bool): 
        """
        Render the car inside the environment: bool=1 to place it, bool=0 to remove it
        """
        for i in range(self.car_length):
            for j in range(self.car_width):
                self.env[self.length-1-i,(self.carposw+j)%self.width]=bool
    
    def renderpol(self,bool): 
        """
        Render the police car inside the environment: bool=1 to place it, bool=0 to remove it
        """
        for i in range(min(self.car_length,self.length-self.polposl)): # if police car is near the end, render only the part of the car that is in the environment
            for j in range(self.car_width):
                self.env[self.polposl+i,(self.polposw+j)%self.width]=bool
    
    def generatepol(self): 
        """
        Initialize the police car in a random position of the first row
        """
        self.polposl=0
        interval=self.width if C.PACMAN else self.width-self.car_width
        self.polposw=np.random.randint(interval) # position police car randomly in the first row
        self.renderpol(1)
         
    def movepol(self,speed): 
        """
        Move the police car along its line
        """
        gameover=False
        self.renderpol(0) # remove old police car
        if self.polposl+self.car_length+speed<=self.length-self.car_length: # police car is still entirely behind your car after moving
            self.polposl+=speed 
            self.renderpol(1)
        else:
            #print("#############",(self.polposw-self.carposw)%self.w,(self.carposw-self.polposw)%self.w,self.car_width-1)
            dist=self.car_dist() #if C.PACMAN else abs(self.polposw-self.carposw)
            if dist<=self.car_width-1: # police car crashes with car   
                gameover=True
            else:
                if self.polposl+speed<=self.length-1: # police car is still partially in the environment after moving
                    self.polposl+=speed
                    self.renderpol(1)
                else:
                    self.score+=1 # police car exits the environment
                    self.generatepol()
        return gameover
                
                
    def crash(self):  
        """
        Save results and reset environment after a crash
        """
        #print('GAME OVER, score: ',self.score)
        if self.score>self.maxscore: 
            self.maxscore=self.score
            print('New max score: ',self.maxscore)
        if C.SAVESCORES!=False:
            f=open(C.SAVESCORES,'a')
            f.write(str(self.score)+', '+str(self.maxscore)+'\n')
            f.close()
        self.env=np.zeros((self.length+1,self.width),dtype=int)
        self.carposw=(self.width-self.car_width)//2 
        self.rendercar(1)
        self.generatepol()
        self.score=0
        
    def movecar(self,action,carspeed): 
        """
        Move your car along the horizontal axis
        """
        gameover=False
        # for each action, check if the car didn't crash with the wall, then move the car
        match action:
            case 2: #left
                if self.carposw-carspeed>=0:
                    self.rendercar(0)
                    self.carposw-= carspeed
                    self.rendercar(1)   
                else:
                    gameover=True
                
            case 1: #right
                if self.carposw+self.car_width+carspeed<=self.width:
                    self.rendercar(0)
                    self.carposw+=carspeed
                    self.rendercar(1)
                else:
                    gameover=True
                
            case 0: #stay still
                pass
            case 4:
                if self.carposw-C.BOOST*carspeed>=0:
                    self.rendercar(0)
                    self.carposw-= C.BOOST*carspeed
                    self.rendercar(1)   
                else:
                    gameover=True
            case 3:
                if self.carposw+self.car_width+C.BOOST*carspeed<=self.width:
                    self.rendercar(0)
                    self.carposw+=C.BOOST*carspeed
                    self.rendercar(1)
                else:
                    gameover=True
                
                
        return gameover
    
    def movecarPM(self,action,carspeed):
        """
        Move your car along the horizontal axis with pacman effect
        """
        self.rendercar(0)
        match action:
            case 2: #left
                self.carposw=(self.carposw-carspeed)%self.width 
            case 1: #right
                self.carposw=(self.carposw+carspeed)%self.width      
            case 0: #stay still
                pass
            case 4: # left with boost
                self.carposw=(self.carposw-C.BOOST*carspeed)%self.width 
            case 3:
                self.carposw=(self.carposw+C.BOOST*carspeed)%self.width      

        self.rendercar(1)
        return False
    
    def playstep(self,action,carspeed,policespeed): 
        """
        Play a step of the game: move both cars and check if the game is over
        """
        gameover_wall=False
        gameover_pol=False
        reward=0
        gameover_wall=self.movecarPM(action,carspeed) if C.PACMAN else self.movecar(action,carspeed) # move your car and check if it crashed with the wall
        gameover_pol=self.movepol(policespeed)      # move police car and check if it crashed with your car
        gameover=gameover_wall or gameover_pol      # game is over if your car crashed with the wall or with the police car
        if gameover:
            self.crash()
            reward=-1000
        else:
            reward= 1*self.car_dist()/float(C.ENVSIZE[1]) + \
                   (0 if C.PACMAN else 2/(1+float(abs(self.carposw-C.ENVSIZE[1]/2))))-\
                    (100 if (action==3 or action==4) else 0)+\
                    (0 if (action==0) else -1)
                    
        if self.score>C.MAXSCORE:
            print('GAME WON, score: ',self.score)
            self.crash()
            reward+=1000
        return reward,gameover
    
    def render(self): 
        """
        Print the environment on terminal
        """
        for i in range(self.length):
            for j in range(self.width):
                print('|X' if self.env[i,j]==1 else '| ',end='')
            print('|\n')
        print('Score: ',self.score,'\n')   