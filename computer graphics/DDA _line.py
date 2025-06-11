import pygame
import sys

def draw_line_dda(x0, y0, x1, y1, screen, color):
    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x0
    y = y0

    for _ in range(steps+1 ):
     screen.set_at((int(round(x)), int(round(y))), color)
    x += x_inc
    y += y_inc
    

def main():
    
    try:
        x0 = int(input("enter starting x-coordinate: "))
        y0 = int(input("enter starting y-coordinate: "))
        x1 = int(input("enter ending x-coordinate: "))
        y1 = int(input("enter ending y-coordinate: "))
    except ValueError:
        print(" invalid  values.")
        sys.exit()

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("MY DDA Line ")
    screen.fill((255, 255, 155))

    draw_line_dda(x0, y0, x1, y1, screen, (0, 0, 0))
    pygame.display.update()

    print(f"Line drawn from ({x0}, {y0}) to ({x1}, {y1})")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
