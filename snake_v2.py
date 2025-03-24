import pygame
import random

# Initialisation de pygame
pygame.init()

# Paramètres de l'écran (1280x720)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Variables du jeu
snake_size = 50
snake_pos = [100, 50]
snake_body = [[100, 50], [50, 50], [0, 50]]
direction = 'RIGHT'
change_to = direction
food_pos = [random.randrange(1, (1280 // snake_size)) * snake_size,
            random.randrange(1, (720 // snake_size)) * snake_size]
food_spawn = True

score = 0

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (204, 0, 102)
GREEN = (102, 204, 0)
BLACK_GREEN = (0, 102, 0)


# Fonction pour dessiner le serpent
def draw_snake(snake_size, snake_body):
    for i, segment in enumerate(snake_body):
        if i == 0:
            pygame.draw.rect(screen, BLACK_GREEN, pygame.Rect(
                segment[0], segment[1], snake_size, snake_size))
        else:
            pygame.draw.rect(screen, GREEN, pygame.Rect(
                segment[0], segment[1], snake_size, snake_size))


# Fonction pour afficher le score
def show_score(score):
    font = pygame.font.SysFont('arial', 20)
    value = font.render("Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])


# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Vérifier si la direction est valide (le serpent ne peut pas se déplacer dans la direction opposée à son corps)
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Déplacer le serpent
    if direction == 'UP':
        snake_pos[1] -= snake_size
    if direction == 'DOWN':
        snake_pos[1] += snake_size
    if direction == 'LEFT':
        snake_pos[0] -= snake_size
    if direction == 'RIGHT':
        snake_pos[0] += snake_size

    # Ajouter le nouveau segment de tête à la position actuelle
    snake_body.insert(0, list(snake_pos))

    # Vérifier si le serpent mange de la nourriture
    snake_head_rect = pygame.Rect(
        snake_pos[0], snake_pos[1], snake_size, snake_size)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size)

    # Collision avec la nourriture
    if snake_head_rect.colliderect(food_rect):
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Re-générer la nourriture
    if not food_spawn:
        food_pos = [random.randrange(1, (1280 // snake_size)) * snake_size,
                    random.randrange(1, (720 // snake_size)) * snake_size]
    food_spawn = True

    # Remplir l'écran en noir
    screen.fill(BLACK)

    # Dessiner le serpent et la nourriture
    draw_snake(snake_size, snake_body)
    pygame.draw.rect(screen, RED, pygame.Rect(
        food_pos[0], food_pos[1], snake_size, snake_size))

    # Afficher le score
    show_score(score)

    # Vérifier si le serpent se touche lui-même ou touche les bords
    if snake_pos[0] < 0 or snake_pos[0] >= 1280 or snake_pos[1] < 0 or snake_pos[1] >= 720:
        running = False
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            running = False

    # Actualiser l'écran
    pygame.display.flip()

    # Cadence du jeu (FPS)
    clock.tick(6)

# Fin du jeu
pygame.quit()
