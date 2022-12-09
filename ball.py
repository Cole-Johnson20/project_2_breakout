import pygame
from pygame.locals import *


class Ball:
    """
    Class that creates the object of ball, a never-stopping object that bounces on the walls, bricks, and the player-controlled line
    """

    def __init__(self, start_x_coord, start_y_coord, screen_width, screen_height, grid, window, player_line,
                 ball_speed):
        """
        Initializes all variable for
        :param start_x_coord: Starting x coordinate for the ball (based on the line)
        :param start_y_coord: Starting y coordinate for the ball (based on the line)
        :param screen_width: Width of the screen
        :param screen_height: Height of the screen
        :param grid: 2D array of bricks
        :param window: Object that is the display for the game
        :param player_line: The object from the line class, which is player-controlled
        :param ball_speed: Int value of the speed of the ball
        """
        self.x_coord = start_x_coord - 10
        self.y_coord = start_y_coord
        self.ball = Rect(self.x_coord, self.y_coord, 20, 20)
        self.window = window
        self.ball_direction_x = 1
        self.ball_direction_y = -1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_line = player_line
        self.grid = grid
        self.game_over = False
        self.ball_speed = ball_speed
        self.score = 0
        self.player_lose = False
        self.player_win = False

    def move_ball(self):
        """
        Function that contains the logic that allows the ball to bounce off the walls, bricks, and player line
        """
        self.game_over = True
        self.ball.x += self.ball_speed * self.ball_direction_x
        self.ball.y += self.ball_speed * self.ball_direction_y

        if self.ball.right > self.screen_width or self.ball.left < 0:
            self.ball_direction_x *= -1
        if self.ball.top < 0:
            self.ball_direction_y = 1
        if self.ball.bottom > self.screen_height:
            self.player_lose = True

        if self.ball.colliderect(self.player_line.line):
            if (self.player_line.line.top - self.ball.bottom) < 6 and self.ball_direction_y > 0:
                self.ball_direction_y = -1
            if (self.player_line.line.right - self.ball.left) < 6 and self.ball_direction_x < 0:
                self.ball_direction_x = 1
            if (self.ball.right - self.player_line.line.left) < 6 and self.ball_direction_x > 0:
                self.ball_direction_x = -1

        row_count = 0
        for row in self.grid:
            brick_count = 0
            for brick in row:
                if self.ball.colliderect(brick):
                    self.score += 100
                    if abs(brick.left - self.ball.right) < 6 and self.ball_direction_x > 0:
                        self.ball_direction_x = -1
                        self.grid[row_count][brick_count] = (0, 0, 0, 0)
                    if abs(self.ball.left - brick.right) < 6 and self.ball_direction_x < 0:
                        self.ball_direction_x = 1
                        self.grid[row_count][brick_count] = (0, 0, 0, 0)
                    if abs(self.ball.top - brick.bottom) < 6 and self.ball_direction_y < 0:
                        self.ball_direction_y = 1
                        self.grid[row_count][brick_count] = (0, 0, 0, 0)
                    if abs(brick.top - self.ball.bottom) < 6 and self.ball_direction_y > 0:
                        self.ball_direction_y = -1
                        self.grid[row_count][brick_count] = (0, 0, 0, 0)
                brick_count += 1

                if brick != (0, 0, 0, 0):
                    self.player_win = False
                    self.game_over = False
                if self.game_over is True:
                    self.player_win = True

            row_count += 1

    def draw_ball(self):
        """
        Function that draws the ball onto the window, is called repeatedly to update when the ball moves
        """
        pygame.draw.rect(self.window, (255, 0, 0), self.ball)
        pygame.draw.rect(self.window, (0, 0, 0), self.ball, 2)

    def get_score(self) -> int:
        return self.score

    def get_player_win(self) -> bool:
        return self.player_win

    def get_player_lose(self) -> bool:
        return self.player_lose
