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
  - [no_pacman_policies](./Project_files/no_pacman_policies) and [pacman_policies](./Project_files/pacman_policies): these directories contain the policies used to train the agent, saved as txt files. By setting the right parameters in the [Constants.py](./Project_files/Constants.py) file, you can import and export policies to try different configurations
  - [scores](./Project_files/scores): this directory contains the scores obtained while executing the model

## How to run the project

### Libraries
To run the project, you need to have `Python 3` installed on your machine, with `Matplotlib` and `NumPy` libraries. If you want to play the game with [car_play](./car_play), you also need to have `Pygame`, `time` and `random` libraries installed.\
Also, in case of Linux OS with Ryzen CPU and Radeon Graphics Graphic Card, depending on the installed libraries, some conflicts between `radeonsi` and `Pygame` libraries could arise. In that case, I suggest either to run the game with a clean Conda environment (containing just the needed libraries) or to manually set the following environment variable before running the game:

```{}
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
```

### Playing the game

To play the game, you need to run the [car_play.py](./car_play/car_play.py) file while being inside the [car_play](./car_play) directory. To stop it, just close thw window. The game will start with a car in the middle of the screen, and you can control it with the arrow keys. The game ends when the car hits an obstacle, and the score is shown in the terminal.\
The original code of this part, which has been revised and improved, can be found [here](https://geekyhumans.com/how-to-create-a-car-racing-game-in-python/).

### Running the RL algorithm

Before running, have a look and set up the parameters in the [Constants.py](./Project_files/Constants.py) file as you prefer. Then, run the [main.py](./Project_files/main.py) file while being inside the [Project_files](./Project_files) directory.\
The implementation of the Temporal Difference algorithm is based on the one done by the course tutor [Emanuele Panizon](https://www.ictp.it/member/emanuele-panizon).
