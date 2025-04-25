import pygame
import random
import time
import sys
from settings import *
from ui_elements import draw_snake, display_message, toggle_music
from pathfinding import find_path_to_food
from game_screens import show_preparation_screen

def game_loop(game_mode, game_duration):
    """Main game loop separated as a function to allow restarting"""
    is_bot_game = (game_mode == "PVE")

    # Show preparation screen
    show_preparation_screen(is_bot_game)

    # Player 1 (Red Snake)
    snake1_pos = [100, 50]
    snake1_body = [[100, 50], [80, 50]]  # Start with 2 blocks
    snake1_direction = 'RIGHT'
    snake1_change = [SNAKE_SIZE, 0]
    snake1_score = 0
    snake1_fps = FPS  # Individual FPS for Player 1
    snake1_speed_boost = 1.0  # Speed multiplier for snake 1
    snake1_last_move_time = 0  # Last time snake 1 moved
    snake1_frozen = False
    snake1_frozen_start_time = None

    # Player 2 (Blue Snake) / Bot
    snake2_pos = [700, 550]
    snake2_body = [[700, 550], [720, 550]]  # Start with 2 blocks
    snake2_direction = 'LEFT'
    snake2_change = [-SNAKE_SIZE, 0]
    snake2_score = 0
    snake2_fps = FPS  # Individual FPS for Player 2
    snake2_speed_boost = 1.0  # Speed multiplier for snake 2
    snake2_last_move_time = 0  # Last time snake 2 moved
    snake2_frozen = False
    snake2_frozen_start_time = None
    bot_decision_time = 0  # Time tracker for bot decisions
    bot_decision_interval = 0.1  # How often the bot makes decisions (in seconds)

    # Food
    food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
    food_spawn = True

    # Power-up variables
    flash_powerup_pos = None
    flash_powerup_active = False
    powerup_effect_start_time_1 = None
    powerup_effect_start_time_2 = None
    powerup_effect_active_1 = False
    powerup_effect_active_2 = False

    # Freeze power-up variables
    snow_powerup_pos = None
    snow_powerup_active = False
    snow_last_spawn_time = None

    # Game variables
    start_time = time.time()
    running = True

    while running:
        current_time = time.time()
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Music toggle
                if event.key == pygame.K_m:
                    toggle_music()
                
                # Player 1 controls (WASD)
                if event.key == pygame.K_w and snake1_direction != 'DOWN':
                    snake1_direction = 'UP'
                    snake1_change = [0, -SNAKE_SIZE]
                elif event.key == pygame.K_s and snake1_direction != 'UP':
                    snake1_direction = 'DOWN'
                    snake1_change = [0, SNAKE_SIZE]
                elif event.key == pygame.K_a and snake1_direction != 'RIGHT':
                    snake1_direction = 'LEFT'
                    snake1_change = [-SNAKE_SIZE, 0]
                elif event.key == pygame.K_d and snake1_direction != 'LEFT':
                    snake1_direction = 'RIGHT'
                    snake1_change = [SNAKE_SIZE, 0]

                # Player 2 controls (Arrow keys) - Only if not a bot game
                if not is_bot_game:
                    if event.key == pygame.K_UP and snake2_direction != 'DOWN':
                        snake2_direction = 'UP'
                        snake2_change = [0, -SNAKE_SIZE]
                    elif event.key == pygame.K_DOWN and snake2_direction != 'UP':
                        snake2_direction = 'DOWN'
                        snake2_change = [0, SNAKE_SIZE]
                    elif event.key == pygame.K_LEFT and snake2_direction != 'RIGHT':
                        snake2_direction = 'LEFT'
                        snake2_change = [-SNAKE_SIZE, 0]
                    elif event.key == pygame.K_RIGHT and snake2_direction != 'LEFT':
                        snake2_direction = 'RIGHT'
                        snake2_change = [SNAKE_SIZE, 0]

        # Bot decision making (if in PVE mode)
        if is_bot_game and not snake2_frozen and current_time - bot_decision_time > bot_decision_interval:
            # Collect obstacles (both snake bodies minus the tail that will move)
            obstacles = snake1_body[:-1] + snake2_body[:-1]
            
            # Find path to food
            bot_change = find_path_to_food(snake2_pos, food_pos, obstacles, WIDTH // SNAKE_SIZE, HEIGHT // SNAKE_SIZE)
            
            # Update direction based on the next move
            if bot_change == (0, -SNAKE_SIZE) and snake2_direction != 'DOWN':
                snake2_direction = 'UP'
                snake2_change = [0, -SNAKE_SIZE]
            elif bot_change == (0, SNAKE_SIZE) and snake2_direction != 'UP':
                snake2_direction = 'DOWN'
                snake2_change = [0, SNAKE_SIZE]
            elif bot_change == (-SNAKE_SIZE, 0) and snake2_direction != 'RIGHT':
                snake2_direction = 'LEFT'
                snake2_change = [-SNAKE_SIZE, 0]
            elif bot_change == (SNAKE_SIZE, 0) and snake2_direction != 'LEFT':
                snake2_direction = 'RIGHT'
                snake2_change = [SNAKE_SIZE, 0]
                
            bot_decision_time = current_time

        # Rest of the game logic...
        # Check if either snake is frozen and update frozen status
        if snake1_frozen and current_time - snake1_frozen_start_time > 3:
            snake1_frozen = False
            
        if snake2_frozen and current_time - snake2_frozen_start_time > 3:
            snake2_frozen = False

        # Move snakes based on their individual timing, if not frozen
        if not snake1_frozen and current_time - snake1_last_move_time > (1.0 / (FPS * snake1_speed_boost)):
            # Update snake 1 position
            snake1_pos[0] += snake1_change[0]
            snake1_pos[1] += snake1_change[1]
            
            # Wrap around screen edges
            snake1_pos[0] %= WIDTH
            snake1_pos[1] %= HEIGHT
            
            # Update snake1 body
            snake1_body.append(list(snake1_pos))
            
            # Check if Player 1 eats the food
            if abs(snake1_pos[0] - food_pos[0]) < SNAKE_SIZE and abs(snake1_pos[1] - food_pos[1]) < SNAKE_SIZE:
                snake1_score += 1
                food_spawn = False
                # Play sound effect when food is eaten
                if has_food_sound:
                    food_sound.play()
            else:
                snake1_body.pop(0)
                
            snake1_last_move_time = current_time
        
        if not snake2_frozen and current_time - snake2_last_move_time > (1.0 / (FPS * snake2_speed_boost)):
            # Update snake 2 position
            snake2_pos[0] += snake2_change[0]
            snake2_pos[1] += snake2_change[1]
            
            # Wrap around screen edges
            snake2_pos[0] %= WIDTH
            snake2_pos[1] %= HEIGHT
            
            # Update snake2 body
            snake2_body.append(list(snake2_pos))
            
            # Check if Player 2 eats the food
            if abs(snake2_pos[0] - food_pos[0]) < SNAKE_SIZE and abs(snake2_pos[1] - food_pos[1]) < SNAKE_SIZE:
                snake2_score += 1
                food_spawn = False
                # Play sound effect when food is eaten
                if has_food_sound:
                    food_sound.play()
            else:
                snake2_body.pop(0)
                
            snake2_last_move_time = current_time

        # Respawn food
        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                        random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
            food_spawn = True

        # Power-up logic
        elapsed_time = current_time - start_time

        # Spawn speed power-up after 10 seconds and every 5 seconds after it disappears
        if elapsed_time > 10 and not flash_powerup_active and not (powerup_effect_active_1 or powerup_effect_active_2):
            flash_powerup_pos = [random.randrange(1, (WIDTH // (SNAKE_SIZE * 3))) * SNAKE_SIZE * 3,
                           random.randrange(1, (HEIGHT // (SNAKE_SIZE * 3))) * SNAKE_SIZE * 3]
            flash_powerup_active = True

        # Spawn freeze power-up after 15 seconds and every 10 seconds after it disappears
        if elapsed_time > 15 and not snow_powerup_active and (snow_last_spawn_time is None or current_time - snow_last_spawn_time > 10):
            snow_powerup_pos = [random.randrange(1, (WIDTH // (SNAKE_SIZE * 3))) * SNAKE_SIZE * 3,
                         random.randrange(1, (HEIGHT // (SNAKE_SIZE * 3))) * SNAKE_SIZE * 3]
            snow_powerup_active = True
            
        # Check if a snake touches the speed power-up
        if flash_powerup_active:
            if (flash_powerup_pos[0] <= snake1_pos[0] < flash_powerup_pos[0] + SNAKE_SIZE * 3 and
                flash_powerup_pos[1] <= snake1_pos[1] < flash_powerup_pos[1] + SNAKE_SIZE * 3):
                flash_powerup_active = False
                powerup_effect_active_1 = True
                powerup_effect_start_time_1 = current_time
                snake1_speed_boost = 1.3  # Increase Player 1's speed by 30%
            elif (flash_powerup_pos[0] <= snake2_pos[0] < flash_powerup_pos[0] + SNAKE_SIZE * 3 and
                  flash_powerup_pos[1] <= snake2_pos[1] < flash_powerup_pos[1] + SNAKE_SIZE * 3):
                flash_powerup_active = False
                powerup_effect_active_2 = True
                powerup_effect_start_time_2 = current_time
                snake2_speed_boost = 1.3  # Increase Player 2's speed by 30%

        # Check if a snake touches the freeze power-up
        if snow_powerup_active:
            if (snow_powerup_pos[0] <= snake1_pos[0] < snow_powerup_pos[0] + SNAKE_SIZE * 3 and
                snow_powerup_pos[1] <= snake1_pos[1] < snow_powerup_pos[1] + SNAKE_SIZE * 3):
                snow_powerup_active = False
                snow_last_spawn_time = current_time
                snake2_frozen = True  # Freeze opponent (Player 2)
                snake2_frozen_start_time = current_time
            elif (snow_powerup_pos[0] <= snake2_pos[0] < snow_powerup_pos[0] + SNAKE_SIZE * 3 and
                  snow_powerup_pos[1] <= snake2_pos[1] < snow_powerup_pos[1] + SNAKE_SIZE * 3):
                snow_powerup_active = False
                snow_last_spawn_time = current_time
                snake1_frozen = True  # Freeze opponent (Player 1)
                snake1_frozen_start_time = current_time

        # End power-up effects
        # End power-up effect after 5 seconds for Player 1
        if powerup_effect_active_1 and current_time - powerup_effect_start_time_1 > 5:
            powerup_effect_active_1 = False
            snake1_speed_boost = 1.0  # Reset Player 1's speed to normal

        # End power-up effect after 5 seconds for Player 2
        if powerup_effect_active_2 and current_time - powerup_effect_start_time_2 > 5:
            powerup_effect_active_2 = False
            snake2_speed_boost = 1.0  # Reset Player 2's speed to normal

        # Draw power-ups
        if flash_powerup_active:
            screen.blit(flash_image, (flash_powerup_pos[0], flash_powerup_pos[1]))
            
        if snow_powerup_active:
            screen.blit(snow_image, (snow_powerup_pos[0], snow_powerup_pos[1]))

        # Draw food
        pygame.draw.rect(screen, GREEN, [food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE])

        # Draw snakes with original rectangle-based heads
        draw_snake(snake1_body, RED)
        draw_snake(snake2_body, BLUE if not is_bot_game else YELLOW)  # Make bot yellow to distinguish

        # Display scores and status effects
        player1_name = "Player 1"
        player2_name = "Player 2" if not is_bot_game else "Bot"
        
        display_message(f"{player1_name}: {snake1_score}", WHITE, 10, 10)
        if snake1_frozen:
            display_message("FROZEN!", WHITE, 10, 70)
        display_message(f"{player2_name}: {snake2_score}", WHITE, 10, 40)
        if snake2_frozen:
            display_message("FROZEN!", WHITE, 10, 100)

        # Display timer
        remaining_time = max(0, game_duration - int(elapsed_time))
        display_message(f"Time Left: {remaining_time}s", WHITE, WIDTH - 200, 10)

        # Check game duration
        if current_time - start_time >= game_duration:
            running = False

        pygame.display.update()
        
        # Fixed frame rate for rendering only
        clock.tick(60)

    # Return final scores
    return snake1_score, snake2_score, is_bot_game
