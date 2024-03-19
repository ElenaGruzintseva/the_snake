from random import choice, randint

import pygame as pg

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
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Creating an object class"""

    def __init__(self, body_color=(0, 0, 0)):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Defined in the descendants"""
        raise NotImplementedError(f'Определите Draw {type(self).__name__}')

    def draw_rect(self, position, body_color=(0, 0, 0)):
        """Drawing rect"""
        self.rect = pg.Rect((position), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, self.rect)
        if self.body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, self.rect, 1)


class Apple(GameObject):
    """Creating Apple class"""

    def __init__(self, snake=None, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.body_color = body_color

    def randomize_position(self, snake):
        """Determine the random position of the apple"""
        while True:
            self.position = (
                randint(1, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
                randint(1, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
            )
            for position in snake.positions:
                if self.position != position:
                    break
            break

    def draw(self):
        """Drawing apple"""
        self.draw_rect(self.position, self.body_color)


class Snake(GameObject):
    """Creating Snake class"""

    def __init__(self, body_color=SNAKE_COLOR, next_direction=None, last=None):
        super().__init__(body_color)
        self.reset()
        self.next_direction = next_direction
        self.last = last

    def update_direction(self):
        """Updating the snake's direction of movement"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Processing the movement of the snake"""
        head_x, head_y = self.get_head_position()
        direct_x, direct_y = self.direction

        self.position = (
            ((head_x + GRID_SIZE * direct_x) % SCREEN_WIDTH),
            ((head_y + GRID_SIZE * direct_y) % SCREEN_HEIGHT)
        )
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Drawing snake"""
        self.draw_rect(self.positions[0], self.body_color)

        if self.last:
            self.draw_rect(self.last, self.body_color)
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, self.rect)

    def get_head_position(self):
        """Get head position of snake"""
        return self.positions[0]

    def reset(self):
        """Reset the snake to the initial state"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Processing keystrokes"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.QUIT()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """The basic logic of the game"""
    snake = Snake()
    apple = Apple(snake)

    while True:
        pg.init()
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
