import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
BOID_COUNT = 300
MAX_SPEED = 4
NEIGHBOR_RADIUS = 50
SEPARATION_DISTANCE = 15

BLUE = (80, 180, 255)
GREY = (70, 70, 70)

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))

    def update(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)

        self.velocity += alignment + cohesion + separation
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        
        self.position += self.velocity
        self.wrap_around()
        self.mouse()

    def align(self, boids):
        avg_velocity = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < NEIGHBOR_RADIUS:
                avg_velocity += boid.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            avg_velocity = avg_velocity - self.velocity
        return avg_velocity * 0.05
    
    def cohere(self, boids):
        center_mass = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < NEIGHBOR_RADIUS:
                center_mass += boid.position
                count += 1
        if count > 0:
            center_mass /= count
            return (center_mass - self.position) * 0.01
        return pygame.Vector2(0, 0)
    
    def separate(self, boids):
        move = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < SEPARATION_DISTANCE:
                move -= (boid.position - self.position)
        return move * 0.05
    
    def wrap_around(self):
        if self.position.x > WIDTH: self.position.x = 0
        if self.position.x < 0: self.position.x = WIDTH
        if self.position.y > HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = HEIGHT

    def mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_position = pygame.Vector2(mouse_x, mouse_y)
        direction = mouse_position - self.position
        if direction.length() > 0:
            direction.normalize_ip()
            self.velocity += direction * 0.1
    
    def draw(self, screen):
        pygame.draw.circle(screen, GREY, (int(self.position.x), int(self.position.y)), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()
    boids = [Boid() for _ in range(BOID_COUNT)]
    
    running = True
    while running:
        screen.fill(BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for boid in boids:
            boid.update(boids)
            boid.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()