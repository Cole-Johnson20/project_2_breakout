import ctypes

import pygame
from bricks import *
from line import *
from ball import *
from gui import *
import csv
from pygame.locals import *

pygame.init()
font = pygame.font.SysFont('Constantia', 30)
window_width = 1000
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Breakout')
background_color = (0, 0, 0)
brick_color = (0, 255, 0)
cols = 3
rows = 5
fps = 60
fps_clock = pygame.time.Clock()
ball_speed = 5
line_speed = 8
top_scores = []



def main():
    """
    Function that serves os the main loop of the game, it refreshes the screen,
     makes objects of classes so that the game can be played, and allows the game to be quit
    """
    grid = Bricks(window_width, cols, rows, brick_color, window, background_color)
    grid.create_grid()
    player_line = Line(window_width, window_height, cols, line_speed, window)
    ball = Ball(player_line.get_x_coord() + (player_line.line_width // 2), player_line.get_y_coord() - 30, window_width,
                window_height, grid.get_grid(), window, player_line, ball_speed)
    game_running = True
    while game_running:
        fps_clock.tick(fps)
        window.fill(background_color)
        player_line.move()
        player_line.draw_line()
        grid.draw_bricks()
        ball.move_ball()
        ball.draw_ball()
        if ball.get_player_win() is True:
            draw_text(f'You Win! Your Score was {ball.get_score()}', font, (0, 255, 0), 300, 500, window)
            add_leaderboard_entry(ball.get_score())
            restart()

        if ball.get_player_lose() is True:
            draw_text(f'You Lose... Your Score was {ball.get_score()}', font, (0, 255, 0), 300, 500, window)
            add_leaderboard_entry(ball.get_score())
            restart()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_game()
        pygame.display.update()


def pause_game():
    """
    Function that allows pauses the game by putting it in a loop and then unpauses the game when the player presses 'p'
    """
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        draw_text('Game is paused, press \'p\' to continue.', font, (255, 255, 255), 250, 500, window)


def draw_text(text, font, text_col, x, y, window):
    """
    Function that allows a string to be input and displayeed on the screen at a certain position(x, y)
    :param text: String that is to be displayed
    :param font: Font of the string that is displayed
    :param text_col: Color of the text that is displayed
    :param x: X-coordinate for the top-left corner of the text box
    :param y: Y-coordinate for the top of the text box
    :param window: Window that the text is being displayed on
    """
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))
    pygame.display.update()


def title_screen():
    """
    Displays the title screen of the game and allows the user to navigate to either the game, tutorial, or leaderboard
    """
    window.fill(background_color)
    selection = False
    while selection is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    selection = True
                    main()
                if event.key == pygame.K_t:
                    window.fill(background_color)
                    tutorial()
                if event.key == pygame.K_l:
                    window.fill(background_color)
                    leaderboard()
        draw_text('BREAKOUT', font, (0, 255, 0), 390, 150, window)
        draw_text('Press \'s\' to start the game.', font, (0, 255, 0), 300, 350, window)
        draw_text('Press \'t\' to read the tutorial.', font, (0, 255, 0), 300, 550, window)
        draw_text('Press \'l\' to look at the leaderboard.', font, (0, 255, 0), 290, 750, window)



def tutorial():
    """
    Displays the text for the tutorial and allows the player to exit the tutorial
    """
    reading_tutorial = True
    while reading_tutorial:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    reading_tutorial = False
                    window.fill(background_color)
                    title_screen()
        draw_text('Use <- and -> (left and right arrows) to move the paddle.', font, (0, 255, 0), 150, 50, window)
        draw_text('Bounce the ball back up with the paddle and don\'t let it ', font, (0, 255, 0), 150, 150, window)
        draw_text('fall through the bottom of the screen. Destroy all of the', font, (0, 255, 0), 150, 250, window)
        draw_text('bricks to win the game. Each brick destroyed earns points.', font, (0, 255, 0), 150, 350, window)
        draw_text('Press \'p\' to pause the game at any time.', font, (0, 255, 0), 250, 450, window)
        draw_text('Press \'t\' to go back to the title screen.', font, (0, 255, 0), 250, 550, window)

def restart():
    """
    Code to allow the user to restart the game once the game has ended
    """
    selection = False
    while selection is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    selection = True
                    title_screen()
        draw_text('Press \'r\' to restart the game.', font, (0, 255, 0), 300, 650, window)




def add_leaderboard_entry(score):
    """
    Creates a seperate GUI that allows the user to input their name to be put on the leaderboard
    :param score: Score that the user has achieved
    """
    screen = Tk()
    screen.title('Input Name')
    screen.geometry('300x200')
    widgets = GUI(screen, score)
    screen.mainloop()

def leaderboard():
    """
    Function that displays the leaderboard,
    also reads the leaderboard.csv file to get all the player's scores
    """
    all_scores = []
    reading_leaderboard = True
    with open('leaderboard.csv', 'r+', newline='\r\n') as csvfile:
        players = []
        for row in csvfile:
            row = row.split(',')
            players.append(row)
            all_scores.append(int(row[1]))
        high_scores = get_highest_players(all_scores, players)
    while reading_leaderboard:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    reading_leaderboard = False
                    window.fill(background_color)
                    title_screen()

        draw_text(f'1. {get_player_string(high_scores[0], 0)}', font, (0, 255, 0), 450, 50, window)
        draw_text(f'2. {get_player_string(high_scores[1], 1)}', font, (0, 255, 0), 450, 150, window)
        draw_text(f'3. {get_player_string(high_scores[2], 2)}', font, (0, 255, 0), 450, 250, window)
        draw_text(f'4. {get_player_string(high_scores[3], 3)}', font, (0, 255, 0), 450, 350, window)
        draw_text(f'5. {get_player_string(high_scores[4], 4)}', font, (0, 255, 0), 450, 450, window)
        draw_text('Press \'l\' to go back to the title screen.', font, (0, 255, 0), 250, 550, window)

def get_highest_players(scores, players) -> list[list]:
    """
    Function that finds the five highest scores from the players in the leaderboard.csv file
    :param scores: List of just the scores of the players
    :param players: list of all the player's and their scores
    :return: List of the players with the 5 highest scores
    """
    high_score_players = []
    temp_scores = scores
    temp_players = players
    for i in range(5):
        if len(scores) > 0:
            high_index = 0
            for num in temp_scores:
                if num > temp_scores[high_index]:
                    high_index = temp_scores.index(num)
        high_score_players.append(temp_players[high_index])
        top_scores.append(temp_scores[high_index])
        temp_scores.pop(high_index)
        temp_players.pop(high_index)
    return high_score_players

def get_player_string(player, index) -> str:
    """
    Method to simplify typing out the string of the player and their score for the leaderboard
    :param player: The name of the player
    :param index: Index of the player's score in the list of all the scores
    :return: String of what is to be displayed on the leaderboard
    """
    player_string = ''
    player_string += (player[0] + ' ')
    player_string += (str(top_scores[index]))
    return player_string

if __name__ == '__main__':
    title_screen()
