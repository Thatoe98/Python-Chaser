import pygame

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for sound

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SNAKE_SIZE = 20
FPS = 10  # Increased FPS to make the game faster

# Game duration (in seconds)
GAME_DURATION = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chaser")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 25)

# Load assets
try:
    flash_image = pygame.image.load("flash.png")
    flash_image = pygame.transform.scale(flash_image, (SNAKE_SIZE * 3, SNAKE_SIZE * 3))
    snow_image = pygame.image.load("snow.jpg")
    snow_image = pygame.transform.scale(snow_image, (SNAKE_SIZE * 2, SNAKE_SIZE * 2))
except:
    print("Warning: Could not load power-up images")

# Load RSU logo
try:
    rsu_logo = pygame.image.load("rsu_logo.png")
    rsu_logo = pygame.transform.scale(rsu_logo, (SNAKE_SIZE * 7, SNAKE_SIZE * 10))
    logo_position = (WIDTH - SNAKE_SIZE * 10 - 10, 10)
    has_logo = True
except:
    print("Warning: Could not load logo file 'rsu_logo.png'")
    has_logo = False

# Load and set up background music
try:
    pygame.mixer.music.load("game_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    music_playing = True
except:
    print("Warning: Could not load background music file 'game_music.mp3'")
    music_playing = False

# Load sound effects
try:
    food_sound = pygame.mixer.Sound("pop.mp3")
    food_sound.set_volume(0.7)
    has_food_sound = True
except:
    print("Warning: Could not load sound effect file 'pop.mp3'")
    has_food_sound = False
