import heapq
from settings import SNAKE_SIZE

def find_path_to_food(snake_head, food_pos, obstacles, grid_width, grid_height):
    # Convert positions to grid coordinates
    start = (snake_head[0] // SNAKE_SIZE, snake_head[1] // SNAKE_SIZE)
    goal = (food_pos[0] // SNAKE_SIZE, food_pos[1] // SNAKE_SIZE)
    
    # Create set of obstacles (snake bodies)
    obstacle_set = set((pos[0] // SNAKE_SIZE, pos[1] // SNAKE_SIZE) for pos in obstacles)
    
    # Queue for Dijkstra's algorithm
    queue = [(0, start, [])]  # (cost, position, path)
    visited = set()
    
    # Possible moves: up, right, down, left
    directions = [
        (0, -1),  # up
        (1, 0),   # right
        (0, 1),   # down
        (-1, 0)   # left
    ]
    
    while queue:
        cost, current, path = heapq.heappop(queue)
        
        # Convert to grid coordinates
        current_x, current_y = current
        
        # If we've reached the goal
        if current == goal:
            if not path:  # If path is empty, move in any valid direction
                for dx, dy in directions:
                    nx, ny = current_x + dx, current_y + dy
                    if 0 <= nx < grid_width and 0 <= ny < grid_height and (nx, ny) not in obstacle_set:
                        return (dx * SNAKE_SIZE, dy * SNAKE_SIZE)
            else:
                # Return the first step in the path
                first_step = path[0]
                dx = first_step[0] - start[0]
                dy = first_step[1] - start[1]
                return (dx * SNAKE_SIZE, dy * SNAKE_SIZE)
        
        # Skip if we've already visited this cell
        if current in visited:
            continue
            
        visited.add(current)
        
        # Check all adjacent cells
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            
            # Check if the new position is valid
            if 0 <= nx < grid_width and 0 <= ny < grid_height and (nx, ny) not in obstacle_set and (nx, ny) not in visited:
                # Calculate Manhattan distance to the goal as a heuristic
                h = abs(nx - goal[0]) + abs(ny - goal[1])
                new_cost = cost + 1 + h  # Cost so far + 1 step + heuristic
                
                # Add new position to the queue
                new_path = path + [(nx, ny)]
                heapq.heappush(queue, (new_cost, (nx, ny), new_path))
    
    # If no path found, move in a random valid direction
    import random
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = start[0] + dx, start[1] + dy
        if 0 <= nx < grid_width and 0 <= ny < grid_height and (nx, ny) not in obstacle_set:
            return (dx * SNAKE_SIZE, dy * SNAKE_SIZE)
            
    # If completely stuck, just try to go up
    return (0, -SNAKE_SIZE)
