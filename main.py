# Note: Before running for the first time, the following command from terminal 
# could be necessary to avoid errors, depending on your OS and on installed libraries:
#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from agent import Agent
from car_class import game
import Constants as C
 
carspeed = C.SPEED
policespeed = C.SPEED
counter = C.COUNTER

def update_env(frame, env, Agent): 
    """
    This function is called at each step to update the entire environment and plot the result
    """
    global carspeed, policespeed, counter
    state = Agent.get_state(env)
    action = Agent.get_action(state)
    reward, gameover = env.playstep(action, carspeed, policespeed)
    newstate = Agent.get_state(env)
    newaction = Agent.get_action(newstate)
    Agent.train_single_step(state, action, reward, newstate, newaction, gameover)
    if env.score==counter: 
        policespeed+=1#max(C.DIFF//2,1) # increase the speed of the police cars
        counter+=C.COUNTER # set the next score to be reached to increase the speed of the police cars
    if gameover:
        policespeed=C.SPEED # reset the speed of the police cars
        counter=C.COUNTER
    if C.PLOTSTEPS:
        plt.clf()  # Clear the current plot
        plt.imshow(env.env, cmap='gray', extent=[0, env.width, 0, env.length])  # Update the plot with the new env data
        plt.title(f"Current score: {env.score}, Max Score: {env.maxscore}")
 
        
# def update_envVI(frame, env, Agent): 
#     global carspeed, policespeed, counter
#     state = Agent.get_state(env)
#     action = Agent.get_action(state)
#     gameover1 = env.movecar(action, carspeed)
#     gameover2 = env.movepol(policespeed)
#     rewards,gameover=Agent.model.rewards(state,action)
#     if env.score==counter: 
#         policespeed+=1#max(C.DIFF//2,1) # increase the speed of the police cars
#         counter+=C.COUNTER # set the next score to be reached to increase the speed of the police cars
#     if gameover:
#         policespeed=C.SPEED # reset the speed of the police cars
#         counter=C.COUNTER
#     if C.PLOTSTEPS:
#         plt.clf()  # Clear the current plot
#         plt.imshow(env.env, cmap='gray', extent=[0, env.width, 0, env.length])  # Update the plot with the new env data
#         plt.title(f"Current score: {env.score}, Max Score: {env.maxscore}")
        
    

def main():
    """
    Main function of the game: plays the game and plots/renders the updates 
    """
    env = game(*C.ENVSIZE, *C.CARSIZE) # build environment
    Agent1 = Agent(C.AGENT) # build agent
    #Agent1.model.value_iteration()
    if C.SAVESCORES!=0:
        f=open(C.SAVESCORES,'a')
        f.write("Algorithm: {}, Speed: {}, Environment size: {}, Car size: {}, Counter: {}, Nsteps: {}".format(C.AGENT,C.SPEED,C.ENVSIZE,C.CARSIZE,C.COUNTER,C.NSTEPS))
        f.close()
    if C.PLOTSTEPS:
        plt.figure(figsize=C.ENVSIZE)
        plt.imshow(env.env, cmap='gray')
        animation = FuncAnimation(plt.gcf(), update_env, fargs=(env, Agent1), frames=C.NSTEPS, interval=C.WAIT)
        plt.show()
    else:
        while Agent1.n_steps<C.NSTEPS: 
            if C.RENDERSTEPS:
                env.render() # print environment on terminal
            Agent1.n_steps+=1
            update_env(None, env, Agent1)
        if env.score>env.maxscore:
            env.maxscore=env.score
        print("Max score: ", env.maxscore)
    if C.EXPORTPOLICY!=0:
        Agent1.model.save_policy()

main()