#############################
## (C) Shay Goldshmit 2022 ##
#############################

import random
import MyGames.ConstColors as colors
from os import environ as env_var
try:
    import tkinter.messagebox
    import tkinter
except Exception:
    print(f'can not import tkinter!')
    tk_flag = False
else:
    tk_flag = True

env_var['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # for hiding an annoying message from Pygame
import pygame

pygame.init()
pygame.display.set_caption('Shay\'s Pong')

# constants
KEYBOARD_PRESSED = pygame.KEYDOWN
GAME_SPEED_START = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_COLOR = colors.SEAGREEN4
PEDAL_1_LENGTH = SCREEN_HEIGHT // 4
PEDAL_1_WIDTH = SCREEN_WIDTH // 100
PEDAL_1_COLOR = colors.BLACK
PEDAL_2_LENGTH = PEDAL_1_LENGTH
PEDAL_2_WIDTH = PEDAL_1_WIDTH
PEDAL_2_COLOR = colors.BLACK
BALL_COLOR = colors.BLACK
BALL_SIZE = PEDAL_1_WIDTH
STEP_LENGTH = 10

# global variables
game_screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
game_over = None
game_speed = None
pedal_1_dir = None
head_pos_x = None
head_pos_y = None
pedal_1_pos_lst = []
pos_ball_x = SCREEN_HEIGHT // 2
pos_ball_y = SCREEN_WIDTH // 2
score = None


def draw_ball(rand_new=False):
    global pos_ball_x
    global pos_ball_y

    if rand_new:
        pos_ball_x = random.randint(10, SCREEN_WIDTH - 5)
        pos_ball_x -= pos_ball_x % PEDAL_1_LENGTH
        pos_ball_y = random.randint(10, SCREEN_HEIGHT - 5)
        pos_ball_y -= pos_ball_y % PEDAL_1_LENGTH

    pygame.draw.circle(game_screen, BALL_COLOR, center=(pos_ball_x, pos_ball_y), radius=BALL_SIZE)


def init_game():
    global game_over
    global game_speed
    global pedal_1_dir
    global head_pos_y
    global head_pos_x
    global pedal_1_pos_lst
    global game_screen
    global score

    game_over = False
    game_speed = GAME_SPEED_START
    pedal_1_dir = ''
    head_pos_x = 0
    head_pos_y = random.randint(SCREEN_HEIGHT // 2 - SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 2 + SCREEN_HEIGHT // 4)
    head_pos_y -= (head_pos_y % PEDAL_1_LENGTH)
    pedal_1_pos_lst.append((head_pos_x, head_pos_y))
    score = 0
    draw_ball()


def finish_game():
    global game_over

    while not game_over:
        draw_score()
        font = pygame.font.Font('freesansbold.ttf', SCREEN_HEIGHT // 15)
        text = font.render('Game Over!', True, colors.RED1, colors.BLUE)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        game_screen.blit(text, textRect)
        pygame.display.update()

        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                game_over = True
            elif game_event.type == KEYBOARD_PRESSED:
                if game_event.key == pygame.K_ESCAPE:
                    game_over = True
                else:
                    init_game()
                    return


def draw_score():
    global score

    font = pygame.font.Font('freesansbold.ttf', SCREEN_HEIGHT // 30)
    text = font.render(f'Score: {score}', True, colors.BLACK, SCREEN_COLOR)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH / 14, SCREEN_HEIGHT / 40)
    game_screen.blit(text, textRect)


def draw_pedals():
    global pedal_1_pos_lst
    global BALL_COLOR

    for pos_tpl in pedal_1_pos_lst:
        pygame.draw.rect(game_screen, PEDAL_1_COLOR, [pos_tpl[0], pos_tpl[1], PEDAL_1_WIDTH, PEDAL_1_LENGTH])
    # for pos_tpl in pedal_2_pos_lst:
        pygame.draw.rect(game_screen, PEDAL_2_COLOR, [SCREEN_WIDTH - PEDAL_2_WIDTH, pos_ball_y, PEDAL_2_WIDTH, PEDAL_2_LENGTH])


def game_action(key: pygame.key):
    global head_pos_x
    global head_pos_y
    global pedal_1_dir
    global pedal_1_pos_lst
    global game_speed
    global score
    tail = pedal_1_pos_lst[0]

    if key == pygame.K_DOWN:
        pedal_1_dir = 'down'
    elif key == pygame.K_UP:
        pedal_1_dir = 'up'
    elif key == pygame.K_n:
        init_game()
    elif key == pygame.K_p:
        pedal_1_dir = ''

    if pedal_1_dir == 'down':
        head_pos_y += STEP_LENGTH
    elif pedal_1_dir == 'up':
        head_pos_y -= STEP_LENGTH
    else:
        # pause game
        return

    pedal_1_pos_lst.append((head_pos_x, head_pos_y))
    tail = pedal_1_pos_lst.pop(0)


def play_game():
    global game_over
    global game_screen
    global head_pos_x
    global head_pos_y
    global game_speed
    draw_ball()
    key = None

    while not game_over:
        game_screen.fill(SCREEN_COLOR)
        game_action(key)
        draw_pedals()
        draw_ball()
        draw_score()
        pygame.display.update()
        pygame.time.Clock().tick(game_speed)

        key = None
        for game_event in pygame.event.get():
            if game_event.type == KEYBOARD_PRESSED:
                if game_event.key == pygame.K_ESCAPE:
                    finish_game()
                else:
                    key = game_event.key
            elif game_event.type == pygame.QUIT:
                finish_game()


if __name__ == '__main__':
    try:
        init_game()
        play_game()
    except Exception as e:
        if tk_flag:
            msg = tkinter.Tk()
            msg.title('Pong Cather )-;')
            msg.geometry('300x1')
            tkinter.messagebox.showwarning('Pong Cather )-;', f'Unfortunately, the game has closed ({e})', parent=msg)
        else:
            print(f'Pong Cather - Unfortunately, the game has closed ({e})')
