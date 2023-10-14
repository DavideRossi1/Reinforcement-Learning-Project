
# This file contains all the constants needed to set up the project. Set them as you prefer

SPEED=5 # starting speed of both you and the falling objects
BOOST=3 # speed multiplier when boost is activated: your speed becomes BOOST*SPEED
MAXSCORE=10000 # maximum score that can be reached, game restarts after it is reached
COUNTER=10000000 # number of points to be scored before increasing the speed of the falling objects, hence increasing the difficulty

ENVSIZE=(100,100) # height and width of the environment
CARSIZE=(25,20) # height and width of the objects. A good choice to have something realistic is ~1/4 of the height and ~1/6 of the width of the environment
PACMAN=False # if True, environment becomes a continuous space, hence you can exit the environment from one side and re-enter from the opposite side

AGENT="SARSA" # agent algorithm to be used for training: SARSA, Qlearning, ExpectedSARSA

IMPORTPOLICYNAME="goodpolnoPMhybrid" # If you want to use a old policy, just set with the name of the file containing the policy. Otherwise, set with 0 to train a new policy
EXPORTPOLICYNAME=0 # If you want to save the learned policy in a file, set with the name of the file. Otherwise, set with 0
SAVESCORES=0 # If you want to save the scores in a file, set with the name of the file. Otherwise, set with 0

PRINTSTEPS=False # if True, the environment is printed in the terminal at each step
PLOTSTEPS=False # if True, the environment is plotted and animated (the animation won't stop until the user closes the plot)
WAIT=1 # time in milliseconds between each step in the case PLOTSTEPS=True. Increase it to slow down the animation





# ------------------------------ DO NOT CHANGE ANYTHING BELOW THIS LINE -------------------------------------

NSTEPS=1000000 # number of steps to be played (used for training purposes, not for plotting)
QSIZE=1600 # size of the Qvalues array, used for saving and loading the policy

if PACMAN:
    IMPORTPOLICY="pacman_policies/"+IMPORTPOLICYNAME
    EXPORTPOLICY="pacman_policies/"+EXPORTPOLICYNAME
else:
    IMPORTPOLICY="no_pacman_policies/"+IMPORTPOLICYNAME
    EXPORTPOLICY="no_pacman_policies/"+EXPORTPOLICYNAME
    
