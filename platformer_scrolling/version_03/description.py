import pygame
import sys
import random

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

# Параметры фона
MOUNTAIN_SCROLL_SPEED = 1.5  # Скорость движения гор (уменьшили скорость)
TREE_SCROLL_SPEED = 3.0  # Скорость движения деревьев
TREE_WIDTHS = [15, 20, 25, 30, 35]
TREE_HEIGHTS = [50, 60, 70, 80, 90]
MOUNTAIN_WIDTHS = [100, 120, 140, 160, 180]
MOUNTAIN_HEIGHTS = [100, 120, 140, 160, 180]

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

# Класс Player (игрок)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 120  # Позиция игрока, с учетом смещения вправо на 100 пикселей
        self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
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

# Класс Tree (дерево)
class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(TREE_BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height

        # Крона дерева
        self.leaf = pygame.Surface((width + 20, width + 20), pygame.SRCALPHA)
        pygame.draw.circle(self.leaf, TREE_GREEN, (width // 2 + 10, width // 2 + 10), width // 2 + 10)
        self.image.blit(self.leaf, (-10, -width // 2))

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

# Класс Mountain (гора)
class Mountain(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(MOUNTAIN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

def draw_background(trees, mountains):
    screen.fill(SKY_BLUE)

    # Отрисовка гор
    for mountain in mountains:
        screen.blit(mountain.image, (mountain.rect.x, mountain.rect.y))

    # Отрисовка деревьев
    for tree in trees:
        screen.blit(tree.image, (tree.rect.x, tree.rect.y))

def main():
    all_sprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    mountains = pygame.sprite.Group()

    # Создание игрока
    player = Player()
    all_sprites.add(player)
    
    # Создание земли
    ground = Ground()
    all_sprites.add(ground)

    # Генерация фонов
    scroll_x = 0
    spawn_tree_interval = 300  # Интервал между деревьями
    spawn_mountain_interval = 600  # Интервал между горами

    next_tree_spawn = spawn_tree_interval
    next_mountain_spawn = spawn_mountain_interval

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:  # Фон движется только при нажатии клавиши вправо
            scroll_x += PLAYER_MOVE_SPEED

            # Обновление всех деревьев и гор
            for tree in trees:
                tree.update(TREE_SCROLL_SPEED)
            for mountain in mountains:
                mountain.update(MOUNTAIN_SCROLL_SPEED)

            # Генерация новых деревьев и гор
            next_tree_spawn -= PLAYER_MOVE_SPEED
            if next_tree_spawn <= 0:
                tree_width = random.choice(TREE_WIDTHS)
                tree_height = random.choice(TREE_HEIGHTS)
                tree_x = WIDTH + random.randint(0, 200)
                tree_y = HEIGHT - GROUND_HEIGHT
                tree = Tree(tree_x, tree_y, tree_width, tree_height)
                trees.add(tree)
                next_tree_spawn = spawn_tree_interval

            next_mountain_spawn -= PLAYER_MOVE_SPEED
            if next_mountain_spawn <= 0:
                mountain_width = random.choice(MOUNTAIN_WIDTHS)
                mountain_height = random.choice(MOUNTAIN_HEIGHTS)
                mountain_x = WIDTH + random.randint(0, 400)
                mountain_y = HEIGHT - GROUND_HEIGHT
                mountain = Mountain(mountain_x, mountain_y, mountain_width, mountain_height)
                mountains.add(mountain)
                next_mountain_spawn = spawn_mountain_interval

        # Удаление деревьев и гор, которые вышли за пределы экрана
        for tree in trees:
            if tree.rect.right < 0:
                tree.kill()

        for mountain in mountains:
            if mountain.rect.right < 0:
                mountain.kill()

        # Обновление и отрисовка
        player.update()
        draw_background(trees, mountains)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()

# Давайте подробно рассмотрим каждую часть кода, чтобы понять, как работает игра.

'''
Импорт и инициализация

import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

1. Импорт библиотек:

pygame — библиотека для создания игр на Python.
sys — стандартная библиотека Python, используемая для работы с системными функциями.
random — стандартная библиотека Python для генерации случайных чисел.

2. Инициализация Pygame:

pygame.init() — инициализирует все необходимые модули Pygame. Эта команда подготавливает Pygame к использованию.

Константы экрана

# Константы экрана
WIDTH, HEIGHT = 800, 600
FPS = 60

WIDTH и HEIGHT задают ширину и высоту окна игры.
FPS (Frames Per Second) определяет частоту кадров игры. Это значение ограничивает количество обновлений экрана в секунду,
чтобы игра работала плавно и с одинаковой скоростью на всех устройствах.

Цвета

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
MOUNTAIN_COLOR = (139, 137, 137)  # Цвет гор (темно-серый)
TREE_BROWN = (139, 69, 19)  # Цвет ствола дерева (коричневый)
TREE_GREEN = (34, 139, 34)  # Цвет листвы дерева (темно-зеленый)

Определены цвета, которые будут использоваться в игре. Цвета представлены в формате RGB, где каждое число в скобках 
соответствует интенсивности красного, зеленого и синего каналов (от 0 до 255).

Параметры игрока и другие настройки

# Параметры игрока
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 35
PLAYER_COLOR = BLACK
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = 15
PLAYER_MOVE_SPEED = 5

PLAYER_WIDTH и PLAYER_HEIGHT — ширина и высота игрока (чёрного квадрата).
PLAYER_COLOR — цвет игрока, заданный как чёрный.
PLAYER_GRAVITY — значение гравитации, которое будет увеличивать скорость падения игрока.
PLAYER_JUMP_STRENGTH — сила прыжка, определяющая, насколько высоко прыгнет игрок.
PLAYER_MOVE_SPEED — скорость движения фона при движении вправо.

Параметры земли и фонов

# Параметры земли
GROUND_HEIGHT = 20
GROUND_COLOR = GREEN

# Параметры фона
MOUNTAIN_SCROLL_SPEED = 1.5  # Скорость движения гор (уменьшили скорость)
TREE_SCROLL_SPEED = 3.0  # Скорость движения деревьев
TREE_WIDTHS = [15, 20, 25, 30, 35]
TREE_HEIGHTS = [50, 60, 70, 80, 90]
MOUNTAIN_WIDTHS = [100, 120, 140, 160, 180]
MOUNTAIN_HEIGHTS = [100, 120, 140, 160, 180]

GROUND_HEIGHT и GROUND_COLOR задают высоту и цвет земли.
MOUNTAIN_SCROLL_SPEED и TREE_SCROLL_SPEED определяют скорость движения фонов (гор и деревьев).
TREE_WIDTHS и TREE_HEIGHTS — списки возможных ширин и высот деревьев.
MOUNTAIN_WIDTHS и MOUNTAIN_HEIGHTS — списки возможных ширин и высот гор.

Настройка экрана и создание объектов

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

pygame.display.set_mode((WIDTH, HEIGHT)) создаёт окно игры с заданными размерами.
pygame.display.set_caption("Платформер") устанавливает заголовок окна.
pygame.time.Clock() создаёт объект часов для управления скоростью игры (FPS).

Класс Player (Игрок)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 120  # Позиция игрока, с учетом смещения вправо на 100 пикселей
        self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
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

Класс Player наследуется от pygame.sprite.Sprite, что позволяет использовать встроенные функции 
Pygame для спрайтов (например, для отрисовки и проверки столкновений).

Метод __init__:
Создаёт поверхность (pygame.Surface) для игрока с заданными размерами.
Заполняет её чёрным цветом.
Определяет прямоугольник (self.rect) для игрока, чтобы легко управлять его позицией.
Задаёт начальную позицию игрока с учётом смещения.
Устанавливает начальную скорость velocity_y в 0 и флаг is_jumping в False.

Метод update:
Применяет гравитацию, увеличивая velocity_y.
Обновляет вертикальную позицию игрока.
Проверяет, достиг ли игрок земли. Если да, то устанавливает его позицию на уровень земли и сбрасывает скорость 
и флаг прыжка.

Метод jump:
Проверяет, не прыгает ли игрок. Если нет, то инициирует прыжок, устанавливая отрицательное значение velocity_y
и устанавливая флаг is_jumping в True.

Класс Ground (Земля)

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, GROUND_HEIGHT))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - GROUND_HEIGHT

Класс Ground также наследуется от pygame.sprite.Sprite.

Метод __init__:
Создаёт поверхность для земли с шириной окна и заданной высотой.
Заполняет поверхность зелёным цветом.
Определяет прямоугольник для позиции земли и устанавливает его внизу окна.

Класс Tree (Дерево)

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(TREE_BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height

        # Крона дерева
        self.leaf = pygame.Surface((width + 20, width + 20), pygame.SRCALPHA)
        pygame.draw.circle(self.leaf, TREE_GREEN, (width // 2 + 10, width // 2 + 10), width // 2 + 10)
        self.image.blit(self.leaf, (-10, -width // 2))

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

Класс Tree представляет дерево в игре.
Метод __init__:
Создаёт поверхность для дерева с заданной шириной и высотой.
Заполняет её коричневым цветом для ствола дерева.
Определяет прямоугольник для позиции дерева.
Рисует круглую крону дерева зелёного цвета и размещает её поверх ствола.

Метод update:
Перемещает дерево влево с заданной скоростью scroll_speed, имитируя движение фона.

Класс Mountain (Гора)

class Mountain(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(MOUNTAIN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

Класс Mountain представляет горы в игре.

Метод __init__:
Создаёт поверхность для горы с заданной шириной и высотой.
Заполняет её цветом, характерным для гор.
Определяет прямоугольник для позиции горы.

Метод update:
Перемещает гору влево с заданной скоростью scroll_speed.

Функция для отрисовки фона

def draw_background(trees, mountains):
    screen.fill(SKY_BLUE)

    # Отрисовка гор
    for mountain in mountains:
        screen.blit(mountain.image, (mountain.rect.x, mountain.rect.y))

    # Отрисовка деревьев
    for tree in trees:
        screen.blit(tree.image, (tree.rect.x, tree.rect.y))

Функция draw_background:

Заполняет фон неба голубым цветом (SKY_BLUE).
Отрисовывает все горы и деревья на экране в их текущих позициях.

Основная игровая функция

def main():
    all_sprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    mountains = pygame.sprite.Group()

    # Создание игрока
    player = Player()
    all_sprites.add(player)
    
    # Создание земли
    ground = Ground()
    all_sprites.add(ground)

    # Генерация фонов
    scroll_x = 0
    spawn_tree_interval = 300  # Интервал между деревьями
    spawn_mountain_interval = 600  # Интервал между горами

    next_tree_spawn = spawn_tree_interval
    next_mountain_spawn = spawn_mountain_interval

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:  # Фон движется только при нажатии клавиши вправо
            scroll_x += PLAYER_MOVE_SPEED

            # Обновление всех деревьев и гор
            for tree in trees:
                tree.update(TREE_SCROLL_SPEED)
            for mountain in mountains:
                mountain.update(MOUNTAIN_SCROLL_SPEED)

            # Генерация новых деревьев и гор
            next_tree_spawn -= PLAYER_MOVE_SPEED
            if next_tree_spawn <= 0:
                tree_width = random.choice(TREE_WIDTHS)
                tree_height = random.choice(TREE_HEIGHTS)
                tree_x = WIDTH + random.randint(0, 200)
                tree_y = HEIGHT - GROUND_HEIGHT
                tree = Tree(tree_x, tree_y, tree_width, tree_height)
                trees.add(tree)
                next_tree_spawn = spawn_tree_interval

            next_mountain_spawn -= PLAYER_MOVE_SPEED
            if next_mountain_spawn <= 0:
                mountain_width = random.choice(MOUNTAIN_WIDTHS)
                mountain_height = random.choice(MOUNTAIN_HEIGHTS)
                mountain_x = WIDTH + random.randint(0, 400)
                mountain_y = HEIGHT - GROUND_HEIGHT
                mountain = Mountain(mountain_x, mountain_y, mountain_width, mountain_height)
                mountains.add(mountain)
                next_mountain_spawn = spawn_mountain_interval

        # Удаление деревьев и гор, которые вышли за пределы экрана
        for tree in trees:
            if tree.rect.right < 0:
                tree.kill()

        for mountain in mountains:
            if mountain.rect.right < 0:
                mountain.kill()

        # Обновление и отрисовка
        player.update()
        draw_background(trees, mountains)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

Создание групп спрайтов:

all_sprites содержит все объекты, которые будут отрисовываться.
trees и mountains содержат деревья и горы соответственно.

Создание игрока и земли:

player и ground создаются и добавляются в группу all_sprites.

Переменные для генерации деревьев и гор:

scroll_x отслеживает движение фона.
spawn_tree_interval и spawn_mountain_interval определяют интервал генерации деревьев и гор.
next_tree_spawn и next_mountain_spawn отслеживают, когда нужно создать новые деревья и горы.

Главный цикл игры:

Обрабатывает события (например, нажатие клавиш).
Если нажата клавиша RIGHT, фон и все объекты начинают двигаться влево.
Генерируются новые деревья и горы, когда достигается определенный интервал.
Удаляются деревья и горы, которые вышли за пределы экрана.
Обновляется игрок, отрисовывается фон и все спрайты, а также обновляется дисплей.
clock.tick(FPS) регулирует частоту кадров.

Запуск игры

if __name__ == "__main__":
    main()

Этот блок кода запускает функцию main, если файл запущен напрямую, а не импортирован как модуль.

Теперь код должен правильно обрабатывать прыжок, держать игрока на месте и генерировать деревья
и горы случайным образом с использованием заданных шаблонов.
'''
