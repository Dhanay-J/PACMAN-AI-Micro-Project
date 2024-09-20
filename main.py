import pygame
import random
import heapq
from collections import deque
import json
from map import Map
from pacman import Pacman
from ghost import Ghost
from settings import *

# Initialize Pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman")


def bfs(ghost, pacman, game_map):
    start = (ghost.x, ghost.y)
    goal = (pacman.x, pacman.y)
    queue = deque([[start]])
    visited = set([start])
    last_pos = None  # Track the last position

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == goal:
            return path
        
        # Randomize the directions to reduce repetitive movements
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if (0 <= next_pos[0] < GRID_WIDTH and 0 <= next_pos[1] < GRID_HEIGHT 
                and next_pos not in visited and not game_map.is_wall(next_pos[0], next_pos[1])):
                # Avoid backtracking immediately to the previous position
                if last_pos != next_pos:
                    queue.append(path + [next_pos])
                    visited.add(next_pos)
                    last_pos = (x, y)
                    if len(visited) > 100:  # Limit search to prevent freezing
                        return path
    return []


def dfs(ghost, pacman, game_map):
    start = (ghost.x, ghost.y)
    goal = (pacman.x, pacman.y)
    stack = [[start]]
    visited = set([start])
    last_pos = None  # Track the last position

    while stack:
        path = stack.pop()
        x, y = path[-1]
        if (x, y) == goal:
            return path

        # Randomize the directions to reduce repetitive movements
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if (0 <= next_pos[0] < GRID_WIDTH and 0 <= next_pos[1] < GRID_HEIGHT 
                and next_pos not in visited and not game_map.is_wall(next_pos[0], next_pos[1])):
                # Avoid backtracking immediately to the previous position
                if last_pos != next_pos:
                    stack.append(path + [next_pos])
                    visited.add(next_pos)
                    last_pos = (x, y)
                    if len(visited) > 100:  # Limit search to prevent freezing
                        return path
    return []


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(ghost, pacman, game_map):
    start = (ghost.x, ghost.y)
    goal = (pacman.x, pacman.y)
    heap = [(0, start, [])]
    visited = set()
    
    while heap:
        _, current, path = heapq.heappop(heap)
        if current == goal:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            if 0 <= next_pos[0] < GRID_WIDTH and 0 <= next_pos[1] < GRID_HEIGHT:
                if not game_map.is_wall(next_pos[0], next_pos[1]) and next_pos not in visited:
                    new_path = path + [current]
                    priority = len(new_path) + manhattan_distance(next_pos, goal)
                    heapq.heappush(heap, (priority, next_pos, new_path))
                    if len(visited) > 100:  # Limit search to prevent freezing
                        return path + [current]
    return []

def save_high_score(score):
    try:
        with open('high_scores.json', 'r') as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []
    
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]  # Keep only top 5 scores
    
    with open('high_scores.json', 'w') as f:
        json.dump(high_scores, f)

def load_high_scores():
    try:
        with open('high_scores.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    high_scores = load_high_scores()

    for level in range(3):
        game_map = Map(level)
        pacman = Pacman(1, 1)
        ghosts = [Ghost(GRID_WIDTH - 2, GRID_HEIGHT - 2)]
        
        # Add initial fruits
        for _ in range(5):
            game_map.add_fruit(pacman, ghosts)

        algorithm = [dfs, bfs, a_star][level]
        
        score = 0
        start_time = pygame.time.get_ticks()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pacman.set_direction((0, -1)) 
                    elif event.key == pygame.K_DOWN:
                        pacman.set_direction((0, 1)) 
                    elif event.key == pygame.K_LEFT:
                        pacman.set_direction((-1, 0)) 
                    elif event.key == pygame.K_RIGHT:
                        pacman.set_direction((1, 0)) 

            pacman.move(game_map)
            
            
            for ghost in ghosts:
                ghost.move(pacman, game_map, algorithm)
                ghost.increase_velocity(pacman.velocity)

            # Check for collisions with fruits
            for fruit in game_map.fruits[:]:
                if (pacman.x, pacman.y) == (fruit.x, fruit.y):
                    score += fruit.score
                    game_map.remove_fruit(fruit)
                    game_map.add_fruit(pacman, ghosts)

            # Check for collisions with ghosts
            for ghost in ghosts:
                if (pacman.x, pacman.y) == (ghost.x, ghost.y):
                    running = False

            # Draw everything
            screen.fill(BLACK)
            game_map.draw(screen)
            pacman.draw(screen)
            for ghost in ghosts:
                ghost.draw(screen)

            # Draw score and time
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            time_left = max(0, GAME_TIME - elapsed_time)
            score_text = font.render(f"Score: {score}", True, WHITE)
            time_text = font.render(f"Time: {time_left}", True, WHITE)
            level_text = font.render(f"Level: {level + 1}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(time_text, (SCREEN_WIDTH - 110, 10))
            screen.blit(level_text, (SCREEN_WIDTH // 2 - 40, 10))

            pygame.display.flip()
            clock.tick(FPS)

            if time_left == 0:
                running = False

        save_high_score(score)

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50))
    
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

    high_scores = load_high_scores()
    high_score_text = font.render(f"High Score: {max(high_scores) if high_scores else 0}", True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

    pygame.quit()

if __name__ == "__main__":
    main()