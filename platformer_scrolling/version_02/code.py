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
