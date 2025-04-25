import pygame
import sys
from settings import *
from ui_elements import toggle_music
from game_screens import show_intro_screen, start_page, display_end_screen
from game_mechanics import game_loop

def main():
    """Main function with game loop that can restart"""
    running = True
    
    # Show intro screen first
    show_intro_screen()
    
    while running:
        # Get game settings from start page
        game_duration, game_mode = start_page()
        
        # Run the game and get scores
        snake1_score, snake2_score, is_bot_game = game_loop(game_mode, game_duration)
        
        # Show end screen and check if we should return to menu
        continue_playing = display_end_screen(snake1_score, snake2_score, is_bot_game)
        
        if not continue_playing:
            running = False

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
