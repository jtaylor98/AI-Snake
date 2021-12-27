## AI Snake
This program replicates the process of a neuroevolutionary system through a genetic algorithm. The program is based off the classic snake arcade game where a snake tries to obtain food while avoiding collision with itself and the walls. In this program a population of snakes is created and through generations of dying and reinforced learning is able to understand the rules and nature of its environment. This genetic algorithm was designed in such a way that certain metrics of the model may be altered depending on the overall progress of cumulative generations. This helps prevent the model from converging toward local minima and instead encourages convergence toward a global minima

## Rules
- The snakes gain health when they consume a piece of food (denoted by the yellow squares)
- The snakes starves to death if it has not consumed a piece of food within an allotted time
- The snakes can only see the walls, the food, and itself
- The snakes also dies when it touches itself or the walls
- The color of the snake represents it's inheritance of DNA from it's parent when mating is performed

## Instructions
- Press "SPACE" to pause simulation
- Press "V" to display the vectors of the snake. The green line is the vector representing its current velocity and the white line is the vector representing its desired velocity
- Press "F" to display the snakes' FOV (field of view). Only the snake with the highest fitness score FOV is shown

## Requirements
- Python 3.9.4
- Pygame

Inspired by: https://www.youtube.com/watch?v=BBLJFYr7zB8&t=162s
