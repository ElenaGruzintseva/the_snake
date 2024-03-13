from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

class GameObject:

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self):
        """"Метод будет определен в потомках"""
        raise NotImplementedError(f'Определите Draw {type(self).__name__}')

class Apple(GameObject):

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__()
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

class Snake(GameObject):

    def __init__(self, body_color=SNAKE_COLOR, length=1, direction=RIGHT, next_direction=None, last=None):
        super().__init__()
        self.body_color = body_color
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.last = last

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_position = list(self.get_head_position())
        if self.direction == RIGHT:
            head_position = [head_position[0] + GRID_SIZE, head_position[1]]
            if head_position[0] > SCREEN_WIDTH:
                head_position[0] -= SCREEN_WIDTH
        elif self.direction == LEFT:
            head_position = [head_position[0] - GRID_SIZE, head_position[1]]
            if head_position[0] < 0:
                head_position[0] += SCREEN_WIDTH
        elif self.direction == UP:
            head_position = [head_position[0], head_position[1] - GRID_SIZE]
            if head_position[1] < 0:
                head_position[1] += SCREEN_HEIGHT
        elif self.direction == DOWN:
            head_position = [head_position[0], head_position[1] + GRID_SIZE]
            if head_position[1] > SCREEN_HEIGHT:
                head_position[1] -= SCREEN_HEIGHT

        head_position = tuple(head_position)

        if head_position in self.positions[2:]:
            self.reset()
            return
        else:
            self.positions.insert(0, head_position)

        if len(self.positions) > self.length:
            self.positions.pop()


    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]
    
    def reset(self):
        self.length = 1
        self.positions = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.direction = choice(UP, DOWN, RIGHT, LEFT)
        screen.fill(BOARD_BACKGROUND_COLOR)

def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple = Apple()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()

