# AI-Snake
This program is a simulation of a neural network being trained by a genetic algorithm which is illustrated through the classic snake game and implemented via the Pygame library. The objective of the simulation is for the snakes to survive as long as they can

## Rules
- The snakes gain health when they consume a piece of food (denoted by the yellow squares)
- The snakes starves to death if it has not consumed a piece of food within an alotted time
- The snakes can only see the walls, the food, and itself
- The snakes also dies when it touches itself or the walls
- The color of the snake represents it's inheritance of DNA from it's parent when mating is peformed

## Instructions
- Press "SPACEBAR" to pause simulation
- Press "V" to display the vectors of the snake. The green line is the vector representing its current velocity and the white line is the vector representing its desired velocity
- Press "F" to display the snakes' FOV (field of view). Only the snake with the highest fitness score FOV is shown

## Requirements
- Python 3.9.4
- Pygame

Inspiration from: https://www.youtube.com/watch?v=BBLJFYr7zB8&t=162s
