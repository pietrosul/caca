import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Urban Defender")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Print current working directory
print("Current workin directory:", os.getcwd())

# Load assets with error handling
try:
    # Get the directory where main.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute paths to assets
    player_path = os.path.join(current_dir, 'assets', 'player.png')
    enemy_path = os.path.join(current_dir, 'assets', 'enemy.png')
    bullet_path = os.path.join(current_dir, 'assets', 'bullet.png')
    
    print("\nDebug Info:")
    print(f"Script location: {current_dir}")
    print("\nTrying to load images from:")
    print(f"Player: {player_path}")
    print(f"Enemy: {enemy_path}")
    print(f"Bullet: {bullet_path}")
    
    # Check if files exist before loading
    for path in [player_path, enemy_path, bullet_path]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Cannot find file: {path}")
    
    # Load images
    player_img = pygame.image.load(player_path).convert_alpha()
    enemy_img = pygame.image.load(enemy_path).convert_alpha()
    bullet_img = pygame.image.load(bullet_path).convert_alpha()
    
    print("\nAll images loaded successfully!")

except Exception as e:
    print("\nError loading images:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nPlease ensure that:")
    print("1. The 'assets' folder exists in the same directory as main.py")
    print("2. All required image files (player.png, enemy.png, bullet.png) are in the assets folder")
    print("3. The image files have correct permissions")
    pygame.quit()
    exit(1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

def main():
    global all_sprites, bullets

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create initial enemies
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Game variables
    score = 0
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check for player-enemy collisions
        if pygame.sprite.spritecollide(player, enemies, False):
            running = False

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
