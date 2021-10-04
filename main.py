#!/usr/bin/env python

import pygame as pg
import settings
from snake import Head, Segment, Snake
from food import Food
from neural_network import Network, DenseLayer, sigmoid
from genetic_algorithm import Population
from barriers import update_barriers_pos, init_pos

pg.init()
settings.init()
def show_stats(population):
    incr = 40
    ypos = 10
    xpos = 10
    
    font = pg.font.Font("freesansbold.ttf", 20)
    time = font.render("Time: " + str(pg.time.get_ticks()/1000), True, settings.IVORY)
    settings.WIN.blit(time, (xpos, ypos))
    ypos += incr
    
    fitness = font.render("Max Fitness: " + str("{0:.2f}".format(population.max_fitness)), True, settings.IVORY)
    settings.WIN.blit(fitness, (xpos, ypos))
    ypos += incr
        
    generation = font.render("Current Generation: " + str(population.current_gen), True, settings.IVORY)
    settings.WIN.blit(generation, (xpos, ypos))
    ypos += incr 

    mutation_rate = font.render("Mutation Rate: " + str("{0:.2%}".format(population.mutation_rate)), True, settings.IVORY)
    settings.WIN.blit(mutation_rate, (xpos, ypos))
    ypos += incr     
    
    ypos = settings.SCR_HEIGHT - 70
    title = font.render("CURRENT STATUS:", True, settings.IVORY)
    settings.WIN.blit(title, (xpos, ypos))
    
    ypos += 35
    font_small = pg.font.Font("freesansbold.ttf", 17)
    model_status = font_small.render(population.current_status, True, settings.ROSY_BROWN)
    settings.WIN.blit(model_status, (xpos, ypos))
            
def main():
    clock = pg.time.Clock()
    run = True
    pause = False
    show_vectors = False
    show_fov = False

    radius = 20 #radius of snake head/body
    pop_size = 8 #size of snake
    n_food = int(pop_size/2) #number of food that will remain on the screen at all times

    ratios = {"force": (0.15, 0.2), #ratio of head to snake speed/force
              "speed": (3, 4)}
    
    #holds position of each barrier visible to the snake
    network_struct = [60, 16, 16, 2] #structure of neural network 60 input, 16 neurons for two hidden layers and 2 output neurons
    food_population = [Food(25) for _ in range(n_food)] #creating 5 food objects
    
    snake_population = Population(pop_size, radius, ratios, network_struct)
    while run:
        clock.tick(settings.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pause = not pause
                if event.key == pg.K_v:
                    show_vectors = not show_vectors
                if event.key == pg.K_f: #show fov
                    show_fov = not show_fov
        
        if not pause:
            settings.WIN.fill(settings.DARKGRAY)
            show_stats(snake_population)
            update_barriers_pos(snake_population.population, food_population) #updating position of barriers to barrier_pos dictionary
            snake_population.update(show_vectors, show_fov) #updating position of snake
            for snake in snake_population.population:
                for food in food_population: #updating pos of food
                    food.update(snake)           
        pg.display.update()
main()
