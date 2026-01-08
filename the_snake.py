from random import randint
import pygame

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

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10  

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов"""
    def __init__(self, body_color=None, position=None):
        self.position = position
        self.body_color = body_color
    
    def draw(self):
        """Абстрактный метод для отрисовки объекта"""
        pass
    
    def update(self):
        """Метод для обновления состояния объекта"""
        pass


class Apple(GameObject):
    """Класс для яблока"""
    def __init__(self, snake_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.snake_positions = snake_positions if snake_positions else []
        self.position = self.randomize_position()
    
    def randomize_position(self):
        """Генерация случайной позиции яблока"""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)
            
            # Проверяем, чтобы яблоко не появилось на змейке
            if position not in self.snake_positions:
                return position
    
    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки"""
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
    
    def reset(self):
        """Сброс состояния змейки"""
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        # Выравниваем позицию по сетке
        start_x = (start_x // GRID_SIZE) * GRID_SIZE
        start_y = (start_y // GRID_SIZE) * GRID_SIZE
        
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
    
    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """Перемещение змейки"""
        head = self.get_head_position()
        dx, dy = self.direction
        
        # Вычисляем новую позицию головы с учетом телепортации через границы
        new_x = (head[0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверяем столкновение с собой
        if new_head in self.positions[1:]:  # Исключаем голову из проверки
            self.reset()
            return True  # Возвращаем True при столкновении
        
        # Добавляем новую голову
        self.positions.insert(0, new_head)
        
        # Сохраняем последнюю позицию для затирания
        self.last = self.positions[-1] if len(self.positions) > self.length else None
        
        # Удаляем хвост, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return False  # Возвращаем False если столкновения не было
    
    def draw(self):
        """Отрисовка змейки"""
        # Отрисовка тела змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
    
    def get_head_position(self):
        """Получение позиции головы змейки"""
        return self.positions[0]
    
    def grow(self):
        """Увеличение длины змейки"""
        self.length += 1


def handle_keys(snake):
    """Обработка нажатий клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            # Обработка управления с проверкой на противоположное направление
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры"""
    # Инициализация PyGame:
    pygame.init()
    
    # Создание объектов игры
    snake = Snake()
    apple = Apple(snake.positions)
    
    while True:
        # Ограничение FPS
        clock.tick(SPEED)
        
        # Обработка ввода
        handle_keys(snake)
        
        # Обновление состояния змейки
        snake.update_direction()
        collision = snake.move()
        
        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple = Apple(snake.positions)  # Создаем новое яблоко
        
        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана
        apple.draw()
        snake.draw()
        
        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()