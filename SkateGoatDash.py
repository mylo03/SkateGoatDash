import pygame
import random
import os
import math
import time

# Initialize Pygame
pygame.init()
#sound = pygame.mixer.Sound("Y2Mate.is - Flight  Music - Soaring in the Stars-ySER3OT5etg-160k-1654320811487.wav")

# Set the screen size
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the background color
background_color = (135, 206, 235)
bird_scale_factor = 0.1

# Load the bird image
bird_image = pygame.image.load(os.path.join('goatinplane.png'))
bird_image = pygame.transform.scale(bird_image, (int(bird_image.get_width() * bird_scale_factor), int(bird_image.get_height() * bird_scale_factor)))

carrot = pygame.image.load(os.path.join('carrot.png'))
carrot = pygame.transform.scale(carrot, (int(carrot.get_width() * 0.35), int(carrot.get_height() * 0.35)))
carrot = pygame.transform.rotate(carrot, 90)

grass_image = pygame.image.load(os.path.join('grass.png'))
grass_scale_factor = 1.5
grass_image = pygame.transform.scale(grass_image, (int(grass_image.get_width() * grass_scale_factor), int(grass_image.get_height() * grass_scale_factor)))
grass_x = 0
grass_y = 0
grass_speed = 5

grass_image_rect = grass_image.get_rect()

cloud = pygame.image.load(os.path.join('cloud.png'))
cloud_scale_factor = 1.2
cloud = pygame.transform.scale(cloud, (int(cloud.get_width() * cloud_scale_factor), int(cloud.get_height() * cloud_scale_factor)))
cloud_rect = cloud.get_rect()

# Load the pipe image
pipe_image = pygame.image.load(os.path.join('pipe.png'))
pipe_scale_factor = 0.4
pipe_image = pygame.transform.scale(pipe_image, (int(pipe_image.get_width() * pipe_scale_factor), int(pipe_image.get_height() * pipe_scale_factor)))

start_screen = pygame.image.load(os.path.join('start.tiff'))
gameover = pygame.image.load(os.path.join('Game-Over.png'))


# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.4

    def update(self):
        self.velocity += self.gravity
        if self.y > 350:
            self.y=350
        self.y += self.velocity

    def flap(self):
        self.velocity = -6

    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))


# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.y_gap = random.randint(180, 200)
        self.width = 50
        self.top_height = random.randint(100, screen_height - self.y_gap - 100)
        self.bottom_height = screen_height - self.top_height - self.y_gap
        self.scored = False

    def update(self):
        self.x -= 5

    def off_screen(self):
        return self.x < -self.width

    def collision(self, bird):
        if bird.x + bird_image.get_width() > self.x and bird.x < self.x + self.width:
            if bird.y < self.top_height or bird.y + bird_image.get_height() > self.top_height + self.y_gap:
                return True
        return False

    def draw(self, screen):
        screen.blit(pipe_image, (self.x, self.top_height - pipe_image.get_height()))
        screen.blit(pygame.transform.rotate(pipe_image, 180), (self.x, self.top_height + self.y_gap))


# Create the Bird and Pipe objects
bird = Bird(100, screen_height // 2)


# Set the game clock
clock = pygame.time.Clock()

running = True

max_pipes = 3
pipes = [Pipe(screen_width)]

last_pipe_x = screen_width

# Set the timer
pygame.time.set_timer(pygame.USEREVENT, 2500)  # trigger an event every 3 seconds

# Set the colors
#colors = [(135, 206, 235)]

sky_blue = (135, 206, 235)
dark_blue = (0, 119, 190)
num_colors = 100
colors = []

# Create gradient from sky blue to dark blue
for i in range(num_colors):
    r = int(sky_blue[0] + i * (dark_blue[0] - sky_blue[0]) / num_colors)
    g = int(sky_blue[1] + i * (dark_blue[1] - sky_blue[1]) / num_colors)
    b = int(sky_blue[2] + i * (dark_blue[2] - sky_blue[2]) / num_colors)
    colors.append((r, g, b))

# Create gradient from dark blue back to sky blue
for i in range(num_colors):
    r = int(dark_blue[0] + i * (sky_blue[0] - dark_blue[0]) / num_colors)
    g = int(dark_blue[1] + i * (sky_blue[1] - dark_blue[1]) / num_colors)
    b = int(dark_blue[2] + i * (sky_blue[2] - dark_blue[2]) / num_colors)
    colors.append((r, g, b))

# Ensure that the list ends with the original sky blue color
colors[-1] = sky_blue
color_index = 0
color_time = pygame.time.get_ticks()
score = 0
scroll = 0


def start_game():
    screen.blit(start_screen, (0, 0))
    # Update the display
    pygame.display.flip()

    # Wait for the player to press a key to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

        if event.type == pygame.QUIT:
            pygame.quit()

def game_over():
    #sound.stop()
    screen.blit(gameover, (100,80))
    pygame.display.update()
    time.sleep(2)


start_game()

tiles = math.ceil(screen_width/ cloud.get_width()) + 1

#sound.play()
#sound.set_volume(0.5)

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()
        if event.type == pygame.USEREVENT:
            # Add a new pipe
            pipes.append(Pipe(screen_width))
            last_pipe_x = pipes[-1].x

    # Update the Bird and Pipe objects
    bird.update()

    for pipe in pipes:
        pipe.update()
        if pipe.off_screen():
            pipes.remove(pipe)
        if not pipe.scored and bird.x > pipe.x + pipe.width:
            score += 1
            pipe.scored = True
        if pipe.collision(bird):
            running = False

    # Draw the gradient background
    if pygame.time.get_ticks() - color_time > 100:
        color_index += 1
        if color_index >= len(colors):
            color_index = 0
        background_color = colors[color_index]
        color_time = pygame.time.get_ticks()

    # scroll background
    scroll -= 3

    # Reset the scroll position
    if abs(scroll) > cloud.get_width():
        scroll = 0

    screen.fill(background_color)

    for i in range(0, tiles):
        screen.blit(cloud, (i * cloud.get_width() + scroll, 270))
        cloud_rect.x = i * cloud.get_width() + scroll

    bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    screen.blit(carrot, (300, 20))
    # Draw the score
    font = pygame.font.Font(None, 50)
    text = font.render(str(score), True, (0, 0, 0))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50))

    # Update the screen
    pygame.display.flip()

    # Set the game clock tick rate
    clock.tick(60)

    # Quit Pygame
game_over()
pygame.quit()