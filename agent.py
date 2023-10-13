from TDmodel import TDControl
import numpy as np
import Constants as C

class Agent():
    def __init__(self,alg):
        self.n_steps=0
        self.eps=0.5  
        self.model=TDControl((2,4,2,3,3),3,algorithm=alg)
        
    # def side_position_binning1(self,env):
    #     #print("Car position: ",env.carposw)
    #     wall_left=      (env.carposw<C.SPEED)                             # wall immediately on the left
    #     wall_right=     (env.carposw+env.car_width>env.w-C.SPEED)   # wall immediately on the right
    #     wall_near_left= (env.carposw<2*C.SPEED)                           # wall 2 steps on the left
    #     wall_near_right=(env.carposw+env.car_width>env.w-2*C.SPEED) # wall 2 steps on the right
    #     pol_left=       (env.l-env.polposl<2*env.car_length and (0<=env.carposw-env.polposw-env.car_width<C.SPEED)) # police car immediately on the left
    #     pol_right=      (env.l-env.polposl<2*env.car_length and (0<=env.polposw-env.carposw-env.car_width<C.SPEED)) # police car immediately on the right
    #     pol_near_left=  (env.l-env.polposl<2*env.car_length and (0<=env.carposw-env.polposw-env.car_width<2*C.SPEED)) # police car 2 steps on the left
    #     pol_near_right= (env.l-env.polposl<2*env.car_length and (0<=env.polposw-env.carposw-env.car_width<2*C.SPEED)) # police car 2 steps on the right
    #     obs_left=wall_left or pol_left                   # if you move left you lose
    #     obs_right=wall_right or pol_right                # if you move right you lose
    #     obs_near_left=wall_near_left or pol_near_left    # if you move left 2 times you lose
    #     obs_near_right=wall_near_right or pol_near_right # if you move right 2 times you lose
    #     #pos=[obs_left or obs_right,obs_near_left or obs_near_right]pol_left
    #     pos=[obs_left,obs_right,obs_near_left,obs_near_right]
    #     return pos
    
    def side_position_binning(self,env):
        pol_near=(env.length-env.polposl<2*env.car_length) # cars are almost at the same height, they could crash from now on
        wall_right=0 if (env.carposw < C.SPEED) else \
                  (1 if (env.carposw<2*C.SPEED) else 
                   2)
        wall_left= 0 if (env.carposw+env.car_width>env.width - C.SPEED) else \
                  (1 if (env.carposw+env.car_width>env.width-2*C.SPEED) else 
                   2)
        pol_left=  0 if (pol_near and ((env.carposw-env.polposw)%env.width-env.car_width < C.SPEED)) else \
                  (1 if (pol_near and ((env.carposw-env.polposw)%env.width-env.car_width<2*C.SPEED)) else \
                   2) # problems here with pacman! solved?   original:(0<=env.carposw-env.polposw-env.car_width<...
        pol_right= 0 if (pol_near and ((env.polposw-env.carposw)%env.width-env.car_width < C.SPEED)) else \
                  (1 if (pol_near and ((env.polposw-env.carposw)%env.width-env.car_width<2*C.SPEED)) else \
                   2)
        obs_left=min(wall_left,pol_left)
        obs_right=min(wall_right,pol_right)
        pos= [pol_left,pol_right] if C.PACMAN else [obs_left,obs_right]
        return pos
        
    # def front_position_binning1(self,env): 
    #     #pol_in_front = (abs(env.carposw-env.polposw)<env.car_width and env.l-env.polposl<2*env.car_length+C.SPEED) 
    #     pol_in_front = (abs(env.carposw-env.polposw)<env.car_width) # police car in front of the car: don't stay there!
    #     pol_leftright = (env.polposw<env.carposw)                       # police car on the left of the car if true, on the right (possibly center) if false
    #     pol_near = pol_in_front and (env.l-env.polposl<2*env.car_length+4*C.SPEED)  # police car near the car: don't stay there!
    #     pos=[pol_in_front,pol_leftright,pol_near]
    #     return pos
    
    def front_position_binning(self,env):
        pol_in_front=(abs(env.carposw-env.polposw)<env.car_width)
        car_vertdist=env.length-env.polposl-2*env.car_length
        c=0 if env.car_width%C.SPEED==0 else 1
        pol_dist= 0 if (pol_in_front and (car_vertdist < C.SPEED)) else \
                 (1 if (pol_in_front and (car_vertdist<2*C.SPEED)) else 
                 (2 if (pol_in_front and (car_vertdist<env.car_width//C.SPEED+c)) else 
                  3))
        pol_leftright = (min((env.carposw-env.polposw)%env.width,(env.polposw-env.carposw)%env.width)==(env.polposw-env.carposw)%env.width) #(env.polposw<env.carposw)  problems here with pacman! solved?
        return [pol_in_front,pol_dist,pol_leftright]
        
    def get_state(self,env):  # returns the overall state of the environment
        state=(*self.front_position_binning(env),*self.side_position_binning(env))
        #print("State not converted: ",state)
        #print("State converted: ",np.array(state,dtype=int))
        return np.array(state,dtype=int)

    def get_action(self,state): # Returns the agent's action based on the previous observation of the state
        action=self.model.getact_eps_greedy(state,self.eps)
        self.eps*=0.90
        return action
        
    def train_single_step(self,state,action,reward,new_state,new_action,done): # Train method that trains the agent using the TDControl model
        self.model.single_step_update(state,action,reward,new_state,new_action,done,self.eps)