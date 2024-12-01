import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Cat")

# Load images
cat_image = pygame.image.load('cat.png')
cat_image = pygame.transform.scale(cat_image, (50, 50))

# Cat class
class Cat:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.gravity = 0.5
        self.lift = -10
        self.velocity = 0

    def show(self):
        screen.blit(cat_image, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        self.velocity = self.lift

# Pipe class
class Pipe:
    def __init__(self):
        self.spacing = 150
        self.top = random.randint(50, SCREEN_HEIGHT // 2)
        self.bottom = SCREEN_HEIGHT - self.top - self.spacing
        self.x = SCREEN_WIDTH
        self.w = 50
        self.speed = 3

    def show(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.w, self.top))
        pygame.draw.rect(screen, GREEN, (self.x, SCREEN_HEIGHT - self.bottom, self.w, self.bottom))

    def update(self):
        self.x -= self.speed

    def off_screen(self):
        return self.x < -self.w

    def hits(self, cat):
        if cat.y < self.top or cat.y > SCREEN_HEIGHT - self.bottom:
            if self.x < cat.x < self.x + self.w:
                return True
        return False

def main():
    clock = pygame.time.Clock()
    cat = Cat()
    pipes = [Pipe()]

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cat.up()

        cat.update()
        cat.show()

        if pipes[-1].x < SCREEN_WIDTH // 2:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.show()
            if pipe.hits(cat):
                print("Game Over!")
                running = False

        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
