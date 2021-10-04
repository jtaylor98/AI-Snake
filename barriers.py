import settings

def init_pos(population):
    for snake in population:
        settings.BARRIERS_POS[snake.ID] = []

def update_barriers_pos(population, food_pop):    
    segment_pos = []
    food_pos =[]
    
    #updating position of whole food population
    for food in food_pop:
        for pos in [(food.rect.topleft, food.rect.topright),
                (food.rect.bottomleft, food.rect.bottomright),
                (food.rect.topleft, food.rect.bottomleft),
                (food.rect.topright, food.rect.bottomright)]:
            food_pos.append(pos)
    settings.BARRIERS_POS.update({"Food": food_pos})

    #keeping track of pos of segments and updating in barriers list
    #first [exclude_segments] segments are exempt from fov
    for snake in population:
        segment_pos.clear()
        for i in range(settings.EXCLUDE_SEGMENTS, len(snake.body)):
            for pos in [(snake.body[i].rect.topleft, snake.body[i].rect.topright),
                    (snake.body[i].rect.bottomleft, snake.body[i].rect.bottomright),
                    (snake.body[i].rect.topleft, snake.body[i].rect.bottomleft),
                    (snake.body[i].rect.topright, snake.body[i].rect.bottomright)]:
                segment_pos.append(pos)
        settings.BARRIERS_POS.update({snake.ID: segment_pos[:]})
    
