# Reinforcement-Learning-Project
Repository for the project of the Reinforcement Learning exam for year 2022-2023 in University of Trieste.

The project consists in implementing a Reinforcement Learning algorithm in a practical scenario. The chosen scenario is a classical dodge drop game, where the player has to avoid obstacles falling from the top of the screen. The player can move left and right, and the game ends when the player hits an obstacle.\
All the results obtained during the project can be found in the [report](./report.pdf).


## Repository structure
This repository contains 2 folders:

- [car_play/](./car_play): contains the files needed to play the game by yourself, with a nice GUI with a car that can be controlled with the arrow keys
- [Project_files/](./Project_files): contains the files needed to run the Reinforcement Learning algorithm and train the agent to play the game. In particular, the files are:
  - [Constants.py](./Project_files/Constants.py): contains all the constants used in the project. All the constants have a detailed explanation and you can change them to try different configurations and to decide what policies to use, whether to save the results or not, whether to render the game or not, etc.
  - [main.py](./Project_files/main.py): the main file, that contains the code to run the algorithm 
  - [agent.py](./Project_files/agent.py): contains the code of the agent, that is the one that learns to play the game
  - [TDmodel.py](./Project_files/TDmodel.py): contains the code for the implementation of the Temporal Difference control algorithm
  - [car_class.py](./Project_files/car_class.py): contains the code for the implementation of the car class, that is the one that controls the car in the game
  - [policies](./Project_files/policies): contains the policies used to train the agent, subdivided by typology (Pacman - No Pacman effect) and by algorithm (SARSA, Qlearning, ExpectedSARSA) saved as txt files. By setting the right parameters in the [Constants.py](./Project_files/Constants.py) file, you can import and export policies to try different configurations
  - [scores](./Project_files/scores): contains the scores obtained while executing the model
  - [archive](./Project_files/): an archive of all the policies and scores obtained during the project. Further information inside the folder

## How to run the project

### Libraries
To run the project, you need to have `Python 3` installed on your machine, with `Matplotlib` and `NumPy` libraries. If you want to play the game with [car_play](./car_play), you also need to have `Pygame`, `time` and `random` libraries installed.
Also, in case of Linux OS with Ryzen CPU, depending on the installed libraries, `Pygame` could have some troubles finding `radeonsi` drivers. In that case, I suggest either to run the game with a clean Conda environment (containing just the needed libraries) or, in case the problem should not be solved, to manually set the following environment variable before running the game:

```{}
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
```

### Playing the game

To play the game, you need to run the [car_play.py](./car_play/car_play.py) file while being inside the [car_play/](./car_play) directory. The game will start with a car in the middle of the screen, and you can control it with the arrow keys. The game ends when the car hits an obstacle, and the score is shown. To stop playing, just close the window.

### Running the RL algorithm

Before running, have a look and set up the parameters in the [Constants.py](./Project_files/Constants.py) file as you prefer. Then, run the [main.py](./Project_files/main.py) file while being inside the [Project_files/](./Project_files) directory. The game will start and the agent will start playing and learning using the selected policy. If PLOTSTEPS=True was selected, the game will also be played with a graphical interface, so that you can see the agent playing.

## Results

The results obtained during the project can be found in the [report](./report.pdf).

The policies seen inside the report, and some others more, are already available to use inside the [policies](./Project_files/policies) directory.

The final results are:

Starting agent:

<img src="/images/starting.gif"/>


Learned agent (with boost):

<img src="/images/improved.gif"/>



## Credits

The original code of the car game, which has been revised and improved, can be found [here](https://geekyhumans.com/how-to-create-a-car-racing-game-in-python/).

The implementation of the Temporal Difference algorithm is based on the one done by the course tutor [Emanuele Panizon](https://www.ictp.it/member/emanuele-panizon).


