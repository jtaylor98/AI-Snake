from snake import Head, Snake, Segment
from random import randint, choice, uniform
from math import floor, ceil
import settings

class Population():
    def __init__(self, size, *args):
        self.size = size
        self.snake_details = args
        self.population = []
        self.death_count = size #will keep track of how many snakes in the mating pool have died off in the population
        self.current_status = "NORMAL"
        self.eval_num = 5
        self.progress_count = 0
        self.gen_stats = [[] for _ in range(self.eval_num)]
        self.gen_index = 0
        self.add_noise = False
        self.fitness_threshold = 6
        self.progress_threshold = .03 #progress must be >= %3
        self.mating_pool = []
        self.mating_pool_cap = self.size - 3
        self.adjust_crossover_method = False
        self.max_fitness = 20
        self.fittest_snake = None
        self.mutation_rate = 0.05
        self.min_mut_rate = 0.01
        self.mutation_bias = 0
        self.crossover_rate = 0.90
        self.current_gen = 1
        for i in range(size):
            self.population.append(Snake(args[0], args[1], args[2]))
            self.population[i].gen = 0
            self.population[i].fitness = self.calc_fitness(self.population[i])
            self.population[i].parents = None
            self.population[i].evaluated = False
            self.mating_pool.append(self.population[i])
        self.onscreen_population = self.population[:]
        self.mating_pool.sort(reverse=True, key=lambda x: x.fitness) #sorting mating_pool based on fitness value     
            
    def evaluate(self, dead_snake): 
        if dead_snake.dead: #removing snake once completely dead
            self.onscreen_population.remove(dead_snake)
            settings.BARRIERS_POS.pop(dead_snake.ID) #removing snake from barrier pos dict
        elif dead_snake.evaluated == False:
            self.death_count += 1 #increasing death count        
            self.population.remove(dead_snake)
            dead_snake.fitness = self.calc_fitness(dead_snake) #updating final fitness value for dead snake
            self.max_fitness = max(self.calc_fitness(s) for s in self.population)
            if self.death_count % self.size == 0: #snakes in current gen have died so updating generation count
                #print("NEW GENERATION")
                self.current_gen += 1
                self.gen_index += 1
                if (self.current_gen - 1) % self.eval_num == 0: #evaluating progress every 5 generations
                    self.evaluate_performance() #evaluating progress of genetic algorithm model
                    self.gen_index = 0
                    self.gen_stats = [[] for i in range(self.eval_num)]
            else:
                self.gen_stats[self.gen_index].append(dead_snake.fitness) #keeping track of all snake fitness values per generation
                if dead_snake not in self.mating_pool and len(self.mating_pool) < self.size:
                    self.mating_pool.append(dead_snake)
                else:
                    for i in range(len(self.mating_pool)):
                        if dead_snake.fitness > self.mating_pool[i].fitness: #comparing dead_snake fitness to other snakes
                            self.mating_pool.insert(i, dead_snake) #appending dead_snake if fitness is greater than any other ones
                            self.mating_pool.pop(-1) #removing last snake since lowest fitness value
                            break   
            self.mating_pool.sort(reverse=True, key=lambda x: x.fitness) #sorting mating_pool based on fitness value     
            parents = self.selection() #selecting parents from mating pool

            child_DNA, gen, child_parents = self.crossover(parents)
            child = Snake(self.snake_details[0], self.snake_details[1], self.snake_details[2], child_DNA)
            child.gen = gen
            child.fitness = self.calc_fitness(child)
            child.parents = child_parents
            child.evaluated = False
            self.population.append(child)
            self.onscreen_population.append(child)
            dead_snake.evaluated = True
            
    def selection(self):
        parents = []
        indices = []

        popl_fitnessq = [self.calc_fitness(s) for s in self.mating_pool[:self.mating_pool_cap]]
        indices = [s for s in self.mating_pool[:self.mating_pool_cap]]
        
        """print("MATING POOL")
        for s in self.mating_pool:
            print(s.fitness)"""

        for _ in range(2): #picking two fit parents
            index = 0
            sum_ = sum(popl_fitnessq)
            num = uniform(0, sum_) #selecting random value b/w 0 and sum of fitness values (will be used to compare against fitness values)
            while num > 0: #will keep repeating until random num < 0
                #num will gradually get smaller as long as it is larger than given fitness value
                num = num - popl_fitnessq[index] #going through each individual in the population and checking if num < fitnessval
                index += 1
            index -= 1 #going back to prev index
            parents.append(indices.pop(index)) #returning associated parent w/ fitness value
            popl_fitnessq.pop(index) #insuring parent selected cannot be selected as second parent
        """print("--PARENTS PICKED--")
        print("P1: ", parents[0].fitness)
        print("P2: ", parents[1].fitness)
        print("\n")"""
        return parents
    
    def calc_fitness(self, snake): return 10 + (snake.size * snake.health)
    
    def evaluate_performance(self):
        first, current = max(self.gen_stats[0]), max(self.gen_stats[-1]) #getting max fitness of first and last gen in list
        if current > first: #checking if fitness has increased 
            incr = current - first
            percentage_incr = incr/current * 100
            if percentage_incr <= (self.progress_threshold * 100) and self.current_gen > 30: #progress is starting to flatten
                self.adjust_crossover_method = True
                self.current_status = "PROGRESS FLATTENING: adjusting crossover method"
            else: 
                self.adjust_crossover_method = False
                self.mutation_bias = 0
                self.current_status = "PROGRESS IS SUFFICIENT"
        else: 
            self.progress_count += 1
            if self.progress_count == 2:
                self.current_status = "MODEL DIGRESSING: increasing mutation rate"
                self.mutation_bias += 0.02  
                self.progress_count = 0
            
    def crossover(self, parents): #generates offspring        
        current_rate = 10/max(self.calc_fitness(s) for s in self.mating_pool)
        self.mutation_rate = current_rate+self.mutation_bias if current_rate > self.min_mut_rate else self.min_mut_rate+self.mutation_bias #mutation rate increases when fitness in mating pool is not high and vice versa
        p1, p2 = parents
        child_DNA = p1.DNA.multipoint_crossover(p2, self.mutation_rate) if not self.adjust_crossover_method else p1.DNA.avg_crossover(p2, self.mutation_rate) #mating parents to produce child
        child_gen = max(p1.gen, p2.gen) + 1 #calculating generation num for child
        child_parents = p1, p1 #p2 if p1.fitness > p2.fitness else p1 #returning parent w/ lowest fitness value
        child_DNA.data.append(p1.color_rgb[:-1] if p1.fitness > p2.fitness else p2.color_rgb[:-1]) #inheriting parent with higher fitness, rgb value
        return child_DNA, child_gen, child_parents
        
    def update(self, show_v, show_f):
        self.population.sort(key=lambda x: x.fitness)
        self.fittest_snake = self.population[-1] #getting snake with highest fitness
        for snake in self.onscreen_population:
            snake.fitness = self.calc_fitness(snake)
            if show_f: #only showing fov for snake with highest fitness
                if snake == self.fittest_snake: snake.update(show_v, show_f,) #updating position of snake
                else: snake.update(show_v, False)
            else:
                snake.update(show_v, show_f)
            if snake.death_fade:
                self.evaluate(snake) #evaluting snake once death_fade occurs

