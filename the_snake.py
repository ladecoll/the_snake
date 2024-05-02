from random import choice, randint

import pygame
import sys

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


# Тут опишите все классы игры.
class GameObject:
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    body_color = APPLE_COLOR

    def __init__(self):
        self.randomize_position()
        super().__init__(self.position, self.body_color)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (position_x, position_y)


class Snake(GameObject):
    body_color = SNAKE_COLOR
    length = 1
    positions = [GameObject.position]
    direction = RIGHT
    next_direction = None

    def __init__(self):
        for position in self.positions:
            super().__init__(self.position, self.body_color)
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        new_x = self.get_head_position()[0] + self.direction[0] * GRID_SIZE
        new_y = self.get_head_position()[1] + self.direction[1] * GRID_SIZE
        if new_x == 640:
            new_x = 0
        elif new_x < 0:
            new_x = 640
        if new_y == 480:
            new_y = 0
        elif new_y < 0:
            new_y = 480
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        self.last = self.positions.pop(-1)

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        self.positions = [GameObject.position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    pygame.init()
    apple = Apple()
    snake = Snake()

    def generate_new_apple_position():
        '''Это функция'''
        apple.randomize_position()
        if apple.position in snake.positions:
            generate_new_apple_position()

    while True:
        '''
        todo: 
        сделать чтоб яблоко не могло генерироваться внутри змейки
        подвести под pip8
        сделать докстринг
        оптимизировать код
        понять зачем нужна snake.length
        '''
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            generate_new_apple_position()
            snake.positions.append(snake.last)
            snake.length += 1
            print(f'length = {snake.length}, фактическая длина = {len(snake.positions)}')
        '''for position in snake.positions[1:]:
            #if position == apple.position:
                #apple.randomize_position() - проверка выполняется 1 раз, если яблоко снова сгенерируется внутри змейки то так и будет
            if position == snake.get_head_position():
                snake.reset()'''
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
