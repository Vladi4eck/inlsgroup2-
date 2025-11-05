import pygame
import sys
import random

#Чтобы запустить игру, убедитесь, что у вас установлен Pygame. Если нет, установите его с помощью команды:
# pip install pygame и затем запустите в терминале этот скрипт. python game.py

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - Игрок vs AI")
clock = pygame.time.Clock()

# Класс для ракетки
class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = 7
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

# Класс для мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])
        self.color = WHITE
    
    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Отскок от верхней и нижней стенки
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
    
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

# Создание объектов
player_paddle = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE)
ai_paddle = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, RED)
ball = Ball()

# Счет
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 74)

# AI логика
def ai_movement():
    # AI следует за мячом
    if ai_paddle.rect.centery < ball.rect.centery:
        ai_paddle.move_down()
    elif ai_paddle.rect.centery > ball.rect.centery:
        ai_paddle.move_up()

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_paddle.move_up()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_paddle.move_down()
    
    # Движение AI
    ai_movement()
    
    # Движение мяча
    ball.move()
    
    # Проверка столкновения с ракетками
    if ball.rect.colliderect(player_paddle.rect):
        ball.speed_x = abs(ball.speed_x)  # Отскок вправо
        ball.speed_y += random.randint(-2, 2)  # Случайное изменение угла
    
    if ball.rect.colliderect(ai_paddle.rect):
        ball.speed_x = -abs(ball.speed_x)  # Отскок влево
        ball.speed_y += random.randint(-2, 2)
    
    # Проверка гола
    if ball.rect.left <= 0:
        ai_score += 1
        ball.reset()
    
    if ball.rect.right >= WIDTH:
        player_score += 1
        ball.reset()
    
    # Отрисовка
    screen.fill(BLACK)
    
    # Рисуем среднюю линию
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
    
    # Рисуем объекты
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()
    
    # Отображение счета
    player_text = font.render(str(player_score), True, BLUE)
    ai_text = font.render(str(ai_score), True, RED)
    screen.blit(player_text, (WIDTH // 4, 30))
    screen.blit(ai_text, (WIDTH * 3 // 4 - 40, 30))
    
    # Проверка победы
    if player_score >= 10:
        win_text = font.render("YOU WIN!", True, BLUE)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
    
    if ai_score >= 10:
        lose_text = font.render("AI WINS!", True, RED)
        screen.blit(lose_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
    
    pygame.display.flip()

pygame.quit()
sys.exit()
