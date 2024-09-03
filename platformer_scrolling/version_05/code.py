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
ENEMY_PURPLE = (128, 0, 128)  # Фиолетовый цвет для врагов

# Параметры игрока
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 35
PLAYER_COLOR = BLACK
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = 15
PLAYER_MOVE_SPEED = 5

# Параметры врага
ENEMY_SIZE = 15  # Размер врага 15x15 пикселей
ENEMY_SPEED = 6  # Скорость движения врага

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

# Класс Enemy (враг)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Создаем квадрат 15x15 пикселей для врага
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(ENEMY_PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - ENEMY_SIZE

    def update(self):
        self.rect.x -= ENEMY_SPEED
        if self.rect.right < 0:
            self.kill()  # Удаляем врага, если он вышел за экран

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
    enemies = pygame.sprite.Group()  # Группа врагов
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
    spawn_enemy_interval = 400  # Уменьшен интервал между врагами для более частого появления

    next_tree_spawn = spawn_tree_interval
    next_mountain_spawn = spawn_mountain_interval
    next_cloud_spawn = spawn_cloud_interval
    next_enemy_spawn = spawn_enemy_interval

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

            # Генерация новых врагов
            next_enemy_spawn -= PLAYER_MOVE_SPEED
            if next_enemy_spawn <= 0:
                enemy_x = WIDTH + random.randint(0, 200)
                enemy_y = HEIGHT - GROUND_HEIGHT

                # Случайное создание одного или двух врагов
                for _ in range(random.choice([1, 2])):
                    enemy = Enemy(enemy_x, enemy_y)
                    enemies.add(enemy)
                    enemy_x += ENEMY_SIZE + random.randint(0, 20)  # Отступ для второго врага, если генерируются два

                next_enemy_spawn = spawn_enemy_interval

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

        # Обновление врагов
        for enemy in enemies:
            enemy.update()

        # Проверка столкновений
        if pygame.sprite.spritecollideany(player, enemies):
            print("Игра окончена!")
            pygame.quit()
            sys.exit()

        # Обновление и отрисовка
        player.update()
        draw_background(trees, mountains, clouds)
        all_sprites.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
