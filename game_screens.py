
import pygame
import time
import math
import sys
from settings import *
from ui_elements import draw_logo, draw_snake, display_message, toggle_music

def show_intro_screen():
    """Display attractive introduction screen"""
    screen.fill(BLACK)
    intro_running = True
    alpha = 0  # For fade in effect
    start_time = time.time()
    
    # Initialize animated snakes for intro
    intro_red_snake = {
        'body': [[100, 300], [80, 300], [60, 300], [40, 300], [20, 300]],
        'direction': [SNAKE_SIZE, 0],
        'pos': [100, 300]
    }
    
    intro_blue_snake = {
        'body': [[700, 300], [720, 300], [740, 300], [760, 300], [780, 300]],
        'direction': [-SNAKE_SIZE, 0],
        'pos': [700, 300]
    }
    
    animation_timer = 0
    animation_speed = 0.15
    last_update = time.time()

    # Load or create title font
    title_font = pygame.font.SysFont("arial", 100, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 40)
    
    while intro_running:
        current_time = time.time()
        delta_time = current_time - last_update
        animation_timer += delta_time
        
        screen.fill(BLACK)
        
        # Animate snakes
        if animation_timer >= animation_speed:
            # Update red snake position
            intro_red_snake['pos'][0] = (intro_red_snake['pos'][0] + intro_red_snake['direction'][0]) % WIDTH
            intro_red_snake['body'].append(list(intro_red_snake['pos']))
            intro_red_snake['body'].pop(0)
            
            # Update blue snake position
            intro_blue_snake['pos'][0] = (intro_blue_snake['pos'][0] + intro_blue_snake['direction'][0]) % WIDTH
            intro_blue_snake['body'].append(list(intro_blue_snake['pos']))
            intro_blue_snake['body'].pop(0)
            
            animation_timer = 0
        
        # Draw animated snakes
        draw_snake(intro_red_snake['body'], RED)
        draw_snake(intro_blue_snake['body'], BLUE)
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((20, 20, 30))
        screen.blit(overlay, (0, 0))
        
        # Draw title with glow effect
        title = "PYTHON CHASER"
        for offset in range(3, 0, -1):
            glow_surface = title_font.render(title, True, (50, 50, 100))
            screen.blit(glow_surface, (WIDTH//2 - glow_surface.get_width()//2 + offset, 
                                     HEIGHT//3 - offset))
        
        title_surface = title_font.render(title, True, WHITE)
        screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, HEIGHT//3))
        
        # Draw subtitle with fade in
        if alpha < 255:
            alpha += 2
        
        subtitle = "Press SPACE to Start"
        subtitle_surface = subtitle_font.render(subtitle, True, WHITE)
        subtitle_surface.set_alpha(int(abs(math.sin(current_time * 2)) * 255))  # Pulsing effect
        screen.blit(subtitle_surface, 
                   (WIDTH//2 - subtitle_surface.get_width()//2, HEIGHT * 2//3))
        
        # Draw logo if available
        draw_logo()
        
        # Display version and controls
        version_text = small_font.render("Version 1.0", True, GRAY)
        screen.blit(version_text, (10, HEIGHT - 30))
        
        controls_text = small_font.render("M - Toggle Music | Q - Quit", True, GRAY)
        screen.blit(controls_text, (WIDTH - controls_text.get_width() - 10, HEIGHT - 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro_running = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:
                    toggle_music()
        
        pygame.display.update()
        last_update = current_time
        clock.tick(60)

def start_page():
    """Enhanced start page with animated snakes"""
    selected_timer = 60
    game_mode = None
    running = True
    
    # Initialize animated menu snakes with more segments
    red_snake = {
        'body': [[100, 200], [80, 200], [60, 200], [40, 200], [20, 200]],
        'direction': [SNAKE_SIZE, 0],
        'pos': [100, 200]
    }
    
    blue_snake = {
        'body': [[700, 400], [720, 400], [740, 400], [760, 400], [780, 400]],
        'direction': [-SNAKE_SIZE, 0],
        'pos': [700, 400]
    }
    
    animation_timer = 0
    animation_speed = 0.15
    last_update = time.time()
    
    while running:
        current_update = time.time()
        delta_time = current_update - last_update
        animation_timer += delta_time
        
        # Create gradient background
        screen.fill(BLACK)
        
        # Animate snakes
        if animation_timer >= animation_speed:
            # Move and update snakes...
            red_snake['pos'][0] = (red_snake['pos'][0] + red_snake['direction'][0]) % WIDTH
            red_snake['pos'][1] = (red_snake['pos'][1] + red_snake['direction'][1]) % HEIGHT
            red_snake['body'].append(list(red_snake['pos']))
            red_snake['body'].pop(0)
            
            blue_snake['pos'][0] = (blue_snake['pos'][0] + blue_snake['direction'][0]) % WIDTH
            blue_snake['pos'][1] = (blue_snake['pos'][1] + blue_snake['direction'][1]) % HEIGHT
            blue_snake['body'].append(list(blue_snake['pos']))
            blue_snake['body'].pop(0)
            
            animation_timer = 0

        # Draw animated snakes
        draw_snake(red_snake['body'], RED)
        draw_snake(blue_snake['body'], BLUE)

        # Create stylish semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((20, 20, 30))  # Dark blue-ish background
        screen.blit(overlay, (0, 0))

        if not game_mode:
            # Draw title with shadow effect
            title = "Select Game Mode"
            title_font = pygame.font.SysFont(None, 60)
            shadow = title_font.render(title, True, (50, 50, 50))
            text = title_font.render(title, True, WHITE)
            screen.blit(shadow, (WIDTH//2 - shadow.get_width()//2 + 2, 80 + 2))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 80))

            # Create modern looking mode buttons
            mode_buttons = [
                ("1. PVE", "Player vs Bot"),
                ("2. PVP", "Player vs Player")
            ]

            for idx, (mode, desc) in enumerate(mode_buttons):
                y_pos = HEIGHT//2 - 100 + idx * 120
                button_rect = pygame.Rect(WIDTH//2 - 200, y_pos, 400, 80)
                
                # Button hover effect
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (60, 60, 70), button_rect, 0, border_radius=15)
                    pygame.draw.rect(screen, (100, 100, 255), button_rect, 3, border_radius=15)
                else:
                    pygame.draw.rect(screen, (40, 40, 50), button_rect, 0, border_radius=15)
                    pygame.draw.rect(screen, GRAY, button_rect, 2, border_radius=15)

                # Mode text
                mode_text = font.render(mode, True, WHITE)
                screen.blit(mode_text, (button_rect.centerx - mode_text.get_width()//2, 
                                      button_rect.y + 15))
                
                # Description text
                desc_text = small_font.render(desc, True, GRAY)
                screen.blit(desc_text, (button_rect.centerx - desc_text.get_width()//2, 
                                       button_rect.y + 45))
        else:
            # Draw title with glow effect
            title = "Select Game Duration"
            title_font = pygame.font.SysFont(None, 70)
            
            # Glow effect
            glow = title_font.render(title, True, (30, 30, 100))
            screen.blit(glow, (WIDTH//2 - glow.get_width()//2 + 2, 80 + 2))  # Moved up slightly
            
            # Main title
            text = title_font.render(title, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 80))  # Moved up slightly

            # Timer selection buttons with centered positioning
            timer_options = [
                ("A. 1 Minute", "Quick Match", 60),
                ("B. 2 Minutes", "Standard Match", 120),
                ("C. 3 Minutes", "Extended Match", 180)
            ]

            # Center the entire button group vertically
            total_height = len(timer_options) * 70 + (len(timer_options) - 1) * 30  # Button height + spacing
            start_y = (HEIGHT - total_height) // 2 + 30  # Added offset to account for title

            for i, (text, desc, duration) in enumerate(timer_options):
                y_pos = start_y + i * (70 + 30)  # Button height (70) + spacing (30)
                
                # Center buttons horizontally
                button_rect = pygame.Rect(WIDTH//2 - 150, y_pos, 300, 70)
                
                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (40, 40, 80), button_rect)
                    pygame.draw.rect(screen, (100, 100, 255), button_rect, 3, border_radius=10)
                else:
                    pygame.draw.rect(screen, (30, 30, 60), button_rect)
                    pygame.draw.rect(screen, GRAY, button_rect, 2, border_radius=10)

                # Timer text
                timer_text = font.render(text, True, WHITE)
                screen.blit(timer_text, (button_rect.centerx - timer_text.get_width()//2, 
                                       button_rect.y + 10))
                
                # Description text
                desc_text = small_font.render(desc, True, GRAY)
                screen.blit(desc_text, (button_rect.centerx - desc_text.get_width()//2, 
                                      button_rect.y + 40))

            # Move controls text to very bottom of screen
            controls_text = "Press M to Toggle Music | Press Q to Quit"
            controls = small_font.render(controls_text, True, (150, 150, 150))
            screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT - 30))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_m:
                    toggle_music()
                
                if game_mode:
                    if event.key in [pygame.K_a, pygame.K_1]:
                        selected_timer = 60
                        running = False
                    elif event.key in [pygame.K_b, pygame.K_2]:
                        selected_timer = 120
                        running = False
                    elif event.key in [pygame.K_c, pygame.K_3]:
                        selected_timer = 180
                        running = False
                else:
                    if event.key == pygame.K_1:
                        game_mode = "PVE"
                    elif event.key == pygame.K_2:
                        game_mode = "PVP"

        pygame.display.update()
        last_update = current_update
        clock.tick(60)

    return selected_timer, game_mode

def display_end_screen(snake1_score, snake2_score, is_bot_game):
    """Display the end game screen with scores and wait for space to return to menu"""
    screen.fill(BLACK)
    
    # Display RSU logo
    draw_logo()
    
    player1_name = "Player 1"
    player2_name = "Bot" if is_bot_game else "Player 2"
    
    # Determine winner
    if snake1_score > snake2_score:
        display_message(f"{player1_name} Wins!", RED, WIDTH // 3, HEIGHT // 3)
    elif snake2_score > snake1_score:
        display_message(f"{player2_name} Wins!", BLUE if not is_bot_game else YELLOW, WIDTH // 3, HEIGHT // 3)
    else:
        display_message("It's a Tie!", WHITE, WIDTH // 3, HEIGHT // 3)
    
    # Sort scores to display in order
    players = [(player1_name, snake1_score, RED), (player2_name, snake2_score, BLUE if not is_bot_game else YELLOW)]
    players.sort(key=lambda x: x[1], reverse=True)
    
    # Display scores in order
    y_pos = HEIGHT // 2
    for i, (name, score, color) in enumerate(players, 1):
        display_message(f"{i}. {name}: {score}", color, WIDTH // 3, y_pos)
        y_pos += 40
    
    # Prompt to return to menu
    display_message("Press SPACE to return to main menu", WHITE, WIDTH // 4, HEIGHT - 100)
    # Add note about music toggle
    display_message("Press M to toggle music", WHITE, WIDTH // 4, HEIGHT - 60)
    pygame.display.update()
    
    # Wait for space key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return True  # Return to main menu
                elif event.key == pygame.K_m:
                    toggle_music()
    
    return False  # Should not reach here

def show_preparation_screen(is_bot_game):
    waiting = True
    
    # Font settings with more balanced sizes
    title_font = pygame.font.SysFont("arial", 36, bold=True)
    header_font = pygame.font.SysFont("arial", 33, bold=True)
    game_font = pygame.font.SysFont("consolas", 28)
    
    while waiting:
        screen.fill((15, 15, 35))
        
        # Title Box - Centered at top
        title = "Get Ready!"
        title_surface = title_font.render(title, True, WHITE)
        title_box = pygame.Rect(WIDTH//2 - 90, 20, 180, 50)  # Moved up slightly
        pygame.draw.rect(screen, (30, 30, 60), title_box, 0, 10)
        pygame.draw.rect(screen, (100, 100, 255), title_box, 2, 10)
        
        # Center title text in box
        title_x = title_box.centerx - title_surface.get_width()//2
        title_y = title_box.centery - title_surface.get_height()//2
        screen.blit(title_surface, (title_x, title_y))

        # Controls Box - Adjusted height for better fit
        controls_box = pygame.Rect(WIDTH//2 - 350, 90, 700, 280)
        pygame.draw.rect(screen, (30, 30, 60), controls_box, 0, 15)
        pygame.draw.rect(screen, (100, 100, 255), controls_box, 2, 15)
        
        # Controls Header
        header_text = header_font.render("Game Controls", True, WHITE)
        header_x = controls_box.centerx - header_text.get_width()//2
        header_y = controls_box.y + 15
        screen.blit(header_text, (header_x, header_y))

        if is_bot_game:
            # Player Box - Made smaller to fit
            player_box = pygame.Rect(controls_box.x + 40, controls_box.y + 60, 260, 190)
            pygame.draw.rect(screen, (40, 40, 70), player_box, 0, 10)
            pygame.draw.rect(screen, RED, player_box, 2, 10)

            # Bot Box - Made smaller to fit
            bot_box = pygame.Rect(controls_box.right - 300, controls_box.y + 60, 260, 190)
            pygame.draw.rect(screen, (40, 40, 70), bot_box, 0, 10)
            pygame.draw.rect(screen, YELLOW, bot_box, 2, 10)

            # Player Controls
            title_text = game_font.render("Player (Red)", True, RED)
            title_x = player_box.centerx - title_text.get_width()//2
            title_y = player_box.y + 20
            screen.blit(title_text, (title_x, title_y))

            controls = [
                ("W", "(Up)"),
                ("A", "(Left)"),
                ("S", "(Down)"),
                ("D", "(Right)")
            ]

            start_y = player_box.y + 60
            spacing = 30
            for i, (key, direction) in enumerate(controls):
                key_surface = game_font.render(key, True, WHITE)
                key_x = player_box.centerx - 50
                key_y = start_y + (i * spacing)
                screen.blit(key_surface, (key_x, key_y))
                
                dash_surface = game_font.render("-", True, WHITE)
                dash_x = player_box.centerx - 20
                screen.blit(dash_surface, (dash_x, key_y))
                
                dir_surface = game_font.render(direction, True, GRAY)
                dir_x = player_box.centerx + 10
                screen.blit(dir_surface, (dir_x, key_y))

            # Bot Info with explanation
            bot_info = [
                ("Bot (Yellow)", YELLOW),
                ("AI Controlled", WHITE),
                ("Finds Food", WHITE),
                ("Avoids Walls", WHITE),
                ("Auto Navigate", WHITE)
            ]

            # Display bot info with same spacing
            start_y = bot_box.y + 20
            for i, (text, color) in enumerate(bot_info):
                text_surface = game_font.render(text, True, color)
                text_x = bot_box.centerx - text_surface.get_width()//2
                text_y = start_y + (i * spacing)
                screen.blit(text_surface, (text_x, text_y))

        else:
            # PVP Mode - Similar adjustments for player boxes
            player1_box = pygame.Rect(controls_box.x + 40, controls_box.y + 60, 260, 190)
            pygame.draw.rect(screen, (40, 40, 70), player1_box, 0, 10)
            pygame.draw.rect(screen, RED, player1_box, 2, 10)

            player2_box = pygame.Rect(controls_box.right - 300, controls_box.y + 60, 260, 190)
            pygame.draw.rect(screen, (40, 40, 70), player2_box, 0, 10)
            pygame.draw.rect(screen, BLUE, player2_box, 2, 10)

            # Player 1 Controls
            title_text = game_font.render("Player 1 (Red)", True, RED)
            title_x = player1_box.centerx - title_text.get_width()//2
            title_y = player1_box.y + 20
            screen.blit(title_text, (title_x, title_y))

            p1_controls = [
                ("W", "(Up)"),
                ("A", "(Left)"),
                ("S", "(Down)"),
                ("D", "(Right)")
            ]

            start_y = player1_box.y + 60
            spacing = 30
            for i, (key, direction) in enumerate(p1_controls):
                key_surface = game_font.render(key, True, WHITE)
                key_x = player1_box.centerx - 50
                key_y = start_y + (i * spacing)
                screen.blit(key_surface, (key_x, key_y))
                
                dash_surface = game_font.render("-", True, WHITE)
                dash_x = player1_box.centerx - 20
                screen.blit(dash_surface, (dash_x, key_y))
                
                dir_surface = game_font.render(direction, True, GRAY)
                dir_x = player1_box.centerx + 10
                screen.blit(dir_surface, (dir_x, key_y))

            # Player 2 Controls
            title_text = game_font.render("Player 2 (Blue)", True, BLUE)
            title_x = player2_box.centerx - title_text.get_width()//2
            title_y = player2_box.y + 20
            screen.blit(title_text, (title_x, title_y))

            p2_controls = [
                ("↑", "(Up)"),
                ("←", "(Left)"),
                ("↓", "(Down)"),
                ("→", "(Right)")
            ]

            start_y = player2_box.y + 60
            for i, (key, direction) in enumerate(p2_controls):
                key_surface = game_font.render(key, True, WHITE)
                key_x = player2_box.centerx - 50
                key_y = start_y + (i * spacing)
                screen.blit(key_surface, (key_x, key_y))
                
                dash_surface = game_font.render("-", True, WHITE)
                dash_x = player2_box.centerx - 20
                screen.blit(dash_surface, (dash_x, key_y))
                
                dir_surface = game_font.render(direction, True, GRAY)
                dir_x = player2_box.centerx + 10
                screen.blit(dir_surface, (dir_x, key_y))

        # Power-ups Box with header
        powerup_box = pygame.Rect(WIDTH//2 - 300, controls_box.bottom + 20, 600, 100)
        pygame.draw.rect(screen, (30, 30, 60), powerup_box, 0, 10)
        pygame.draw.rect(screen, (100, 100, 255), powerup_box, 2, 10)

        # Power-ups Header
        powerup_header = header_font.render("Power-ups", True, WHITE)
        powerup_x = powerup_box.centerx - powerup_header.get_width()//2
        screen.blit(powerup_header, (powerup_x, powerup_box.y + 10))

        # Display power-ups with icons
        icon_size = 32
        padding = 20

        # Speed boost power-up
        speed_x = powerup_box.x + 50
        speed_y = powerup_box.centery + 5
        screen.blit(pygame.transform.scale(flash_image, (icon_size, icon_size)), (speed_x, speed_y))
        speed_text = game_font.render("Speed Boost (5s)", True, WHITE)
        screen.blit(speed_text, (speed_x + icon_size + 10, speed_y))

        # Freeze power-up
        freeze_x = powerup_box.centerx + 50
        freeze_y = powerup_box.centery + 5
        screen.blit(pygame.transform.scale(snow_image, (icon_size, icon_size)), (freeze_x, freeze_y))
        freeze_text = game_font.render("Freeze (3s)", True, WHITE)
        screen.blit(freeze_text, (freeze_x + icon_size + 10, freeze_y))

        # Press Space Box at bottom
        space_box = pygame.Rect(WIDTH//2 - 200, HEIGHT - 60, 400, 40)
        pygame.draw.rect(screen, (30, 30, 60), space_box, 0, 10)
        pygame.draw.rect(screen, (100, 100, 255), space_box, 2, 10)

        # Press Space Text with pulsing effect
        space_text = game_font.render("Press SPACE to Start", True, WHITE)
        space_alpha = abs(math.sin(time.time() * 2)) * 255
        space_text.set_alpha(int(space_alpha))
        screen.blit(space_text, (WIDTH//2 - space_text.get_width()//2, HEIGHT - 55))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_m:
                    toggle_music()

        pygame.display.update()
        clock.tick(60)
