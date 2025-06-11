import pygame
import sys
import math
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Adventure")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PLANET_NAMES = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

COLORS = [
    (169, 169, 169),  # Mercury - gray
    (255, 140, 0),    # Venus - orange
    (0, 0, 255),      # Earth - blue
    (255, 0, 0),      # Mars - red
    (255, 215, 0),    # Jupiter - gold
    (218, 165, 32),   # Saturn - goldenrod
    (0, 255, 255),    # Uranus - cyan
    (0, 0, 139),      # Neptune - dark blue
]

ORBIT_RADII = [60, 90, 120, 150, 200, 250, 300, 350]
PLANET_RADII = [6, 8, 9, 7, 15, 13, 11, 11]
SPEEDS = [0.02, 0.015, 0.013, 0.01, 0.008, 0.007, 0.005, 0.004]

NUM_STARS = 200
stars = [(random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1), random.randint(1,2)) for _ in range(NUM_STARS)]

NUM_GALAXIES = 5
galaxies = []
min_dist = ORBIT_RADII[-1] + 10
max_dist = ORBIT_RADII[-1] + 70
for _ in range(NUM_GALAXIES):
    while True:
        gx = random.randint(0, WIDTH)
        gy = random.randint(0, HEIGHT)
        dist = math.hypot(gx - WIDTH//2, gy - HEIGHT//2)
        if min_dist < dist < max_dist:
            size = random.randint(40, 80)
            galaxies.append((gx, gy, size))
            break

def draw_planet_label(surface, name, x, y):
    font = pygame.font.SysFont("Arial", 12)
    label = font.render(name, True, WHITE)
    surface.blit(label, (x + 10, y - 10))

class Spaceship:
    def __init__(self):
        self.reset()
        # Create a detailed spaceship design
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        # Body
        pygame.draw.polygon(self.image, (100, 100, 255), [(15, 0), (5, 40), (25, 40)])
        # Wings
        pygame.draw.polygon(self.image, (150, 150, 150), [(5, 30), (0, 40), (5, 40)])
        pygame.draw.polygon(self.image, (150, 150, 150), [(25, 30), (30, 40), (25, 40)])
        # Cockpit
        pygame.draw.ellipse(self.image, (200, 200, 255), (10, 5, 10, 10))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.rotation_speed = 3

    def update(self, planets):
        keys = pygame.key.get_pressed()
        # Rotation
        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed

        # Acceleration
        if keys[pygame.K_UP]:
            accel_x = self.acceleration * math.cos(math.radians(self.angle))
            accel_y = -self.acceleration * math.sin(math.radians(self.angle))
            self.velocity_x += accel_x
            self.velocity_y += accel_y
        # Deceleration
        else:
            speed = math.hypot(self.velocity_x, self.velocity_y)
            if speed > 0:
                factor = max(0, speed - self.deceleration) / speed
                self.velocity_x *= factor
                self.velocity_y *= factor

        # Limit max speed
        speed = math.hypot(self.velocity_x, self.velocity_y)
        if speed > self.max_speed:
            factor = self.max_speed / speed
            self.velocity_x *= factor
            self.velocity_y *= factor

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Boundary collision
        padding = 20
        if self.x < padding:
            self.x = padding
            self.velocity_x = -self.velocity_x * 0.5
        if self.x > WIDTH - padding:
            self.x = WIDTH - padding
            self.velocity_x = -self.velocity_x * 0.5
        if self.y < padding:
            self.y = padding
            self.velocity_y = -self.velocity_y * 0.5
        if self.y > HEIGHT - padding:
            self.y = HEIGHT - padding
            self.velocity_y = -self.velocity_y * 0.5

        # Planet collision
        for planet in planets:
            dist = math.hypot(self.x - planet[0], self.y - planet[1])
            if dist < planet[2] + 15:  # Spaceship radius approx 15
                # Simple bounce
                normal_x = (self.x - planet[0]) / dist
                normal_y = (self.y - planet[1]) / dist
                dot = self.velocity_x * normal_x + self.velocity_y * normal_y
                self.velocity_x -= 2 * dot * normal_x
                self.velocity_y -= 2 * dot * normal_y
                # Move out of collision
                self.x = planet[0] + (dist + 16) * normal_x
                self.y = planet[1] + (dist + 16) * normal_y

        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect.topleft)

def plot_circle_points(surface, xc, yc, x, y, color):
    points = [
        (xc + x, yc + y),
        (xc - x, yc + y),
        (xc + x, yc - y),
        (xc - x, yc - y),
        (xc + y, yc + x),
        (xc - y, yc + x),
        (xc + y, yc - x),
        (xc - y, yc - x),
    ]
    for point in points:
        if 0 <= point[0] < WIDTH and 0 <= point[1] < HEIGHT:
            surface.set_at(point, color)

