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
CLOUD_COLOR = WHITE  # Цвет облаков

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
MOUNTAIN_SCROLL_SPEED = 1.5  # Скорость движения гор
TREE_SCROLL_SPEED = 3.0  # Скорость движения деревьев
CLOUD_SCROLL_SPEED = 1.0  # Скорость движения облаков
TREE_WIDTHS = [15, 20, 25, 30, 35]
TREE_HEIGHTS = [50, 60, 70, 80, 90]
MOUNTAIN_WIDTHS = [100, 120, 140, 160, 180]
MOUNTAIN_HEIGHTS = [100, 120, 140, 160, 180]
CLOUD_WIDTHS = [80, 100, 120]  # Увеличены размеры облаков
CLOUD_HEIGHTS = [40, 60, 80]  # Увеличены размеры облаков

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

# Класс Cloud (облако)
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(CLOUD_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

def draw_background(trees, mountains, clouds):
    screen.fill(SKY_BLUE)

    # Отрисовка гор
    for mountain in mountains:
        screen.blit(mountain.image, (mountain.rect.x, mountain.rect.y))

    # Отрисовка деревьев
    for tree in trees:
        screen.blit(tree.image, (tree.rect.x, tree.rect.y))
    
    # Отрисовка облаков
    for cloud in clouds:
        screen.blit(cloud.image, (cloud.rect.x, cloud.rect.y))

def main():
    all_sprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    mountains = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

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
    spawn_cloud_interval = 400  # Интервал между облаками, увеличен для уменьшения количества

    next_tree_spawn = spawn_tree_interval
    next_mountain_spawn = spawn_mountain_interval
    next_cloud_spawn = spawn_cloud_interval

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

            # Обновление всех деревьев, гор и облаков
            for tree in trees:
                tree.update(TREE_SCROLL_SPEED)
            for mountain in mountains:
                mountain.update(MOUNTAIN_SCROLL_SPEED)
            for cloud in clouds:
                cloud.update(CLOUD_SCROLL_SPEED)

            # Генерация новых деревьев
            next_tree_spawn -= PLAYER_MOVE_SPEED
            if next_tree_spawn <= 0:
                tree_width = random.choice(TREE_WIDTHS)
                tree_height = random.choice(TREE_HEIGHTS)
                tree_x = WIDTH + random.randint(0, 200)
                tree_y = HEIGHT - GROUND_HEIGHT
                tree = Tree(tree_x, tree_y, tree_width, tree_height)
                trees.add(tree)
                next_tree_spawn = spawn_tree_interval

            # Генерация новых гор
            next_mountain_spawn -= PLAYER_MOVE_SPEED
            if next_mountain_spawn <= 0:
                mountain_width = random.choice(MOUNTAIN_WIDTHS)
                mountain_height = random.choice(MOUNTAIN_HEIGHTS)
                mountain_x = WIDTH + random.randint(0, 400)
                mountain_y = HEIGHT - GROUND_HEIGHT
                mountain = Mountain(mountain_x, mountain_y, mountain_width, mountain_height)
                mountains.add(mountain)
                next_mountain_spawn = spawn_mountain_interval

            # Генерация новых облаков
            next_cloud_spawn -= PLAYER_MOVE_SPEED
            if next_cloud_spawn <= 0:
                cloud_width = random.choice(CLOUD_WIDTHS)
                cloud_height = random.choice(CLOUD_HEIGHTS)
                cloud_x = WIDTH + random.randint(0, 300)
                cloud_y = random.randint(0, HEIGHT // 2)  # Облака появляются в верхней половине экрана
                cloud = Cloud(cloud_x, cloud_y, cloud_width, cloud_height)
                clouds.add(cloud)
                next_cloud_spawn = spawn_cloud_interval

        # Удаление деревьев, гор и облаков, которые вышли за пределы экрана
        for tree in trees:
            if tree.rect.right < 0:
                tree.kill()

        for mountain in mountains:
            if mountain.rect.right < 0:
                mountain.kill()

        for cloud in clouds:
            if cloud.rect.right < 0:
                cloud.kill()

        # Обновление и отрисовка
        player.update()
        draw_background(trees, mountains, clouds)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()

# Подробное объяснение кода

'''
import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

pygame.init() — функция для инициализации всех модулей Pygame.

# Константы экрана
WIDTH, HEIGHT = 800, 600
FPS = 60

WIDTH, HEIGHT — размеры экрана игры. FPS — частота обновления кадров в секунду (frames per second).

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
MOUNTAIN_COLOR = (139, 137, 137)  # Цвет гор (темно-серый)
TREE_BROWN = (139, 69, 19)  # Цвет ствола дерева (коричневый)
TREE_GREEN = (34, 139, 34)  # Цвет листвы дерева (темно-зеленый)
CLOUD_COLOR = WHITE  # Цвет облаков

Определение цветов для использования в игре в формате RGB.

# Параметры игрока
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 35
PLAYER_COLOR = BLACK
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = 15
PLAYER_MOVE_SPEED = 5

PLAYER_WIDTH, PLAYER_HEIGHT — размеры игрока. PLAYER_COLOR — цвет игрока. PLAYER_GRAVITY — сила гравитации.
PLAYER_JUMP_STRENGTH — сила прыжка. PLAYER_MOVE_SPEED — скорость перемещения игрока.

# Параметры земли
GROUND_HEIGHT = 20
GROUND_COLOR = GREEN

GROUND_HEIGHT — высота земли. GROUND_COLOR — цвет земли.

# Параметры фона
MOUNTAIN_SCROLL_SPEED = 1.5  # Скорость движения гор
TREE_SCROLL_SPEED = 3.0  # Скорость движения деревьев
CLOUD_SCROLL_SPEED = 1.0  # Скорость движения облаков
TREE_WIDTHS = [15, 20, 25, 30, 35]
TREE_HEIGHTS = [50, 60, 70, 80, 90]
MOUNTAIN_WIDTHS = [100, 120, 140, 160, 180]
MOUNTAIN_HEIGHTS = [100, 120, 140, 160, 180]
CLOUD_WIDTHS = [80, 100, 120]  # Увеличены размеры облаков
CLOUD_HEIGHTS = [40, 60, 80]  # Увеличены размеры облаков

Параметры для генерации фонов (деревьев, гор и облаков): скорости скроллинга и размеры.

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

pygame.display.set_mode((WIDTH, HEIGHT)) — установка размеров экрана. pygame.display.set_caption("Платформер")
 — установка заголовка окна. pygame.time.Clock() — создание объекта для управления частотой обновления кадров.

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

Player — класс для игрока. __init__ — инициализация игрока. update — обновление позиции игрока с учетом гравитации. 
jump — функция для прыжка.

# Класс Ground (земля)
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, GROUND_HEIGHT))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - GROUND_HEIGHT

Ground — класс для земли. __init__ — инициализация земли.

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

Tree — класс для дерева. __init__ — инициализация дерева с кроной. update — обновление позиции дерева в зависимости
от скорости скроллинга.

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

Mountain — класс для гор. __init__ — инициализация гор. update — обновление позиции гор в зависимости от скорости
скроллинга.

# Класс Cloud (облако)
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(CLOUD_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

Cloud — класс для облаков. __init__ — инициализация облаков. update — обновление позиции облаков в зависимости от
cкорости скроллинга.

def draw_background(trees, mountains, clouds):
    screen.fill(SKY_BLUE)

    # Отрисовка гор
    for mountain in mountains:
        screen.blit(mountain.image, (mountain.rect.x, mountain.rect.y))

    # Отрисовка деревьев
    for tree in trees:
        screen.blit(tree.image, (tree.rect.x, tree.rect.y))
    
    # Отрисовка облаков
    for cloud in clouds:
        screen.blit(cloud.image, (cloud.rect.x, cloud.rect.y))

draw_background — функция для отрисовки фона: гор, деревьев и облаков.

def main():
    all_sprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    mountains = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

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
    spawn_cloud_interval = 400  # Интервал между облаками

    next_tree_spawn = spawn_tree_interval
    next_mountain_spawn = spawn_mountain_interval
    next_cloud_spawn = spawn_cloud_interval

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

            # Обновление всех деревьев, гор и облаков
            for tree in trees:
                tree.update(TREE_SCROLL_SPEED)
            for mountain in mountains:
                mountain.update(MOUNTAIN_SCROLL_SPEED)
            for cloud in clouds:
                cloud.update(CLOUD_SCROLL_SPEED)

            # Генерация новых деревьев
            next_tree_spawn -= PLAYER_MOVE_SPEED
            if next_tree_spawn <= 0:
                tree_width = random.choice(TREE_WIDTHS)
                tree_height = random.choice(TREE_HEIGHTS)
                tree_x = WIDTH + random.randint(0, 200)
                tree_y = HEIGHT - GROUND_HEIGHT
                tree = Tree(tree_x, tree_y, tree_width, tree_height)
                trees.add(tree)
                next_tree_spawn = spawn_tree_interval

            # Генерация новых гор
            next_mountain_spawn -= PLAYER_MOVE_SPEED
            if next_mountain_spawn <= 0:
                mountain_width = random.choice(MOUNTAIN_WIDTHS)
                mountain_height = random.choice(MOUNTAIN_HEIGHTS)
                mountain_x = WIDTH + random.randint(0, 400)
                mountain_y = HEIGHT - GROUND_HEIGHT
                mountain = Mountain(mountain_x, mountain_y, mountain_width, mountain_height)
                mountains.add(mountain)
                next_mountain_spawn = spawn_mountain_interval

            # Генерация новых облаков
            next_cloud_spawn -= PLAYER_MOVE_SPEED
            if next_cloud_spawn <= 0:
                cloud_width = random.choice(CLOUD_WIDTHS)
                cloud_height = random.choice(CLOUD_HEIGHTS)
                cloud_x = WIDTH + random.randint(0, 300)
                cloud_y = random.randint(0, HEIGHT // 2)  # Облака появляются в верхней половине экрана
                cloud = Cloud(cloud_x, cloud_y, cloud_width, cloud_height)
                clouds.add(cloud)
                next_cloud_spawn = spawn_cloud_interval

        # Удаление деревьев, гор и облаков, которые вышли за пределы экрана
        for tree in trees:
            if tree.rect.right < 0:
                tree.kill()

        for mountain in mountains:
            if mountain.rect.right < 0:
                mountain.kill()

        for cloud in clouds:
            if cloud.rect.right < 0:
                cloud.kill()

        # Обновление и отрисовка
        player.update()
        draw_background(trees, mountains, clouds)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

main — главная функция игры:

Создание групп спрайтов для всех объектов (игрок, деревья, горы, облака).
Создание и добавление игрока и земли в группы спрайтов.
Установка интервалов для генерации деревьев, гор и облаков.
В бесконечном цикле:
Обработка событий (выход из игры и прыжок игрока).
Обработка нажатий клавиш (движение фона).
Обновление позиций деревьев, гор и облаков.
Генерация новых деревьев, гор и облаков.
Удаление объектов, вышедших за пределы экрана.
Обновление и отрисовка всех объектов на экране.
Обновление экрана с частотой FPS.
if __name__ == "__main__": — проверка, что скрипт запускается напрямую, а не импортируется как модуль, и вызов основной функции игры.

Этот код создает простую 2D-платформенную игру с движущимися фонами, такими как деревья, горы и облака, а также игроком, который может прыгать и двигаться по экрану.

'''

# Вот подробное объяснение кода функции main:

def main():
    all_sprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    mountains = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

'''
pygame.sprite.Group() — создание групп спрайтов для хранения и управления разными типами объектов.

all_sprites — общая группа для всех спрайтов, чтобы их можно было отрисовывать одновременно.
trees — группа для деревьев.
mountains — группа для гор.
clouds — группа для облаков.

    # Создание игрока
    player = Player()
    all_sprites.add(player)
    
    # Создание земли
    ground = Ground()
    all_sprites.add(ground)

Создание игрока и земли:

Создаем объект игрока с помощью класса Player и добавляем его в общую группу all_sprites.
Создаем объект земли с помощью класса Ground и также добавляем его в all_sprites.

    # Генерация фонов
    scroll_x = 0
    spawn_tree_interval = 300  # Интервал между деревьями
    spawn_mountain_interval = 600  # Интервал между горами
    spawn_cloud_interval = 400  # Интервал между облаками

    next_tree_spawn = spawn_tree_interval
    next_mountain_spawn = spawn_mountain_interval
    next_cloud_spawn = spawn_cloud_interval

Переменные для генерации объектов:

scroll_x — начальное значение для перемещения фона (пока не используется, можно удалить или использовать
 для других целей).
spawn_tree_interval, spawn_mountain_interval, spawn_cloud_interval — интервалы для появления новых деревьев,
 гор и облаков соответственно.
next_tree_spawn, next_mountain_spawn, next_cloud_spawn — таймеры, отсчитывающие время до появления следующих 
деревьев, гор и облаков.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

Основной игровой цикл:

Используем pygame.event.get() для получения всех событий, произошедших в текущем кадре.
Если событие — выход из игры (pygame.QUIT), то завершаем работу Pygame и выходим из программы.
Если нажата клавиша пробела (pygame.K_SPACE), вызываем метод jump у игрока, чтобы он прыгнул.

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:  # Фон движется только при нажатии клавиши вправо
            scroll_x += PLAYER_MOVE_SPEED

Обработка нажатий клавиш:

Проверяем, удерживается ли клавиша вправо (pygame.K_RIGHT). Если да, увеличиваем scroll_x на скорость перемещения 
игрока (PLAYER_MOVE_SPEED). (Этот блок можно удалить, если не используете перемещение фона по scroll_x).

            # Обновление всех деревьев, гор и облаков
            for tree in trees:
                tree.update(TREE_SCROLL_SPEED)
            for mountain in mountains:
                mountain.update(MOUNTAIN_SCROLL_SPEED)
            for cloud in clouds:
                cloud.update(CLOUD_SCROLL_SPEED)

Обновление фона:

Для каждого дерева в группе trees вызываем метод update с параметром TREE_SCROLL_SPEED.
Для каждой горы в группе mountains вызываем метод update с параметром MOUNTAIN_SCROLL_SPEED.
Для каждого облака в группе clouds вызываем метод update с параметром CLOUD_SCROLL_SPEED.

            # Генерация новых деревьев
            next_tree_spawn -= PLAYER_MOVE_SPEED
            if next_tree_spawn <= 0:
                tree_width = random.choice(TREE_WIDTHS)
                tree_height = random.choice(TREE_HEIGHTS)
                tree_x = WIDTH + random.randint(0, 200)
                tree_y = HEIGHT - GROUND_HEIGHT
                tree = Tree(tree_x, tree_y, tree_width, tree_height)
                trees.add(tree)
                next_tree_spawn = spawn_tree_interval

Генерация новых деревьев:

Уменьшаем таймер next_tree_spawn на скорость перемещения игрока (PLAYER_MOVE_SPEED).
Если таймер стал меньше или равен нулю, создаем новое дерево с случайным размером и позицией:
tree_width и tree_height — случайные размеры дерева.
tree_x — случайная позиция по горизонтали за пределами экрана.
tree_y — позиция по вертикали на уровне земли.
Создаем объект Tree и добавляем его в группу trees.
Сбрасываем таймер next_tree_spawn на исходное значение.

            # Генерация новых гор
            next_mountain_spawn -= PLAYER_MOVE_SPEED
            if next_mountain_spawn <= 0:
                mountain_width = random.choice(MOUNTAIN_WIDTHS)
                mountain_height = random.choice(MOUNTAIN_HEIGHTS)
                mountain_x = WIDTH + random.randint(0, 400)
                mountain_y = HEIGHT - GROUND_HEIGHT
                mountain = Mountain(mountain_x, mountain_y, mountain_width, mountain_height)
                mountains.add(mountain)
                next_mountain_spawn = spawn_mountain_interval

Генерация новых гор:

Уменьшаем таймер next_mountain_spawn на скорость перемещения игрока (PLAYER_MOVE_SPEED).
Если таймер стал меньше или равен нулю, создаем новую гору с случайным размером и позицией:
mountain_width и mountain_height — случайные размеры горы.
mountain_x — случайная позиция по горизонтали за пределами экрана.
mountain_y — позиция по вертикали на уровне земли.
Создаем объект Mountain и добавляем его в группу mountains.
Сбрасываем таймер next_mountain_spawn на исходное значение.

            # Генерация новых облаков
            next_cloud_spawn -= PLAYER_MOVE_SPEED
            if next_cloud_spawn <= 0:
                cloud_width = random.choice(CLOUD_WIDTHS)
                cloud_height = random.choice(CLOUD_HEIGHTS)
                cloud_x = WIDTH + random.randint(0, 300)
                cloud_y = random.randint(0, HEIGHT // 2)  # Облака появляются в верхней половине экрана
                cloud = Cloud(cloud_x, cloud_y, cloud_width, cloud_height)
                clouds.add(cloud)
                next_cloud_spawn = spawn_cloud_interval

Генерация новых облаков:

Уменьшаем таймер next_cloud_spawn на скорость перемещения игрока (PLAYER_MOVE_SPEED).
Если таймер стал меньше или равен нулю, создаем новое облако с случайным размером и позицией:
cloud_width и cloud_height — случайные размеры облака.
cloud_x — случайная позиция по горизонтали за пределами экрана.
cloud_y — случайная позиция по вертикали в верхней половине экрана.
Создаем объект Cloud и добавляем его в группу clouds.
Сбрасываем таймер next_cloud_spawn на исходное значение.

        # Удаление деревьев, гор и облаков, которые вышли за пределы экрана
        for tree in trees:
            if tree.rect.right < 0:
                tree.kill()

        for mountain in mountains:
            if mountain.rect.right < 0:
                mountain.kill()

        for cloud in clouds:
            if cloud.rect.right < 0:
                cloud.kill()

Удаление объектов, вышедших за пределы экрана:

Для каждого дерева в группе trees, если правая граница дерева выходит за пределы экрана (то есть tree.rect.right < 0),
удаляем дерево из группы trees.
Аналогично для гор и облаков.

        # Обновление и отрисовка
        player.update()
        draw_background(trees, mountains, clouds)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

Обновление и отрисовка:

player.update() — обновляем состояние игрока (например, гравитацию и прыжок).
draw_background(trees, mountains, clouds) — отрисовываем фон (деревья, горы и облака) на экране.
all_sprites.draw(screen) — отрисовываем все спрайты из группы all_sprites на экране.
pygame.display.flip() — обновляем экран, чтобы отобразить все изменения.
clock.tick(FPS) — ограничиваем частоту кадров до FPS (в данном случае 60 кадров в секунду).

Этот цикл будет повторяться бесконечно, пока игрок не закроет окно игры, и будет обрабатывать все события, обновлять
состояние объектов, генерировать новые объекты, удалять устаревшие и отрисовывать все на экране.

'''
