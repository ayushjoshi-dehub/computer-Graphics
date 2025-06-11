import pygame
import sys
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dog House Drawing")

# Colors
WHITE = (255, 255, 115)
BLACK = (0, 0, 0)

def draw_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for _ in range(int(steps) + 1):
        screen.set_at((round(x), round(y)), WHITE)
        x += x_inc
        y += y_inc

def draw_dog_house():
    
    draw_line(300, 400, 500, 400)
    draw_line(300, 400, 300, 300) 
    draw_line(500, 400, 500, 300)  
    draw_line(300, 300, 500, 300) 

    draw_line(300, 300, 400, 200)  
    draw_line(400, 200, 500, 300) 

   
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_dog_house()
        pygame.display.flip()
        clock.tick(60)

main()

import pygame
import sys
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DDA Line Drawing")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
def draw_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for _ in range(int(steps) + 1):
        screen.set_at((round(x), round(y)), WHITE)
        x += x_inc
        y += y_inc

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
        draw_line(10, 10, 100, 90)
        pygame.display.flip()
main()