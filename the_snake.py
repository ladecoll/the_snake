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
    """Родительский класс игровых объектов.

    Атрибут body_color задается при инициализации
    объектов дочерних классов и не определен заранее"""
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))  # Положение объекта на экране по умолчанию

    def __init__(self, position, body_color):
        """Используется только при инициализации объектов дочерних классов."""
        self.position = position
        self.body_color = body_color

    def draw(self, rect):
        """Отрисовывает переданный экземпляр дочернего класса."""
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Использует цвет из дочернего класса, поскольку атрибут цвета уникален для каждого дочернего класса.


class Apple(GameObject):
    """Дочерний класс Gameobject.

    Атрибут position определяет позицию объекта и не определен заранее."""
    body_color = APPLE_COLOR  # Цвет объекта

    def __init__(self):
        """Создает объект Apple с случайной позицией и заданным цветом"""
        self.randomize_position()
        super().__init__(self.position, self.body_color)
        # Передает сгенерированные координаты и заданный цвет в инициализатор родительского класса

    def draw_apple(self):
        """Отрисовывет объект Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        # Созает квадрат pygame при помощи position, передает в метод draw родительского класса
        super().draw(rect)

    def randomize_position(self):
        """Генерирует атрибут position"""
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (position_x, position_y)


class Snake(GameObject):
    """Дочерний класс Gameobject.

    Атрибут last определяет последний сегмент змейки и не определен заранее"""
    body_color = SNAKE_COLOR  # Цвет объекта
    direction = RIGHT  # Yаправление движения
    next_direction = None  # Направление движения в следующей итерации основного цикла
    positions = [GameObject.position]  # Cписок позиций сегментов змейки

    def __init__(self):
        """Создает объект Snake с заданным цветом"""
        for position in self.positions:
            super().__init__(self.position, self.body_color)  # Передает позицию и заданный цвет в инициализатор родительского класса
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def move(self):
        """Добавляет элемент в начало списка positions и удаляет элемент в конце."""
        new_x = self.get_head_position()[0] + self.direction[0] * GRID_SIZE
        new_y = self.get_head_position()[1] + self.direction[1] * GRID_SIZE
        # Вычисляет новую позицию головы из текущей и текущего направления движения.
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
        self.positions.insert(0, new_head)
        self.last = self.positions.pop(-1)
        # Перемещает последний сегмент в атрибут last.

    def draw_snake(self):
        """Рисует объект Snake."""
        for position in self.positions:  # Цикл перебирает позиции сегментов змейки
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            super().draw(rect)  # Каждая позиция передается в  метод draw родительского класса
        if self.last:  # Стирает последний сегмент змейки
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Меняет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку после проигрыша"""
        self.positions = [GameObject.position]  # Позиция объекта по умолчанию
        self.direction = choice([UP, DOWN, LEFT, RIGHT])  # Случайное направление движения
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)  # Стирает тело змейки с экрана


def main():
    pygame.init()
    apple = Apple()
    snake = Snake()

    def generate_new_apple_position():
        """Запускает генерацию позиции яблока."""
        apple.randomize_position()
        if apple.position in snake.positions:
            generate_new_apple_position()  # Повторяет пока позиция совпадает с позицией сегмента змейки.

    while True:
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
        snake.move()
        if snake.get_head_position() == apple.position:
            generate_new_apple_position()
            snake.positions.append(snake.last)
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        snake.update_direction()
        snake.draw_snake()
        apple.draw_apple()
        pygame.display.update()


if __name__ == '__main__':
    main()