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

# Позиция змейки по умолчанию
SNAKE_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

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
    """Родительский класс игровых объектов.

    Цвет body_color и координаты position
    определяются в дочерних объектах
    """

    def __init__(self, position=None, body_color=None):
        """Используется только при инициализации объектов дочерних классов."""
        self.position = position
        self.body_color = body_color

    def draw(self, position, body_color):
        """Отрисовывает переданный экземпляр дочернего класса."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Использует цвет из дочернего класса,
        # поскольку атрибут цвета уникален для каждого дочернего класса.


class Apple(GameObject):
    """Дочерний класс Gameobject.

    Атрибут position определяет позицию объекта и не определен заранее.
    """

    def __init__(self):
        """Создает объект Apple с случайной позицией и заданным цветом"""
        super().__init__(self.randomize_position(), APPLE_COLOR)

    def draw_apple(self):
        """Отрисовывет объект Apple."""
        super().draw(self.position, self.body_color)

    def randomize_position(self, positions=None):
        """Генерирует атрибут position"""
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        if positions and (position_x, position_y) in positions:
            self.randomize_position()
        self.position = (position_x, position_y)
        return position_x, position_y


class Snake(GameObject):
    """Дочерний класс Gameobject.

    Атрибут last определяет последний сегмент змейки и не определен заранее
    """

    direction = RIGHT  # Yаправление движения
    next_direction = None
    # Направление движения в следующей итерации основного цикла
    positions = [SNAKE_POSITION]
    # Cписок позиций сегментов змейки

    def __init__(self):
        """Создает объект Snake с заданным цветом"""
        super().__init__(SNAKE_POSITION, SNAKE_COLOR)
        # Передает позицию и заданный цвет
        # в инициализатор родительского класса
        self.last = None

    def move(self):
        """Добавляет элемент в начало positions и удаляет элемент в конце."""
        new_x = self.positions[0][0] + self.direction[0] * GRID_SIZE
        new_y = self.positions[0][1] + self.direction[1] * GRID_SIZE
        # Вычисляет новую позицию головы из текущей и направления движения.
        if new_x == 640:
            new_x = 0
        elif new_x < 0:
            new_x = 640
        if new_y == 480:
            new_y = 0
        elif new_y < 0:
            new_y = 480
        # Если задет край экрана, перемещает в противоположную сторону.
        new_head = (new_x, new_y)
        self.positions.insert(0, (new_x, new_y))
        self.last = self.positions.pop(-1)
        # Перемещает последний сегмент в атрибут last.
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw_snake(self):
        """Рисует объект Snake."""
        super().draw(self.positions[0], SNAKE_COLOR)
        last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку после проигрыша"""
        self.positions = [SNAKE_POSITION]  # Позиция объекта по умолчанию
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        # Случайное направление движения
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)  # Стирает тело змейки с экрана


def handle_keys(events, snake):
    """Обрабатывает действия пользователя"""
    for event in events:
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


def main():
    """Основная функция."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:  # Основной цикл
        clock.tick(SPEED)
        handle_keys(pygame.event.get(), snake)
        snake.move()
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            if len(snake.positions) == GRID_WIDTH * GRID_HEIGHT:
                # Остановка игры, поздравление с победой
                pass
            apple.randomize_position(snake.positions)
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
        snake.draw_snake()
        apple.draw_apple()
        pygame.display.update()


if __name__ == '__main__':
    main()
