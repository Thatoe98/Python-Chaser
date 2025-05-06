import pygame
from settings import *

def draw_logo():
    """Draw the RSU logo in the top right corner if available"""
    if has_logo:
        screen.blit(rsu_logo, logo_position)

def draw_snake(snake_list, color, direction=None):
    for i, block in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Head of the snake
            # Draw the white head
            pygame.draw.rect(screen, WHITE, [block[0], block[1], SNAKE_SIZE, SNAKE_SIZE])
            
            # Add eyes to the snake head
            eye_radius = SNAKE_SIZE // 5
            eye_offset = SNAKE_SIZE // 4
            
            # Default eye positions (for RIGHT direction)
            left_eye_pos = (block[0] + SNAKE_SIZE - eye_offset, block[1] + eye_offset)
            right_eye_pos = (block[0] + SNAKE_SIZE - eye_offset, block[1] + SNAKE_SIZE - eye_offset)
            
            # Adjust eye positions based on the last segment to determine direction
            if len(snake_list) > 1:
                prev_block = snake_list[-2]
                # Moving right
                if block[0] > prev_block[0]:
                    left_eye_pos = (block[0] + SNAKE_SIZE - eye_offset, block[1] + eye_offset)
                    right_eye_pos = (block[0] + SNAKE_SIZE - eye_offset, block[1] + SNAKE_SIZE - eye_offset)
                # Moving left
                elif block[0] < prev_block[0]:
                    left_eye_pos = (block[0] + eye_offset, block[1] + eye_offset)
                    right_eye_pos = (block[0] + eye_offset, block[1] + SNAKE_SIZE - eye_offset)
                # Moving down
                elif block[1] > prev_block[1]:
                    left_eye_pos = (block[0] + eye_offset, block[1] + SNAKE_SIZE - eye_offset)
                    right_eye_pos = (block[0] + SNAKE_SIZE - eye_offset, block[1] + SNAKE_SIZE - eye_offset)
                # Moving up
                elif block[1] < prev_block[1]:
                    left_eye_pos = (block[0] + eye_offset, block[1] + eye_offset)
                    right_eye_pos = (block[0] + SNAKE_SIZE - eye_offset, block[1] + eye_offset)
            
            # Draw the eyes
            pygame.draw.circle(screen, BLACK, left_eye_pos, eye_radius)
            pygame.draw.circle(screen, BLACK, right_eye_pos, eye_radius)
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
