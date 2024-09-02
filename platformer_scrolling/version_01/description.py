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

        screen.fill(SKY_BLUE)  # Устанавливаем цвет фона
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()

# Объяснение кода:

'''
1. Инициализация Pygame и настройка экрана:

Мы инициализируем Pygame и устанавливаем размеры экрана, а также частоту кадров.

2. Константы и цвета:

Устанавливаем цвета для земли, неба, игрока и т.д.

3. Класс Player (игрок):

Создаем спрайт игрока, который может двигаться влево и вправо, а также прыгать.
Добавлена гравитация: игроку постоянно добавляется скорость вниз, и он останавливается, когда касается земли.

4. Класс Ground (земля):

Создаем спрайт земли, который расположен внизу экрана и имеет ширину экрана.

5. Главная функция main():

Основной игровой цикл обрабатывает события, обновляет позиции спрайтов и рисует их на экране.
'''

# Как запустить:

'''
1. Сохраните код в файл, например, platformer.py.
2. Убедитесь, что у вас установлен Pygame (pip install pygame).
3. Запустите игру с помощью Python: python platformer.py.

Теперь у вас есть простая игра-платформер с движением игрока, прыжками и гравитацией!
'''

# Давайте подробно разберем каждую часть кода для вашей игры-платформера.

'''
1. Инициализация и настройка

import pygame
import sys

# Инициализация Pygame
pygame.init()

import pygame: Импортируем библиотеку Pygame для создания игры.
import sys: Импортируем модуль sys для выхода из программы.
pygame.init(): Инициализируем все модули Pygame.

2. Константы экрана и параметры

# Константы экрана
WIDTH, HEIGHT = 800, 600
FPS = 60

WIDTH, HEIGHT: Задаем размеры экрана в пикселях (ширина 800, высота 600).
FPS: Частота обновления экрана в кадрах в секунду (60 FPS).

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

Определяем цвета в формате RGB.

# Параметры игрока
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 35
PLAYER_COLOR = BLACK
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = 15
PLAYER_MOVE_SPEED = 5

Задаем параметры игрока: ширину, высоту, цвет, силу гравитации, силу прыжка и скорость перемещения.

# Параметры земли
GROUND_HEIGHT = 20
GROUND_COLOR = GREEN

Задаем параметры земли: высоту и цвет.

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

pygame.display.set_mode((WIDTH, HEIGHT)): Создаем экран с заданными размерами.
pygame.display.set_caption("Платформер"): Устанавливаем заголовок окна игры.
clock = pygame.time.Clock(): Создаем объект для управления частотой кадров.

3. Класс Player (игрок)

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

class Player(pygame.sprite.Sprite): Определяем класс игрока, наследуя от pygame.sprite.Sprite.
super().__init__(): Инициализируем родительский класс.
self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)): Создаем поверхность (пиксельное представление) игрока.
self.image.fill(PLAYER_COLOR): Заполняем поверхность цветом игрока.
self.rect = self.image.get_rect(): Получаем прямоугольник для определения позиции и размера.
self.rect.x = 50: Устанавливаем начальное положение игрока по горизонтали.
self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT: Устанавливаем начальное положение игрока по вертикали, так чтобы он стоял на земле.
self.velocity_y = 0: Инициализируем вертикальную скорость.
self.is_jumping = False: Флаг для проверки, прыгает ли игрок.

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

def update(self): Метод обновления состояния игрока.
keys = pygame.key.get_pressed(): Получаем состояние всех клавиш.
if keys[pygame.K_LEFT]: Если нажата клавиша влево, перемещаем игрока влево.
if keys[pygame.K_RIGHT]: Если нажата клавиша вправо, перемещаем игрока вправо.
self.velocity_y += PLAYER_GRAVITY: Применяем гравитацию, увеличивая вертикальную скорость.
self.rect.y += self.velocity_y: Обновляем вертикальное положение игрока.
if self.rect.bottom >= HEIGHT - GROUND_HEIGHT: Проверяем, касается ли игрок земли.
self.rect.bottom = HEIGHT - GROUND_HEIGHT: Устанавливаем игрока на землю.
self.velocity_y = 0: Обнуляем вертикальную скорость.
self.is_jumping = False: Останавливаем прыжок.

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -PLAYER_JUMP_STRENGTH
            self.is_jumping = True

def jump(self): Метод для прыжка.
if not self.is_jumping: Проверяем, прыгает ли уже игрок.
self.velocity_y = -PLAYER_JUMP_STRENGTH: Устанавливаем вертикальную скорость вверх.
self.is_jumping = True: Устанавливаем флаг прыжка.

4. Класс Ground (земля)

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, GROUND_HEIGHT))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - GROUND_HEIGHT

class Ground(pygame.sprite.Sprite): Определяем класс земли, наследуя от pygame.sprite.Sprite.
self.image = pygame.Surface((WIDTH, GROUND_HEIGHT)): Создаем поверхность земли, которая будет растягиваться по всей ширине экрана.
self.image.fill(GROUND_COLOR): Заполняем поверхность цветом земли.
self.rect = self.image.get_rect(): Получаем прямоугольник для определения позиции и размера.
self.rect.x = 0: Устанавливаем положение земли по горизонтали.
self.rect.y = HEIGHT - GROUND_HEIGHT: Устанавливаем положение земли по вертикали, чтобы она была внизу экрана.

5. Главная функция

def main():
    all_sprites = pygame.sprite.Group()
    
    # Создание игрока
    player = Player()
    all_sprites.add(player)
    
    # Создание земли
    ground = Ground()
    all_sprites.add(ground)

def main(): Основная функция игры.
all_sprites = pygame.sprite.Group(): Создаем группу для хранения всех спрайтов.
player = Player(): Создаем объект игрока.
all_sprites.add(player): Добавляем игрока в группу спрайтов.
ground = Ground(): Создаем объект земли.
all_sprites.add(ground): Добавляем землю в группу спрайтов.

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

        screen.fill(SKY_BLUE)  # Устанавливаем цвет фона
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

while True: Главный игровой цикл, который продолжается до тех пор, пока игра не завершится.
for event in pygame.event.get(): Обрабатываем все события.
if event.type == pygame.QUIT: Если событие — закрытие окна, завершаем игру.
elif event.type == pygame.KEYDOWN: Если нажата клавиша.
if event.key == pygame.K_SPACE: Если нажата клавиша пробел, вызываем метод jump() у игрока.
all_sprites.update(): Обновляем состояние всех спрайтов.
screen.fill(SKY_BLUE): Заполняем экран цветом неба.
all_sprites.draw(screen): Рисуем все спрайты на экране.
pygame.display.flip(): Обновляем экран.
clock.tick(FPS): Ограничиваем частоту кадров до 60 FPS.

6. Запуск игры

if __name__ == "__main__":
    main()

if __name__ == "__main__":: Проверяем, что скрипт запущен как основная программа.
main(): Запускаем главную функцию игры.
'''

