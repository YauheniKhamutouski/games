import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы экрана
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
MOUNTAIN_COLOR = (139, 137, 137)  # Цвет гор (темно-серый)
TREE_BROWN = (139, 69, 19)  # Цвет ствола дерева (коричневый)
TREE_GREEN = (34, 139, 34)  # Цвет листвы дерева (темно-зеленый)

# Параметры игрока
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 35
PLAYER_COLOR = BLACK
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = 15
PLAYER_MOVE_SPEED = 5

# Параметры земли
GROUND_HEIGHT = 20
GROUND_COLOR = GREEN

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

# Функция отрисовки фонов
def draw_background():
    # Дальний фон (небо)
    screen.fill(SKY_BLUE)

    # Средний фон (горы)
    # Рисуем горы, их базовая линия будет совпадать с высотой земли
    pygame.draw.polygon(screen, MOUNTAIN_COLOR, [(0, HEIGHT - GROUND_HEIGHT), (200, HEIGHT - GROUND_HEIGHT - 150), (400, HEIGHT - GROUND_HEIGHT)])
    pygame.draw.polygon(screen, MOUNTAIN_COLOR, [(300, HEIGHT - GROUND_HEIGHT), (500, HEIGHT - GROUND_HEIGHT - 200), (700, HEIGHT - GROUND_HEIGHT)])

    # Ближний фон (деревья)
    pygame.draw.rect(screen, TREE_BROWN, (50, HEIGHT - GROUND_HEIGHT - 60, 20, 60))  # Ствол дерева
    pygame.draw.circle(screen, TREE_GREEN, (60, HEIGHT - GROUND_HEIGHT - 80), 30)  # Крона дерева

    pygame.draw.rect(screen, TREE_BROWN, (200, HEIGHT - GROUND_HEIGHT - 60, 20, 60))  # Ствол дерева
    pygame.draw.circle(screen, TREE_GREEN, (210, HEIGHT - GROUND_HEIGHT - 80), 30)  # Крона дерева

# Класс Player (игрок)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_MOVE_SPEED

        # Применение гравитации
        self.velocity_y += PLAYER_GRAVITY
        self.rect.y += self.velocity_y

        # Проверка на касание земли
        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -PLAYER_JUMP_STRENGTH
            self.is_jumping = True

# Класс Ground (земля)
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, GROUND_HEIGHT))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - GROUND_HEIGHT

def main():
    all_sprites = pygame.sprite.Group()
    
    # Создание игрока
    player = Player()
    all_sprites.add(player)
    
    # Создание земли
    ground = Ground()
    all_sprites.add(ground)

    # Главный игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        all_sprites.update()

        # Отрисовка фонов
        draw_background()
        
        # Отрисовка всех спрайтов
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()

# Объяснение кода

