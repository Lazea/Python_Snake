"""Snake game with pygame"""

import sys
import pygame
import time
import numpy as np

# Game constants
BG_COLOR = (100, 100, 100)
SCORE_COLOR = (175,175,60)
SCORE_BOARD_COLOR = (60,60,60)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCORE_HEIGHT = 100
SCL = 20
COLS = int(SCREEN_WIDTH / SCL)
ROWS = int(SCREEN_HEIGHT / SCL)

FPS = 12

# Game objects
class Food():
    """Food that the player needs to eat"""

    def __init__(self):
        self.color = (210,90,90)
        self.x = 0
        self.y = 0
        self.set_location()
        self.value = 50

    def set_location(self):
        """Move food to new random location"""

        self.x = int(np.random.rand(1) * COLS) * SCL
        self.y = int(np.random.rand(1) * ROWS) * SCL

class Snake():
    """Snake the player controls"""

    def __init__(self, food):
        self.color = (255,255,255)
        self.value = 50
        self.prev_x = 0
        self.prev_y = 0
        self.x = 0
        self.y = 0
        self.direction = [1, 0]

        self.tails = []
        self.length = len(self.tails)

    def turn(self, new_dir):
        """Turns the direction as long as the new
        direction isn't 180 of current"""

        _dir = [new_dir[0] * -1,
                new_dir[1] * -1]
        if self.direction != _dir:
            self.direction = new_dir

    def move(self):
        """Updates the position by direction * scale"""

        # Move head
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += self.direction[0] * SCL
        self.y += self.direction[1] * SCL

        # Move tails
        for t in range(self.length):
            if t == 0:
                self.tails[t].move(self.prev_x, self.prev_y)
            else:
                prev_tail = self.tails[t - 1]
                self.tails[t].move(prev_tail.prev_x, prev_tail.prev_y)

        # Screen borders
        if self.x >= SCREEN_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = SCREEN_WIDTH - SCL
        if self.y >= SCREEN_HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT - SCL

    class Tail():
        """Snake tail object"""

        def __init__(self, head, x, y):
            self.color = head.color
            self.prev_x = x
            self.prev_y = y
            self.x = x
            self.y = y

        def move(self, x, y):
            """Updates to new position"""

            self.prev_x = self.x
            self.prev_y = self.y
            self.x = x
            self.y = y

    def grow(self):
        """Grow tail by 1"""

        if self.length == 0:
            tail = self.Tail(self, self.x, self.y)
        else:
            prev_tail = self.tails[self.length - 1]
            tail = self.Tail(self, prev_tail.x, prev_tail.y)

        self.tails.append(tail)
        self.length = len(self.tails)

    def eat(self, food):
        """Eat the food to grow the tail"""

        if self.x == food.x and self.y == food.y:
            food.set_location()
            self.grow()

            return True
        else:
            return False

    def is_dead(self):
        """Check if snake is bitting itself"""

        future_x = self.x + self.direction[0] * SCL
        future_y = self.y + self.direction[1] * SCL
        for tail in self.tails:
            if future_x == tail.x and future_y == tail.y:
                return True
        return False

# Draw functions
def draw(screen, time, score, objs):
    """Updates the screen with all objects in the game"""

    screen.fill(BG_COLOR)

    # Draw objects
    for obj in objs:
        try:
            pygame.draw.rect(screen, obj.color, (obj.x, obj.y, SCL, SCL), 0)
        except:
            print(obj.x, obj.y, obj.color)

    # Draw score board
    pygame.draw.rect(screen, SCORE_BOARD_COLOR,
                     (0, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_HEIGHT), 0)

    font = pygame.font.SysFont("monospace", 24, bold=True)
    score_label = font.render("SCORE: " + str(score), 1, SCORE_COLOR)
    score_rect = score_label.get_rect(center=(SCREEN_WIDTH * 0.15,
                                              SCORE_HEIGHT/2 + SCREEN_HEIGHT))
    screen.blit(score_label, score_rect)

    # Draw clock
    def format_time(t):
        seconds = int(t)
        minutes = int(seconds / 65)
        return str(minutes).zfill(2) + ':' + str(seconds).zfill(2)

    time_label = font.render("TIME: " + format_time(time), 1, SCORE_COLOR)
    time_rect = time_label.get_rect(center=(SCREEN_WIDTH * (1 - 0.15),
                                              SCORE_HEIGHT/2 + SCREEN_HEIGHT))
    screen.blit(time_label, (int(SCREEN_WIDTH * 0.6),
                        int(SCORE_HEIGHT * 0.38) + SCREEN_HEIGHT))

    pygame.display.update()

def pause(clock):
    paused = True
    while(paused):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        pygame.display.update()
        clock.tick(15)

# Game states
def pause_game(screen, clock):
    """Pauses the game"""

    font = pygame.font.SysFont("monospace", 35, bold=True)
    pause_label = font.render("PAUSED", 1, SCORE_COLOR)
    label_rect = pause_label.get_rect(center=(SCREEN_WIDTH/2,
                                              SCREEN_HEIGHT/2))
    screen.blit(pause_label, label_rect)

    pause(clock)

def end_game(screen, clock):
    """Ends the game and asks to play again"""

    screen.fill(BG_COLOR)

    pause(clock)

def quit_game():
    """Quits the game"""

    pygame.quit()
    sys.exit()

def main():
    """Main gameplay logic"""

    # Game setup
    pygame.init()
    score = 0
    fps = FPS

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + SCORE_HEIGHT))

    food = Food()
    snake = Snake(food)

    # Gameplay Loop
    start = time.time()
    while(True):
        for event in pygame.event.get():
            # Events
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.turn([-1,0])
                if event.key == pygame.K_UP:
                    snake.turn([0,-1])
                if event.key == pygame.K_RIGHT:
                    snake.turn([1,0])
                if event.key == pygame.K_DOWN:
                    snake.turn([0,1])
                if event.key == pygame.K_p:
                    pause_game(screen, clock)

        elapsed = clock.tick(fps)

        # Object states
        if snake.is_dead():
            end_game(screen, clock)
        snake.move()
        if snake.eat(food) : score += food.value

        objects = [tail for tail in snake.tails]
        objects.append(food)
        objects.append(snake)
        draw(screen, time.time() - start, score, objects)


if __name__ == "__main__":
    main()
