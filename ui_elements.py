import pygame
from settings import *

def draw_logo():
    """Draw the RSU logo in the top right corner if available"""
    if has_logo:
        screen.blit(rsu_logo, logo_position)

def draw_snake(snake_list, color, direction=None):
    for i, block in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Head of the snake
            pygame.draw.rect(screen, WHITE, [block[0], block[1], SNAKE_SIZE, SNAKE_SIZE])  # White head
        else:
            pygame.draw.rect(screen, color, [block[0], block[1], SNAKE_SIZE, SNAKE_SIZE])

def display_message(msg, color, x, y):
    text = font.render(msg, True, color)
    screen.blit(text, [x, y])

def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
        music_playing = False
    else:
        pygame.mixer.music.unpause()
        music_playing = True
    return music_playing
