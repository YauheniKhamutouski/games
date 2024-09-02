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
