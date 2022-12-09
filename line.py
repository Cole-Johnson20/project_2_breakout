import pygame
from pygame.locals import *


class Line:
    """
    Class that creates an object line, which is the movable tool that the player can use to keep the ball in bounds
    """
    def __init__(self, window_width, window_height, cols, player_line_speed, window):
        """
        Function that initializes all the necessary variables for the line to be able to move
        :param window_width: Width of the window
        :param window_height: Height of the window
        :param cols: Amount of columns of bricks
        :param player_line_speed: Speed of the line (amount of pixels moved per frame)
        :param window: Object that is the display for the game
        """
        self.window_width = window_width
        self.line_width = window_width / cols
        self.line_height = 30
        self.line_x_coord = window_width / 2 - self.line_width / 2
        self.line_y_coord = window_height - self.line_height - 10
        self.line = Rect(self.line_x_coord, self.line_y_coord, self.line_width, self.line_height)
        self.window = window
        self.line_speed = player_line_speed

    def move(self):
        """
        Function that gathers user input and correlates those inputs to movement of the line,
         allowing the player to control it
        """
        action = pygame.key.get_pressed()
        if action[pygame.K_LEFT] and self.line.left > 0:
            self.line.x -= self.line_speed
        if action[pygame.K_RIGHT] and self.line.right < self.window_width:
            self.line.x += self.line_speed

    def draw_line(self):
        """
        Function that draws the line onto the window, is called repeatedly to update whenever the line is moved
        """
        pygame.draw.rect(self.window, (255, 0, 0), self.line)
        pygame.draw.rect(self.window, (0, 0, 0), self.line, 3)

    def get_x_coord(self) -> int:
        """
        :return: Returns the x coordinate of where the line is (top-left corner)
        """
        return self.line.x

    def get_y_coord(self) -> int:
        """
        :return: Returns the y coordinate of where the line is (top-left corner)
        """
        return self.line.y

