
# This file contains all the constants needed to set up the project. Set them as you prefer


 # Integer. Starting speed of both you and the enemy cars:
SPEED=5          

# Integer. Speed multiplier: when boost is activated, your speed becomes BOOST*SPEED:
BOOST=4      

 # Integer. Maximum score that can be reached, game restarts after it is reached:     
MAXSCORE=100000000    

# Integer. Number of points to be scored before increasing the speed of the enemy cars, 
# hence increasing the difficulty. Set it to a high value to maintain the enemy speed constant:
COUNTER=100   

# Couple of integers. Height and width of the environment:
ENVSIZE=(100,100)

# Couple of integers. Height and width of the cars. A good choice to have something realistic is ~1/4 of 
# the height and ~1/6 of the width of the environment. Avoid setting them with too big values (larger than ~1/3 of 
# the height and ~1/4 of the width of the environment in the case of no pacman), otherwise it will be too 
# difficult to avoid the enemy cars:
CARSIZE=(25,20)    

# Boolean. If True, environment becomes a continuous space, hence you can exit the environment 
# from one side and re-enter from the opposite side:
PACMAN=True       

# String, or 0. If you want to use a old policy, set with the name of the file containing the policy. 
# Otherwise, set with 0 to train a new policy:
IMPORTPOLICYNAME="policy_SARSA_hybrid_PM_diff4.txt"

# String, or 0. If you want to save the learned policy in a file, set with the name of the file. 
# Otherwise, set with 0:
EXPORTPOLICYNAME="policy_SARSA_hybrid_PM_diff4_bigenv.txt"

# String, or 0. If you want to save the scores in a file, set with the name of the file. 
# Otherwise, set with 0:              
SAVESCORESNAME="scores_SARSA_hybrid_PM_diff4_bigenv.txt"                    

# Boolean. If True, the environment is printed in the terminal at each step:
PRINTSTEPS=False   

# Boolean. If True, the environment is plotted and animated (the animation won't stop until the user closes the plot):
PLOTSTEPS=False

# Integer. Time in milliseconds between each step in the case PLOTSTEPS=True. Increase it to slow down the animation:  
WAIT=1             

# Agent algorithm to be used for training: SARSA, Qlearning, ExpectedSARSA:
AGENT="SARSA"      

# Double in [0,1]. Discount factor for temporal difference learning:
GAMMA=1            

# Positive double. Learning rate for temporal difference learning:
LEARNING_RATE=0.01 

# Double in [0,1]. Epsilon used for the epsilon-greedy policy. 0 means no exploration, 1 means no exploitation:
EPSILON=0.5      

# Double in [0,1]. Epsilon decay factor: the epsilon used for the epsilon-greedy policy is multiplied by this factor at each step
EPSDECAY=0.90      














# ------------------------------ DO NOT CHANGE ANYTHING BELOW THIS LINE -------------------------------------

NSTEPS=10000000     # number of steps to be played (used for training purposes, not for plotting)
QSIZE=1600         # size of the Qvalues array, used to save and load the policy, don't change it

# routine to set the right path for files
if PACMAN:
    if IMPORTPOLICYNAME!=0:
        IMPORTPOLICY="policies/pacman/"+AGENT+"/"+IMPORTPOLICYNAME
    if EXPORTPOLICYNAME!=0:
        EXPORTPOLICY="policies/pacman/"+AGENT+"/"+EXPORTPOLICYNAME
    if SAVESCORESNAME!=0:    
        SAVESCORES="scores/pacman/"+AGENT+"/"+SAVESCORESNAME
else:
    if IMPORTPOLICYNAME!=0:
        IMPORTPOLICY="policies/no_pacman/"+AGENT+"/"+IMPORTPOLICYNAME
    if EXPORTPOLICYNAME!=0:
        EXPORTPOLICY="policies/no_pacman/"+AGENT+"/"+EXPORTPOLICYNAME
    if SAVESCORESNAME!=0:    
        SAVESCORES="scores/no_pacman/"+AGENT+"/"+SAVESCORESNAME

    
