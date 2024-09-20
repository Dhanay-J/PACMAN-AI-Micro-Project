
import time
import pygame
from settings import *

class SpriteSheet:
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()  # Use convert_alpha to handle transparency
        
    def get_image(self, x, y, width, height):
        # Create a surface with an alpha channel for transparency
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))  # Scale image if needed
        return image


class Pacman:
    def __init__(self, x, y,assets_folder='./assets/images/pacman'):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.velocity = PACMAN_SPEED  # Pacman's velocity (moves per second)
        self.last_move_time = time.time()
        

        self.animation_steps = 3
        self.frame = 0
        self.animation_list = []

        self.l_to_r_sprite_sheet = SpriteSheet(assets_folder+"/l-r_pacman.png")
        self.l_to_r_animation = [self.l_to_r_sprite_sheet.get_image(i * 115,0, 115, 115) for i in range(self.animation_steps)]

        self.r_to_l_sprite_sheet = SpriteSheet(assets_folder+"/r-l_pacman.png")
        self.r_to_l_animation = [self.r_to_l_sprite_sheet.get_image(i * 115,0, 115, 115) for i in range(self.animation_steps)]

        self.t_to_b_sprite_sheet = SpriteSheet(assets_folder+"/t-b_pacman.png")
        self.t_to_b_animation = [self.t_to_b_sprite_sheet.get_image(0,i * 115, 115, 115) for i in range(self.animation_steps)]

        self.b_to_t_sprite_sheet = SpriteSheet(assets_folder+"/b-t_pacman.png")
        self.b_to_t_animation = [self.b_to_t_sprite_sheet.get_image(0,i * 115, 115, 115) for i in range(self.animation_steps)]

        self.last_update = pygame.time.get_ticks()
        self.animation_cool_down = 1/FPS # milliseconds

        self.animation_list = self.b_to_t_animation


    def set_direction(self, direction):
        self.direction = direction
        # UP
        if self.direction == (0,-1):
            self.animation_list = self.b_to_t_animation
        # Down
        if self.direction == (0,1):
            self.animation_list = self.t_to_b_animation
        # Left
        if self.direction == (-1,0):
            self.animation_list = self.r_to_l_animation
        # Right
        if self.direction == (1,0):
            self.animation_list = self.l_to_r_animation


    def move(self, game_map):
        current_time = time.time()
        if current_time - self.last_move_time >= 1 / self.velocity:
            new_x = max(0, min(self.x + self.direction[0], GRID_WIDTH - 1))
            new_y = max(0, min(self.y + self.direction[1], GRID_HEIGHT - 1))
            if not game_map.is_wall(new_x, new_y):
                self.x, self.y = new_x, new_y
            self.last_move_time = current_time

    def draw(self, screen:pygame.Surface):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cool_down:
            self.frame = (self.frame + 1) % self.animation_steps
            self.last_update = current_time
        
        screen.blit(self.animation_list[self.frame], (self.x*CELL_SIZE, self.y*CELL_SIZE))

        # pygame.draw.circle(screen, YELLOW, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)