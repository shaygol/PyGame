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
GAME_SPEED_START = 60
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_COLOR = colors.SEAGREEN4
PEDAL_1_LENGTH = SCREEN_HEIGHT // 4
PEDAL_1_WIDTH = SCREEN_WIDTH // 100
STEP_LENGTH = PEDAL_1_LENGTH
PEDAL_1_COLOR = colors.BLACK
BALL_COLOR = colors.BLACK
BALL_SIZE = 2 * PEDAL_1_LENGTH

# global variables
game_screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
game_over = None
game_speed = None
pedal_1_dir = None
head_pos_x = None
head_pos_y = None
pedal_1_pos_lst = None
is_space = None
pos_ball_x = SCREEN_HEIGHT // 2
pos_ball_y = SCREEN_WIDTH // 2
score = None


def draw_ball(rand_new=False):
    global pos_ball_x
    global pos_ball_y
    global BALL_COLOR
    global BALL_SIZE

    if rand_new:
        pos_ball_x = random.randint(10, SCREEN_WIDTH - 5)
        pos_ball_x -= pos_ball_x % PEDAL_1_LENGTH
        pos_ball_y = random.randint(10, SCREEN_HEIGHT - 5)
        pos_ball_y -= pos_ball_y % PEDAL_1_LENGTH
        while True:
            colo = colors.get_rand_color()
            ball_color = colo[0]
            ball_color_name = colo[1]
            if (ball_color != SCREEN_COLOR) and ('green' not in ball_color_name):
                break

        ball_size_factor = 2 * random.random() + 1
        BALL_SIZE = int(ball_size_factor * PEDAL_1_LENGTH)
        print(f'ball: ({pos_ball_x}, {pos_ball_y}), Size - {BALL_SIZE}, Color - {colo[1]}')

        pygame.draw.circle(game_screen, ball_color, center=(pos_ball_x, pos_ball_y), radius=BALL_SIZE)


def init_game():
    global game_over
    global game_speed
    global pedal_1_dir
    global head_pos_y
    global head_pos_y
    global pedal_1_pos_lst
    global game_screen
    global is_space
    global score

    game_over = False
    game_speed = GAME_SPEED_START
    pedal_1_dir = ''
    head_pos_x = 0
    head_pos_y = random.randint(SCREEN_HEIGHT // 2 - SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 2 + SCREEN_HEIGHT // 4)
    head_pos_y -= (head_pos_y % PEDAL_1_LENGTH)
    pedal_1_pos_lst = [(head_pos_x, head_pos_y)]  # list of tuples
    is_space = True
    score = 0
    draw_ball(True)


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

    for pos_tpl in pedal_1_pos_lst:
        #pygame.draw.circle(game_screen, color=PEDAL_1_COLOR, center=tuple(pos_tpl), radius=PEDAL_1_LENGTH)
        pygame.draw.rect(game_screen, ball_color, [pos_ball_x, pos_ball_y, BALL_SIZE, BALL_SIZE])

def game_action(key: pygame.key):
    global head_pos_x
    global head_pos_y
    global pedal_1_dir
    global pedal_1_pos_lst
    global is_space
    global game_speed
    global score
    tail = pedal_1_pos_lst[0]

    if (key == pygame.K_DOWN) and (pedal_1_dir != 'up'):
        pedal_1_dir = 'down'
    elif (key == pygame.K_UP) and (pedal_1_dir != 'down'):
        pedal_1_dir = 'up'
    elif key == pygame.K_s:
        is_space ^= 1
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

    for (pox, poy) in pedal_1_pos_lst:
        # check if the head hits part of the body
        if (pox, poy) == (head_pos_x, head_pos_y) and len(pedal_1_pos_lst) > 1:
            finish_game()
            return

        # check if the head hits the screen edges
        if (pox >= SCREEN_WIDTH) or (pox <= 0) or (poy >= SCREEN_HEIGHT) or (poy <= 0):
            finish_game()
            return

    pedal_1_pos_lst.append((head_pos_x, head_pos_y))
    if is_space:
        tail = pedal_1_pos_lst.pop(0)

    if (abs(head_pos_x - pos_ball_x) <= PEDAL_1_LENGTH) and (abs(head_pos_y - pos_ball_y) <= PEDAL_1_LENGTH):
        print(f'Head: ({head_pos_x}, {head_pos_y})\n')
        draw_ball(True)
        pedal_1_pos_lst.insert(0, tail)
        game_speed += 2
        score += 1


def play_game():
    global game_over
    global game_screen
    global head_pos_x
    global head_pos_y
    global game_speed
    draw_ball(True)
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
