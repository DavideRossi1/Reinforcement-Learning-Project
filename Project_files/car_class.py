import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import Constants as C

class game():
    """
    This class represents the environment of the game. It is a matrix of zeros, where 1 represents the position of the cars.
    The class also contains the methods to move the cars and to check if the game is over and restart it.
    """
    
    
    def __init__(self, height, width, car_height, car_width):
        """
        Initialize the environment by setting the height and width of the environment and the 
        height and width of the cars, which we assume to be equally sized.
        Car position variables refer to the top left corner of the car.
        """
        self.height=height                                 # height of the environment
        self.width=width                                   # width of the environment
        self.car_height=car_height                         # height of the cars
        self.car_width=car_width                           # width of the cars
        self.env=np.zeros((height,width),dtype=int)        # initialize the environment as a matrix of zeros
        self.car_x_position=(self.width-self.car_width)//2 # position your car in the center of the last row
        self.render_car(1)                                 # generate car
        self.generate_enemy_car()                          # generate enemy car
        self.score=0     
        self.maxscore=0
        
        
        
    def render_car(self,bool): 
        """
        Render the car inside the environment: bool=1 to place it, bool=0 to remove it
        """
        for i in range(self.car_height):
            # compute the current line to render
            current_line=self.height-1-i
            
            for j in range(self.car_width):
                # use %self.width to account for the possibility of car to exit the environment from one side and re-enter from the opposite side
                self.env[current_line, (self.car_x_position+j)%self.width]=bool
    
    
    
    def render_enemy_car(self,bool): 
        """
        Render the enemy car inside the environment: bool=1 to place it, bool=0 to remove it
        """
        # if enemy car is near the end, render only the part of the car that is still inside the environment
        highest_position=min(self.car_height, self.height-self.enemy_y_position)
        
        for i in range(highest_position): 
            for j in range(self.car_width):
                # use %self.width to account for the possibility of car to exit the environment from one side and re-enter from the opposite side
                self.env[self.enemy_y_position+i,(self.enemy_x_position+j)%self.width]=bool
    
    
    
    def generate_enemy_car(self): 
        """
        Initialize the enemy car in a random position of the first row
        """
        
        # position enemy in the first row...
        self.enemy_y_position=0
        
        interval=self.width if C.PACMAN else self.width-self.car_width
        
        # ... in a random position
        self.enemy_x_position=np.random.randint(interval) 
        self.render_enemy_car(1)
        
        

    def car_distance(self):
        """
        Return the minimum horizontal distance between a side of your car and a side of the enemy car
        """
        left_distance= (self.enemy_x_position-self.car_x_position)%self.width
        right_distance=(self.car_x_position-self.enemy_x_position)%self.width
        return min(left_distance,right_distance)
        
         
    def move_enemy_car(self,speed): 
        """
        Move the enemy car along its vertical line with the given speed, and return the game status
        """
        gameover=False
        
        # remove old enemy
        self.render_enemy_car(0) 
        
        # if enemy is still entirely behind you after moving...
        if self.enemy_y_position+self.car_height+speed<=self.height-self.car_height: 
            # ...simply move it
            self.enemy_y_position+=speed 
            self.render_enemy_car(1)
        else:
            
            # check the horizontal distance between the two cars
            distance=self.car_distance()
            
            # the two cars are too close: crash!
            if distance<=self.car_width-1:   
                gameover=True
            else:
                
                # enemy car is still partially in the environment after moving
                if self.enemy_y_position+speed<=self.height-1: 
                    self.enemy_y_position+=speed
                    self.render_enemy_car(1)
                else:
                    
                    # enemy car exits the environment: increase score and generate a new enemy car
                    self.score+=1 
                    self.generate_enemy_car()
                    
        return gameover
                
               
                
    def crash(self):  
        """
        Save results and reset environment after a crash
        """
        
        # update the max score
        if self.score>self.maxscore: 
            self.maxscore=self.score
            print('New max score: ',self.maxscore)
            
        # save the new score in the specified file
        if C.SAVESCORESNAME!=0:
            f=open(C.SAVESCORES,'a')
            f.write(str(self.score)+', '+str(self.maxscore)+'\n')
            f.close()
            
        # reset the environment
        self.env=np.zeros((self.height+1,self.width),dtype=int)
        self.car_x_position=(self.width-self.car_width)//2 
        self.render_car(1)
        self.generate_enemy_car()
        self.score=0
        
        
        
    def movecar(self,action,carspeed): 
        """
        Move your car along the horizontal axis, following the given 
        action and with the given speed, and return the game status
        """
        gameover=False
        
        # for each action, check if the car didn't crash with the wall, then move the car
        match action:
            
            case 0: #stay still
                pass
            
            case 1: #right
                
                # if the car is still entirely inside the environment after moving...
                if self.car_x_position+self.car_width+carspeed<=self.width:
                    
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.render_car(0)
                    self.car_x_position+=carspeed
                    self.render_car(1)
                else:
                    # car crashed with the wall: game is over
                    gameover=True
            
            case 2: #left
                
                # if the car is still entirely inside the environment after moving...
                if self.car_x_position-carspeed>=0:
                    
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.render_car(0)
                    self.car_x_position-= carspeed
                    self.render_car(1)   
                else:
                    # car crashed with the wall: game is over
                    gameover=True
                    
            case 3: #right with boost
                
                # if the car is still entirely inside the environment after moving...
                if self.car_x_position+self.car_width+C.BOOST*carspeed<=self.width:
                    
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.render_car(0)
                    self.car_x_position+=C.BOOST*carspeed
                    self.render_car(1)
                else:
                    # car crashed with the wall: game is over
                    gameover=True
                
            case 4: #left with boost
                
                # if the car is still entirely inside the environment after moving...
                if self.car_x_position-C.BOOST*carspeed>=0:
                    
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.render_car(0)
                    self.car_x_position-= C.BOOST*carspeed
                    self.render_car(1)   
                else:
                    # car crashed with the wall: game is over
                    gameover=True
                
        return gameover
    
    def movecarPM(self,action,carspeed):
        """
        Move your car along the horizontal axis in a continuous space, following 
        the given action and with the given speed, and return the game status
        """
        self.render_car(0)
        
        # for each action, check if the car didn't crash with the wall, then move the car
        # What happens is basically the same as in the movecar function, but the car can exit 
        # the environment from one side and re-enter from the opposite side, hence the position 
        # of the car is computed as the remainder of the division by the width of the environment 
        # and no crash with the wall is possible
        match action:
            
            case 0: #stay still
                pass
            
            case 1: #right
                self.car_x_position=(self.car_x_position+carspeed)%self.width     
                
            case 2: #left
                self.car_x_position=(self.car_x_position-carspeed)%self.width 
             
            case 3: # right with boost
                self.car_x_position=(self.car_x_position+C.BOOST*carspeed)%self.width  
                
            case 4: # left with boost
                self.car_x_position=(self.car_x_position-C.BOOST*carspeed)%self.width 
                
        self.render_car(1)
        
        # game is never over in this case: you can't crash with the wall
        return False
    
    
    
    def playstep(self,action,carspeed,enemyspeed): 
        """
        Play a step of the game: move both cars and check if the game is over
        """
        
        # move your car and check if it crashed with the wall
        gameover_wall = self.movecarPM(action,carspeed) if C.PACMAN \
                   else self.movecar(action,carspeed) 
        
         # move enemy car and check if it crashed with your car
        gameover_car = self.move_enemy_car(enemyspeed)     
        
        # game is over if your car crashed with the wall or with the enemy car
        gameover = gameover_wall or gameover_car      
        if gameover:
            self.crash()
            reward=-1000
        else:
            # reward in case of no crash is given by 4 terms:
            # 1) how far you are from the enemy car (normalized by the height of the environment): the farther you are, the better the reward
            # 2) how close you are to the center of the environment (only if PACMAN=False): the closer you are, the better the reward
            # 3) if you used the boost, you get a negative reward (to discourage the use of the it and only use it in case of emergency)
            # 4) if you moved, you get a slightly negative reward (to encourage the agent to move only when necessary and to stand still when waiting for the enemy)
            
            reward = self.car_distance()/float(C.ENVSIZE[1])  +                                         \
                    (0 if C.PACMAN   else    2/(1+float(abs(self.car_x_position-C.ENVSIZE[1]/2)))) +    \
                 (-100 if (action==3 or action==4)   else   0)   +                                   \
                    (0 if (action==0)   else   -1)
        
        # if you reached the maximum score, you won the game: environment is reset
        if self.score>C.MAXSCORE:
            print('GAME WON, score: ',self.score)
            self.crash()
            gameover=True
        
        return reward,gameover
    
    
    
    def render(self): 
        """
        Print the environment on terminal
        """
        for i in range(self.height):
            for j in range(self.width):
                print('|X' if self.env[i,j]==1 else '| ',end='')
            print('|\n')
            
        # if you also want the score to be printed at each step, uncomment the following line
        #print('Score: ',self.score,'\n')   