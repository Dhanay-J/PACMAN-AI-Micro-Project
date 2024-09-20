import pygame
from settings import *

import os
import random
import pygame

class Fruit:
    def __init__(self, x, y, assets_folder='./assets/images/fruits'):
        self.x = x
        self.y = y
        self.assets_folder = assets_folder

        # Load all fruit images from the assets folder
        self.fruit_images = [file for file in os.listdir(self.assets_folder) if file.endswith('.png')]
        
        # Randomly choose a fruit image
        self.image_name = random.choice(self.fruit_images)
        self.image = pygame.image.load(os.path.join(self.assets_folder, self.image_name))

        # Extract score from the last digit in the image name before the file extension fileName_score.png
        self.score = int(self.image_name[:-4].split('_')[-1])

        # Resize the image to fit in the cell
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    def draw(self, screen):
        # Draw the fruit image on the screen at the specified position
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