'''
1. Импорт библиотек

import pygame
import sys

pygame используется для создания игры, отрисовки графики и обработки ввода.
sys предоставляет функции для завершения работы программы.

2. Инициализация Pygame

pygame.init()

Инициализирует все модули Pygame, которые будут использоваться в игре.

3. Константы экрана

WIDTH, HEIGHT = 800, 600
FPS = 60

WIDTH и HEIGHT определяют размеры окна игры.
FPS устанавливает количество кадров в секунду для плавности анимации.

4. Цвета

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
MOUNTAIN_COLOR = (139, 137, 137)  # Цвет гор (темно-серый)
TREE_BROWN = (139, 69, 19)  # Цвет ствола дерева (коричневый)
TREE_GREEN = (34, 139, 34)  # Цвет листвы дерева (темно-зеленый)

Определяет цвета, которые будут использоваться в игре.

5. Параметры игрока

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 35
PLAYER_COLOR = BLACK
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = 15
PLAYER_MOVE_SPEED = 5

PLAYER_WIDTH и PLAYER_HEIGHT задают размеры игрока.
PLAYER_COLOR определяет цвет игрока.
PLAYER_GRAVITY и PLAYER_JUMP_STRENGTH управляют физикой прыжков.
PLAYER_MOVE_SPEED определяет скорость движения игрока.

6. Параметры земли

GROUND_HEIGHT = 20
GROUND_COLOR = GREEN

GROUND_HEIGHT задает высоту земли.
GROUND_COLOR определяет цвет земли.

7. Настройка экрана

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

Создает окно игры с указанными размерами.
Устанавливает заголовок окна.
clock используется для управления частотой обновления кадров.

8. Функция отрисовки фонов

def draw_background():
    # Дальний фон (небо)
    screen.fill(SKY_BLUE)

    # Средний фон (горы)
    pygame.draw.polygon(screen, MOUNTAIN_COLOR, [(0, HEIGHT - GROUND_HEIGHT), (200, HEIGHT - GROUND_HEIGHT - 150), (400, HEIGHT - GROUND_HEIGHT)])
    pygame.draw.polygon(screen, MOUNTAIN_COLOR, [(300, HEIGHT - GROUND_HEIGHT), (500, HEIGHT - GROUND_HEIGHT - 200), (700, HEIGHT - GROUND_HEIGHT)])

    # Ближний фон (деревья)
    pygame.draw.rect(screen, TREE_BROWN, (50, HEIGHT - GROUND_HEIGHT - 60, 20, 60))  # Ствол дерева
    pygame.draw.circle(screen, TREE_GREEN, (60, HEIGHT - GROUND_HEIGHT - 80), 30)  # Крона дерева

    pygame.draw.rect(screen, TREE_BROWN, (200, HEIGHT - GROUND_HEIGHT - 60, 20, 60))  # Ствол дерева
    pygame.draw.circle(screen, TREE_GREEN, (210, HEIGHT - GROUND_HEIGHT - 80), 30)  # Крона дерева

Дальний фон (небо): screen.fill(SKY_BLUE) заполняет весь экран цветом неба.
Средний фон (горы): Используем pygame.draw.polygon для рисования гор. Вертикальная позиция базовой линии гор установлена на уровне земли (HEIGHT - GROUND_HEIGHT), 
чтобы горы не висели в воздухе.

Ближний фон (деревья): Используем pygame.draw.rect для рисования стволов деревьев и pygame.draw.circle для крон деревьев. Высота деревьев скорректирована так, 
чтобы они стояли на уровне земли.

9. Класс Player

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_MOVE_SPEED

        # Применение гравитации
        self.velocity_y += PLAYER_GRAVITY
        self.rect.y += self.velocity_y

        # Проверка на касание земли
        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -PLAYER_JUMP_STRENGTH
            self.is_jumping = True

Конструктор __init__:

self.image создается как прямоугольная поверхность с размерами игрока и окрашивается в PLAYER_COLOR.
self.rect определяет положение игрока. Изначально он расположен внизу экрана, над землей.
self.velocity_y используется для управления вертикальной скоростью (гравитацией).
self.is_jumping проверяет, прыгает ли игрок.

Метод update():

Обрабатывает ввод с клавиатуры для движения игрока влево и вправо.
Применяет гравитацию и обновляет вертикальное положение игрока.
Проверяет, касается ли игрок земли, и корректирует его положение и скорость.

Метод jump():

Начинает прыжок, если игрок не прыгает. Устанавливает вертикальную скорость для прыжка.

10. Класс Ground

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, GROUND_HEIGHT))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - GROUND_HEIGHT

Конструктор __init__:
self.image создается как прямоугольная поверхность с размерами ширины экрана и высоты земли, и окрашивается в GROUND_COLOR.
self.rect определяет положение земли, которая располагается внизу экрана.

11. Основная функция main()

def main():
    all_sprites = pygame.sprite.Group()
    
    # Создание игрока
    player = Player()
    all_sprites.add(player)
    
    # Создание земли
    ground = Ground()
    all_sprites.add(ground)

    # Главный игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        all_sprites.update()

        # Отрисовка фонов
        draw_background()
        
        # Отрисовка всех спрайтов
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

Создание группы спрайтов:

all_sprites содержит все спрайты, которые будут обновляться и отрисовываться.

Создание игрока и земли:

Создаем экземпляры классов Player и Ground и добавляем их в группу all_sprites.

Главный игровой цикл:

Обрабатывает события, например, выход из игры и нажатие клавиш.
Обновляет состояние всех спрайтов (передвижение игрока, гравитация и т.д.).
Отрисовывает фоны и спрайты на экране.
Обновляет экран и управляет частотой кадров с помощью clock.tick(FPS).

12. Запуск игры

if __name__ == "__main__":
    main()

Запускает основную функцию игры, если скрипт выполняется напрямую.

Этот код создаёт простую платформенную игру, где игрок может двигаться влево и вправо, прыгать и взаимодействовать
 с окружающей средой. Фоны правильно отображаются на экране, а гравитация 
 и движение игрока реализованы с использованием Pygame.

'''
