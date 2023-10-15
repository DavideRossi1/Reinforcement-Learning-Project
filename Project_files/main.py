# Note: Before running for the first time, the following command from terminal 
# could be useful/necessary to avoid errors/warnings, depending on your OS and on installed libraries:
#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from agent import Agent
from car_class import game
import Constants as C
 
 # global variables that will be changed to modify the speed of the cars and the score at which the speed increases
carspeed = C.SPEED
policespeed = C.SPEED
counter = C.COUNTER

def update_env(frame, env, Agent): 
    """
    This function is called at each step to update the entire environment and plot the result
    """
    global carspeed, policespeed, counter
    
    # get the current state of the environment
    state = Agent.get_state(env) 
    
    # get the action to be taken based on the state
    action = Agent.get_action(state) 
    
    # play a step of the game and get the reward and the gameover status
    reward, gameover = env.playstep(action, carspeed, policespeed) 
    
    # get the new state of the environment after the step
    newstate = Agent.get_state(env)
    
    # get the new action to be taken based on the new state
    newaction = Agent.get_action(newstate)
    
    # train the agent using Temporal Difference control
    Agent.train_single_step(state, action, reward, newstate, newaction, gameover)
    
    # update the speed of the falling objects
    if env.score==counter: 
        policespeed+=1  # increase the speed 
        counter+=C.COUNTER # set the next score to be reached to increase the speed
    if gameover:
        policespeed=C.SPEED # reset the speed 
        counter=C.COUNTER
        
    # if desired, plot the environment
    if C.PLOTSTEPS:
        plt.clf()  # Clear the current plot
        plt.imshow(env.env, cmap='gray', extent=[0, env.width, 0, env.length])  # Update the plot with the new env data
        plt.title(f"Current score: {env.score}, Max Score: {env.maxscore}")
    
    
    
    
def main():
    """
    Main function of the game: plays the game and plots/renders the updates 
    """
    
    # build the environment
    env = game(*C.ENVSIZE, *C.CARSIZE) 
    
    # build the agent
    Agent1 = Agent(C.AGENT) 
    
    # if desired, save the scores in a file
    if C.SAVESCORESNAME!=0:
        f=open(C.SAVESCORES,'a')
        comments="Algorithm: {}, Speed: {}, Boost: {}, PM: {}, Env size: {}, Car size: {}, Counter: {}, Nsteps: {}, Gamma: {}, LearnRate: {}, Eps: {}, Epsdecay: {}".format(C.AGENT,C.SPEED,C.BOOST,C.PACMAN,C.ENVSIZE,C.CARSIZE,C.COUNTER,C.NSTEPS,C.GAMMA,C.LEARNING_RATE,C.EPSILON,C.EPSDECAY)
        f.write(comments)
        f.close()
        
    # if desired, plot the environment
    if C.PLOTSTEPS:
        plt.figure(figsize=C.ENVSIZE)
        plt.imshow(env.env, cmap='gray')
        animation = FuncAnimation(plt.gcf(), update_env, fargs=(env, Agent1), frames=C.NSTEPS, interval=C.WAIT)
        plt.show()
    
    # otherwise, just play the game
    else:
        while Agent1.n_steps<C.NSTEPS: 
            
            # if desired, print the environment
            if C.PRINTSTEPS:
                env.render() # print environment on terminal
            Agent1.n_steps+=1
            update_env(None, env, Agent1)
        if env.score>env.maxscore:
            env.maxscore=env.score
        print("Max score: ", env.maxscore)
        
    # if desired, save the learned policy in a file
    if C.EXPORTPOLICYNAME!=0:
        Agent1.model.save_policy()




# Let's play!
main()