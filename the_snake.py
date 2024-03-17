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
        """The method will be defined in the descendants"""
        raise NotImplementedError(f'Определите Draw {type(self).__name__}')


class Apple(GameObject):
    """Creating Apple class"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Determine the random position of the apple"""
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
        )

    def draw(self):
        """Drawing apple"""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Creating Snake class"""

    def __init__(self, body_color=SNAKE_COLOR, length=1, direction=RIGHT,
                 next_direction=None, last=None):
        super().__init__(body_color)
        self.body_color = body_color
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.last = last

    def update_direction(self):
        """Updating the snake's direction of movement"""
        if self.next_direction:  # Избавиться, Просто получать новое направление, через параметр метода.
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Processing the movement of the snake"""
        head_position = self.get_head_position()
        head_position = (
            ((head_position[0] + GRID_SIZE * self.direction[0]) %
             SCREEN_WIDTH),
            ((head_position[1] + GRID_SIZE * self.direction[1]) %
             SCREEN_HEIGHT)
        )
        self.positions.insert(0, head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

        #if head_position == self.positions:
            #self.reset() Должно быть в мейн

    def draw(self):
        """Drawing snake"""
       #for position in self.positions[:-1]:
       #    rect = (
       #        pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
       #    )
       #    pg.draw.rect(surface, self.body_color, rect)
       #    pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Get head position of snake"""
        return self.positions[0]

    def reset(self):
        """Reset the snake to the initial state"""
        self.length = 1
        #self.positions.clear()
        #self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.direction = choice(UP, DOWN, RIGHT, LEFT)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Processing keystrokes"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
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
    apple = Apple()

    while True:
        pg.init()
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:  # Использовать метод для получения головы.
            snake.length += 1
            apple = Apple()  # Вызвать метод random_pos.

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
