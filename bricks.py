import pygame
from pygame.locals import *

class Bricks:
    """
    Class that houses the brick object, which are the objects that you want to hit with the ball
    """
    def __init__(self, window_width, cols, rows, brick_color, window, background_color):
        """
        Initializes variables for the brick class
        :param window_width: width of game
        :param cols: amount of columns if bricks on the screen
        :param rows: amount of rows of bricks on the screen
        :param brick_color: designated color for the bricks
        :param window: Object that is the display for the game
        :param background_color: color for the background of the game, used to make borders for the bricks
        """
        self.width = window_width // cols
        self.height = 75
        self.rows = rows
        self.cols = cols
        self.window = window
        self.brick_color = brick_color
        self.background_color = background_color
        self.grid = []

    def create_grid(self):
        """
        Function that creates a 2D array that holds all the bricks
        """
        for row in range(self.rows):
            brick_row = []
            for col in range(self.cols):
                rect = pygame.Rect((self.width * col), (self.height * row), self.width, self.height)
                brick_row.append(rect)
            self.grid.append(brick_row)

    def draw_bricks(self):
        """
        Function that draws each brick onto the window, is called repeatedly to update whenever a brick is destroyed
        """
        for row in self.grid:
            for brick in row:
                pygame.draw.rect(self.window, self.brick_color, brick)
                pygame.draw.rect(self.window, self.background_color, brick, 4)

    def get_grid(self):
        """
        Function that returns the grid
        :return: The 2D array of bricks
        """
        return self.grid
