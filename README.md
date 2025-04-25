# Python Chaser

A snake-like game where players compete to collect food and gain power-ups.

## Features
- Player vs. Player or Player vs. Bot modes
- Multiple game durations (1, 2, or 3 minutes)
- Power-ups: Speed Boost and Freeze
- Intelligent AI opponent using A* pathfinding

## How to Play
1. Use WASD keys to control Player 1 (Red)
2. In PVP mode, use Arrow keys to control Player 2 (Blue)
3. Collect green food to increase your score
4. Collect power-ups to gain advantages:
   - Lightning bolt: Speed boost for 5 seconds
   - Snowflake: Freeze opponent for 3 seconds
5. The player with the highest score when time runs out wins!

## Controls
- M: Toggle music
- Q: Quit game
- Space: Progress through menus

## Requirements
- Python 3.x
- Pygame

## Installation
```bash
# Install pygame
pip install pygame

# Run the game
python pChaser_1.0.py
```

## Project Structure
- `pChaser_1.0.py`: Main game entry point
- `settings.py`: Game constants and configurations
- `game_mechanics.py`: Core game logic and loop
- `pathfinding.py`: AI pathfinding algorithm
- `game_screens.py`: Menu and UI screens
- `ui_elements.py`: UI drawing utilities
