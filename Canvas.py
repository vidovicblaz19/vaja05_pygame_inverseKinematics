import random
import pygame
import colors as col

class Canvas:
    def __init__(self, width, height):
        self.height = height
        self.width = width

    def setup(self, screen, color):
        screen.fill(color)
        return screen
