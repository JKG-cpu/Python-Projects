import pygame
from random import randint
from sys import exit as cg
import os

def cc():
    os.system("cls" if os.name == 'nt' else 'clear')

class Apple:
    def __init__(self, grid_size, color="red"):
        self.screen = pygame.display.get_surface()
        self.grid_size = grid_size
        self.color = color
        self.redraw_pos()

    def redraw_pos(self):
        cols = self.screen.get_width() // self.grid_size
        rows = self.screen.get_height() // self.grid_size
        x = randint(0, cols - 1) * self.grid_size
        y = randint(0, rows - 1) * self.grid_size
        self.rect = pygame.Rect(x, y, self.grid_size, self.grid_size)

    def check_collisions(self, obj):
        if self.rect.colliderect(obj):
            self.redraw_pos()
            return True
        return False

    def update(self, snake_head):
        collided = self.check_collisions(snake_head)
        pygame.draw.rect(self.screen, self.color, self.rect)
        return collided

class Snake:
    def __init__(self, grid_size):
        self.screen = pygame.display.get_surface()
        self.grid_size = grid_size
        self.apple = Apple(grid_size)

        self.body = [
            pygame.Rect(350, 250, grid_size, grid_size)
        ]

        self.direction = 'right'
        self.grow = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.direction != 'left':
            self.direction = 'right'
        elif keys[pygame.K_a] and self.direction != 'right':
            self.direction = 'left'
        elif keys[pygame.K_w] and self.direction != 'down':
            self.direction = 'up'
        elif keys[pygame.K_s] and self.direction != 'up':
            self.direction = 'down'

    def movement(self):
        head = self.body[0].copy()
        if self.direction == 'right':
            head.x += self.grid_size
        elif self.direction == 'left':
            head.x -= self.grid_size
        elif self.direction == 'up':
            head.y -= self.grid_size
        elif self.direction == 'down':
            head.y += self.grid_size

        self.body.insert(0, head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def collisions(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.colliderect(segment):
                pygame.quit()
                cc()
                cg()

        if (head.left <  0-self.grid_size or head.right > self.screen.get_width() or
            head.top < 0 or head.bottom > self.screen.get_height()):
            pygame.quit()
            cc()
            cg()

    def update(self):
        self.handle_input()
        self.movement()
        collided = self.apple.update(self.body[0])
        if collided:
            self.grow = True
        self.collisions()

        for segment in self.body:
            pygame.draw.rect(self.screen, "green", segment)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((750, 500))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.grid_size = 25
        self.snake = Snake(self.grid_size)

    def main(self):
        while True:
            self.clock.tick(10)
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cc()
                    cg()

            self.snake.update()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.main()
