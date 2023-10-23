from TDmodel import TDControl
import numpy as np
import Constants as C

class Agent():
    """
    Agent class that uses the TDControl model to train and play the game
    """
    
    def __init__(self,alg):
        """
        Initialize the agent with a given algorithm, and set the number of steps and the epsilon for the epsilon-greedy policy.
        The model parameters (states space size and actions space size) are described accurately in the class functions below.
        """
        
        self.n_steps=0
        self.eps=C.EPSILON  
        self.model=TDControl((2,5,2,4,4), 5, gamma=C.GAMMA,learning_rate=C.LEARNING_RATE, algorithm=alg)
       
       
       
      # first version of the binning function, using boolean values  
      
    # def side_position_binning(self,env):
    #     #print("Car position: ",env.car_x_position)
    #     wall_left=      (env.car_x_position<C.SPEED)                             # wall immediately on the left
    #     wall_right=     (env.car_x_position+env.car_width>env.w-C.SPEED)         # wall immediately on the right
    #     wall_near_left= (env.car_x_position<2*C.SPEED)                           # wall 2 steps on the left
    #     wall_near_right=(env.car_x_position+env.car_width>env.w-2*C.SPEED)       # wall 2 steps on the right
    #     enemy_left=       (env.l-env.enemy_y_position<2*env.car_height and (0<=env.car_x_position-env.enemy_x_position-env.car_width<C.SPEED)) # police car immediately on the left
    #     enemy_right=      (env.l-env.enemy_y_position<2*env.car_height and (0<=env.enemy_x_position-env.car_x_position-env.car_width<C.SPEED)) # police car immediately on the right
    #     enemy_near_left=  (env.l-env.enemy_y_position<2*env.car_height and (0<=env.car_x_position-env.enemy_x_position-env.car_width<2*C.SPEED)) # police car 2 steps on the left
    #     enemy_near_right= (env.l-env.enemy_y_position<2*env.car_height and (0<=env.enemy_x_position-env.car_x_position-env.car_width<2*C.SPEED)) # police car 2 steps on the right
    #     obstacle_left=wall_left or enemy_left                   # if you move left you lose
    #     obstacle_right=wall_right or enemy_right                # if you move right you lose
    #     obs_near_left=wall_near_left or enemy_near_left         # if you move left 2 times you lose
    #     obs_near_right=wall_near_right or enemy_near_right      # if you move right 2 times you lose
    #     #pos=[obstacle_left or obstacle_right,obs_near_left or obs_near_right]enemy_left
    #     pos=[obstacle_left,obstacle_right,obs_near_left,obs_near_right]
    #     return pos
    
    
    
     # second version of the binning function, using integers
     
    # def side_position_binning(self,env):
    #     enemy_near=(env.height-env.enemy_y_position<2*env.car_height) # cars are almost at the same height, they could crash from now on
    #     wall_right=0 if (env.car_x_position < C.SPEED) else \
    #                1 if (env.car_x_position<2*C.SPEED) else \
    #                2
    #     wall_left= 0 if (env.car_x_position+env.car_width>env.width - C.SPEED) else \
    #                1 if (env.car_x_position+env.car_width>env.width-2*C.SPEED) else \
    #                2
    #     enemy_left=  0 if (enemy_near and ((env.car_x_position-env.enemy_x_position)%env.width-env.car_width < C.SPEED)) else \
    #                1 if (enemy_near and ((env.car_x_position-env.enemy_x_position)%env.width-env.car_width<2*C.SPEED)) else \
    #                2 # problems here with pacman! solved?   original:(0<=env.car_x_position-env.enemy_x_position-env.car_width<...
    #     enemy_right= 0 if (enemy_near and ((env.enemy_x_position-env.car_x_position)%env.width-env.car_width < C.SPEED)) else \
    #                1 if (enemy_near and ((env.enemy_x_position-env.car_x_position)%env.width-env.car_width<2*C.SPEED)) else \
    #                2
    #     obstacle_left=min(wall_left,enemy_left)
    #     obstacle_right=min(wall_right,enemy_right)
    #     pos= [enemy_left,enemy_right] if C.PACMAN else [obstacle_left,obstacle_right]
    #     return pos
    
    
    
     # third version of the binning function, using integers and boost
    def side_position_binning_boost(self,env):
        """
        Return the horizontal distance of the enemy car and the walls, with respect to the car, using integers.
        """        
        # cars are at the same height, they could crash from now on
        enemy_near=(env.height-env.enemy_y_position<2*env.car_height) 
        
        # use binning to get different positions of the car with respect to walls and enemy car:
            # 0: wall or enemy car immediately on the left/right, meaning that if you move left/right you lose
            # 1: wall or enemy car 2 steps on the left/right, meaning that if you move left/right 2 times you lose
            # 2: wall or enemy car 2 boosted steps on the left/right, meaning that if you move left/right using boost 2 times you lose
            # 3: wall or enemy car farther than 2 boosted steps on the left/right
        
        # Notice that to compute the distance from walls we don't use modules, since we are 
        # not interested in walls position in the case of continuous space (PACMAN=True)
        wall_left_distance=env.car_x_position
        wall_right_distance=env.width-(env.car_x_position+env.car_width)

        wall_left= 0 if wall_left_distance < C.SPEED          else  \
                   1 if wall_left_distance<2*C.SPEED          else  \
                   2 if wall_left_distance<2*C.BOOST*C.SPEED  else  \
                   3
        
        wall_right=0 if wall_right_distance < C.SPEED         else  \
                   1 if wall_right_distance<2*C.SPEED         else  \
                   2 if wall_right_distance<2*C.BOOST*C.SPEED else  \
                   3
        
        # compute the horizontal distance between the two cars (using modules to consider the case of continuous space),
        # meaning the distance between the closest side of the two cars
        enemy_left_distance= (env.car_x_position-env.enemy_x_position)%env.width-env.car_width
        enemy_right_distance=(env.enemy_x_position-env.car_x_position)%env.width-env.car_width
        
        # compute the distance between the two cars (using modules to consider the case of continuous space),
        # in the case in which they are at the same height, meaning that they could crash from now on
        enemy_left=  0 if enemy_near and (enemy_left_distance < C.SPEED)          else  \
                     1 if enemy_near and (enemy_left_distance<2*C.SPEED)          else  \
                     2 if enemy_near and (enemy_left_distance<2*C.BOOST*C.SPEED)  else  \
                     3
        enemy_right= 0 if enemy_near and (enemy_right_distance < C.SPEED)         else  \
                     1 if enemy_near and (enemy_right_distance<2*C.SPEED)         else  \
                     2 if enemy_near and (enemy_right_distance<2*C.BOOST*C.SPEED) else  \
                     3
        # find the closest obstacle (wall or enemy car) on the left and on the right
        obstacle_left= min(wall_left, enemy_left)
        obstacle_right=min(wall_right,enemy_right)
        
        # return the distance of the closest obstacle on the left and on the right
        pos= [enemy_left, enemy_right] if C.PACMAN else [obstacle_left, obstacle_right]
        return pos
        
        
        
        # first version of the binning function, using boolean values
    # def front_position_binning(self,env): 
    #     #enemy_in_front = (abs(env.car_x_position-env.enemy_x_position)<env.car_width and env.l-env.enemy_y_position<2*env.car_height+C.SPEED) 
    #     enemy_in_front = (abs(env.car_x_position-env.enemy_x_position)<env.car_width) # police car in front of the car: don't stay there!
    #     enemy_leftright = (env.enemy_x_position<env.car_x_position)                       # police car on the left of the car if true, on the right (possibly center) if false
    #     enemy_near = enemy_in_front and (env.l-env.enemy_y_position<2*env.car_height+4*C.SPEED)  # police car near the car: don't stay there!
    #     pos=[enemy_in_front,enemy_leftright,enemy_near]
    #     return pos
    
    
    
    def front_position_binning(self,env):
        """
        Return information about the vertical position of the enemy car with respect to the car, using integers and booleans
        """
        
        # Compute the horizontal distance between the two cars (using modules to consider the case of continuous space),
        # meaning the distance between the closest side of the two cars
        enemy_left_distance= (env.car_x_position-env.enemy_x_position)%env.width-env.car_width
        enemy_right_distance=(env.enemy_x_position-env.car_x_position)%env.width-env.car_width
        
        minimum_distance=min(enemy_left_distance,enemy_right_distance)
        # Enemy is in front of you if the distance between the two cars is less than 0
        enemy_in_front= (minimum_distance<0)
        
        # Compute the vertical distance between the two cars
        car_vertical_distance=env.height-env.enemy_y_position-2*env.car_height
        
        # define a constant needed to normalize the results
        b=0 if env.car_width%(C.BOOST*C.SPEED)==0 else 1
        c=0 if env.car_width%C.SPEED==0 else 1
        #min_num_steps=env.car_width//(C.BOOST*C.SPEED)+b
        #min_num_steps2=env.car_width//C.SPEED+c
        # In this case I decided to use a different binning:
        # 0: enemy car in front of the car, crash in the next step is nothing changes
        # 1: enemy car in front of the car, crash in 2 steps from now if nothing changes
        # 2: enemy car in front of the car, in the worst case too close to escape even using boost 
        # 3: enemy car in front of the car, in the worst case too close to escape without using boost
        # 4: enemy car not in front of the car or very far away
        pol_dist= 0 if (enemy_in_front and (car_vertical_distance < C.SPEED)) else \
                  1 if (enemy_in_front and (car_vertical_distance<2*C.SPEED)) else \
                  2 if (enemy_in_front and (car_vertical_distance<env.car_width//(C.BOOST*C.SPEED)+b)) else \
                  3 if (enemy_in_front and (car_vertical_distance<env.car_width//C.SPEED+c)) else \
                  4
                  #new:    
                  #2 if (enemy_in_front and (min_num_steps2<=car_vertical_distance)) else \
                  #3 if (enemy_in_front and (min_num_steps<=car_vertical_distance)) else \
                  #4
                  
                  #middle:
                  #2 if (enemy_in_front and (car_vertical_distance<2*C.BOOST*C.SPEED)) else \
                  #3 if (enemy_in_front and (car_vertical_distance<3*C.BOOST*C.SPEED)) else \
                  #4    
                  
                  # 2 and 3 are actually not ideal for 2 reasons: you CANNOT escape if you move repeatedly,
                  # since the distance is strictly less than the one required to do it, and that factor is
                  # actually smaller than c.speed in almost every case (it is not only in case of big car with
                  # small speed and boost), hence it is rarely used
                  
        
        # Boolean value that tells if the enemy car is on the left of the car 
        # (hence, if it is False the enemy is on the right)
        enemy_leftright = (minimum_distance==enemy_left_distance)
        return [enemy_in_front,pol_dist,enemy_leftright]
        
        
        
    def get_state(self,env): 
        """
        Return the state of the environment: a quintuple (enemy_in_front, pol_dist, enemy_leftright, obstacle_left, obstacle_right)
        """
        state=(*self.front_position_binning(env),*self.side_position_binning_boost(env))
        return np.array(state,dtype=int)



    def get_action(self,state): 
        """
        Return the agent's action based on the previous observation of the state
        """
        action=self.model.getact_eps_greedy(state,self.eps)
        
        # reduce the epsilon for the epsilon-greedy policy, to make the agent more greedy at each step
        self.eps*=C.EPSDECAY
        return action
        
        
        
    def train_single_step(self,state,action,reward,new_state,new_action,done): 
        """
        Train method that trains the agent using the TDControl model
        """
        self.model.single_step_update(state,action,reward,new_state,new_action,done,self.eps)