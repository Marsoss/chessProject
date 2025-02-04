import pygame 
from time import sleep, time
import os
import random

def main():
    t1 = time()
    num_targets = 10
    score = 0
    for _ in range(num_targets):
        score = create_window(random.randint(100, 1000), random.randint(100, 500), 100, 100, score) 
    t2 = time()
    print("Score: ", score,"/", num_targets)
    print("Time taken: ", "%.3f" %float(t2-t1), 's')

def create_window(screen_x, screen_y, screen_w, screen_h, score=0):
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_x, screen_y)
    pygame.display.set_mode((screen_w, screen_h))
    run = 1
    t1 = time()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    run = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run = 0
                score+=1
            elif time()-t1 > 1:
                run = 0
        
    pygame.display.quit()
    return score

if __name__=='__main__':
    main()