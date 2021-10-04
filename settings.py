import pygame as pg

def init():
    global WIN, SCR_WIDTH, SCR_HEIGHT, SCR_TOP, SCR_BOTTOM, SCR_LEFT, SCR_RIGHT, FPS, WHITE, BLACK, RED, GREEN, BLUE, RED, YELLOW, DARKGRAY, IVORY, ROSY_BROWN, EXCLUDE_SEGMENTS, BARRIERS_POS, N_GLOBAL_BARR, BATCH_SIZE
    
    SCR_WIDTH, SCR_HEIGHT = 1300, 1000
    WIN = pg.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pg.display.set_caption("AI Snake")

    WIN_rect = WIN.get_rect()
    SCR_TOP = WIN_rect.topleft, WIN_rect.topright
    SCR_BOTTOM = WIN_rect.bottomleft, WIN_rect.bottomright
    SCR_LEFT = WIN_rect.topleft, WIN_rect.bottomleft
    SCR_RIGHT = WIN_rect.topright, WIN_rect.bottomright
    
    BARRIERS_POS = {"Wall": [(SCR_TOP), (SCR_BOTTOM), (SCR_LEFT), (SCR_RIGHT)],
                    "Food": [],
                    "STOP": None} #stop is a placeholder separating global barriers and body pos of all snakes
    N_GLOBAL_BARR = 2 #number of barriers that all snakes will see (wall & food)
    BATCH_SIZE = 3
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    DARKGRAY = (40, 40, 40)
    IVORY = (255, 255, 240)
    ROSY_BROWN = (188, 143, 143)
    
    EXCLUDE_SEGMENTS = 2  #specifyiEg a number of segments to exclude in our barriers list