def midpoint_circle(surface, xc, yc, radius, color):
    x = 0
    y = radius
    p = 1 - radius
    plot_circle_points(surface, xc, yc, x, y, color)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(surface, xc, yc, x, y, color)

def draw_planet(surface, xc, yc, radius, color):
    pygame.draw.circle(surface, color, (int(xc), int(yc)), radius)

def draw_stars(surface):
    for x, y, size in stars:
        pygame.draw.circle(surface, WHITE, (x, y), size)

def draw_galaxies(surface):
    for gx, gy, size in galaxies:
        arms = 3
        turns = 2
        max_radius = size // 2
        for arm in range(arms):
            for t in range(100):
                angle = (t / 100) * turns * 2 * math.pi + (arm * 2 * math.pi / arms)
                radius = max_radius * (t / 100)
                x = gx + radius * math.cos(angle)
                y = gy + radius * math.sin(angle)
                alpha = max(0, 150 - t * 1.5)
                dot_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(dot_surf, (200, 200, 255, int(alpha)), (3, 3), 3)
                surface.blit(dot_surf, (x - 3, y - 3))
        core_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(core_surf, (255, 255, 230, 180), (size//2, size//2), size//4)
        surface.blit(core_surf, (gx - size//2, gy - size//2))

def draw_saturn_ring(surface, x, y, planet_radius):
    ring_width = planet_radius + 6
    ring_height = planet_radius // 2
    ring_color = (210, 180, 140)
    
    ring_surf = pygame.Surface((ring_width*4, ring_height*4), pygame.SRCALPHA)
    for i in range(3):
        pygame.draw.ellipse(
            ring_surf,
            (ring_color[0], ring_color[1], ring_color[2], 120 - i*30),
            (i*2, i*2, ring_width*4 - i*4, ring_height*4 - i*4),
            2
        )
    rotated_ring = pygame.transform.rotate(ring_surf, 20)
    rect = rotated_ring.get_rect(center=(int(x), int(y)))
    surface.blit(rotated_ring, rect)

def draw_asteroid_belt(surface, xc, yc, inner_radius, outer_radius):
    num_asteroids = 150
    bright_red = (255, 50, 50)
    for _ in range(num_asteroids):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(inner_radius, outer_radius)
        x = int(xc + radius * math.cos(angle))
        y = int(yc + radius * math.sin(angle))
        pygame.draw.circle(surface, bright_red, (x, y), 2)
        highlight_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(highlight_surf, (255, 255, 255, 180), (3, 3), 1)
        surface.blit(highlight_surf, (x - 3, y - 3))
        glow_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 50, 50, 70), (4, 4), 3)
        surface.blit(glow_surf, (x - 4, y - 4))

def draw_boundary(surface):
    pygame.draw.rect(surface, (100, 100, 100), (0, 0, WIDTH, HEIGHT), 5)

def draw_reset_button(surface):
    font = pygame.font.SysFont("Arial", 20)
    button_rect = pygame.Rect(WIDTH - 100, 10, 90, 30)
    pygame.draw.rect(surface, (50, 50, 50), button_rect)
    pygame.draw.rect(surface, WHITE, button_rect, 2)
    label = font.render("Reset", True, WHITE)
    surface.blit(label, (WIDTH - 85, 15))
    return button_rect

def main():
    if platform.system() == "Emscripten":
        print("This game is not compatible with Pyodide/Emscripten due to pygame dependencies.")
        return

    spaceship = Spaceship()
    clock = pygame.time.Clock()
    angles = [i * (2*math.pi / 8) for i in range(8)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    spaceship.reset()

        window.fill(BLACK)

        draw_stars(window)
        draw_galaxies(window)
        draw_boundary(window)

        pygame.draw.circle(window, YELLOW, (WIDTH//2, HEIGHT//2), 30)

        for r in ORBIT_RADII:
            midpoint_circle(window, WIDTH//2, HEIGHT//2, r, WHITE)

        draw_asteroid_belt(window, WIDTH//2, HEIGHT//2, 155, 195)

        # Update and draw planets, store positions for collision
        planets = []
        for i in range(8):
            angles[i] += SPEEDS[i]
            x = WIDTH // 2 + ORBIT_RADII[i] * math.cos(angles[i])
            y = HEIGHT // 2 + ORBIT_RADII[i] * math.sin(angles[i])
            planets.append((x, y, PLANET_RADII[i]))
            draw_planet(window, x, y, PLANET_RADII[i], COLORS[i])
            draw_planet_label(window, PLANET_NAMES[i], x, y)
            if i == 5:
                draw_saturn_ring(window, x, y, PLANET_RADII[i])

        spaceship.update(planets)
        spaceship.draw(window)

        reset_button = draw_reset_button(window)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    import platform
    main()