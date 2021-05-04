# %%

import pygame
import numpy as np
import time
import random
import pyaudio
import struct
import pyautogui  # to press a button to play the game
import pvporcupine
import threading
import asyncio
from multiprocessing.pool import ThreadPool
from multiprocessing import Process
import multiprocessing
from time import sleep

# %%

def collision_with_apple(apple_position, score):

    pygame.mixer.music.load("../Assets/eat.wav")
    # Setting the volume
    pygame.mixer.music.set_volume(0.7)
    # Start playing the song
    pygame.mixer.music.play()
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_position, score

def Player(Player_Avatar , PlayerX , PlayerY ):
    display.blit(Player_Avatar, (PlayerX, PlayerY))
def collision_with_boundaries(snake_head):

    # if the positions were bigger than display the player loses
    if snake_head[0] >= 500 or snake_head[0] < 0 or snake_head[1] >= 500 or snake_head[1] < 0:
        pygame.mixer.music.load("../Assets/death.wav")
        # Setting the volume
        pygame.mixer.music.set_volume(0.7)
        # Start playing the song
        pygame.mixer.music.play()
        return 1
    else:
        return 0


def collision_with_self(snake_position):

    # if the positions were the same the player loses
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        pygame.mixer.music.load("../Assets/death.wav")
        # Setting the volume
        pygame.mixer.music.set_volume(0.7)
        # Start playing the song
        pygame.mixer.music.play()
        return 1
    else:
        return 0


# %%

def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0] + current_direction_vector
    snake_head = snake_position[0]
    if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
        return 1
    else:
        return 0


# %%

def generate_snake(snake_head, snake_position, apple_position, button_direction, score):
    #to make the snake we use a vector and if the
    if button_direction == 1:
        snake_head[0] += 10
    elif button_direction == 0:
        snake_head[0] -= 10
    elif button_direction == 2:
        snake_head[1] += 10
    elif button_direction == 3:
        snake_head[1] -= 10
    else:
        pass

    if snake_head == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0, list(snake_head))

    else:
        snake_position.insert(0, list(snake_head))
        snake_position.pop()

    return snake_position, apple_position, score


# %%

def display_snake(snake_position):
    #to display boudneries and snake
    pygame.draw.line(display, purple, (0,0),(0,500) , 5 )
    pygame.draw.line(display, purple, (0, 0), (500, 0), 5)
    pygame.draw.line(display, purple, (500, 500), (0, 500), 5)
    pygame.draw.line(display, purple, (500, 500), (500, 0), 5)
    for position in snake_position:
        pygame.draw.rect(display, blue, pygame.Rect(position[0], position[1], 10, 10))


def display_apple(display, apple_position, apple):
    display.blit(apple, (apple_position[0], apple_position[1]))


# %%

def play_game(snake_head, snake_position, apple_position, button_direction, apple, score):
    crashed = False
    prev_button_direction = 1
    button_direction = 1
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    Player_Avatar = pygame.image.load("../Assets/Snake_Head.png")
    # when a key is press an event will happen and if the key was the right key snake will rotate

    while crashed is not True:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and prev_button_direction != 1:
                    if(prev_button_direction != 0):
                        pygame.mixer.music.load("../Assets/left_sound.wav")
                        # Setting the volume
                        pygame.mixer.music.set_volume(0.7)
                        # Start playing the song
                        pygame.mixer.music.play()
                        if (button_direction == 3):
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, 90)
                        else:
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, -90)

                    button_direction = 0


                elif event.key == pygame.K_RIGHT and prev_button_direction != 0:
                    if(prev_button_direction != 1):
                        pygame.mixer.music.load("../Assets/right_sound.wav")
                        # Setting the volume
                        pygame.mixer.music.set_volume(0.7)
                        # Start playing the song
                        pygame.mixer.music.play()
                        if (button_direction == 3):
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, -90)
                        else:
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, 90)
                    button_direction = 1


                elif event.key == pygame.K_UP and prev_button_direction != 2:
                    if(prev_button_direction != 3):
                        pygame.mixer.music.load("../Assets/up_sound.wav")
                        # Setting the volume
                        pygame.mixer.music.set_volume(0.7)
                        # Start playing the song
                        pygame.mixer.music.play()
                        if (button_direction == 1):
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, 90)
                        else:
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, -90)
                    button_direction = 3


                elif event.key == pygame.K_DOWN and prev_button_direction != 3:
                    if(prev_button_direction != 2):
                        pygame.mixer.music.load("../Assets/down_sound.wav")
                        # Setting the volume
                        pygame.mixer.music.set_volume(0.7)
                        # Start playing the song
                        pygame.mixer.music.play()
                        if (button_direction == 1):
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, -90)
                        else:
                            Player_Avatar = pygame.transform.rotate(Player_Avatar, 90)
                    button_direction = 2
                else:
                    button_direction = button_direction

        display.fill(window_color)
        display_apple(display, apple_position, apple)
        display_snake(snake_position)
        Player(Player_Avatar,snake_head[0],snake_head[1])
        snake_position, apple_position, score = generate_snake(snake_head, snake_position, apple_position,
                                                               button_direction, score)
        pygame.display.set_caption("Snake Game" + "  " + "SCORE: " + str(score))
        pygame.display.update()
        prev_button_direction = button_direction
        if is_direction_blocked(snake_position, current_direction_vector) == 1:
            crashed = True

        clock.tick(4)
    return score


# %%

def display_final_score(display_text):
    #display the score and wait for 2 sec
    largeText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf = largeText.render(display_text, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width / 2), (display_height / 2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
# %%

if __name__ == "__main__":
    ###### initialize required parameters ########
    display_width = 500
    display_height = 500
    green = (0, 255, 0)
    blue = (24, 123, 205)
    black = (0, 0, 0)
    purple=(170,6,255)
    window_color = (0, 171, 102)
    apple_image = pygame.image.load('../Assets/apple.png')
    clock = pygame.time.Clock()
    keyword_index=-1
    snake_head = [250, 250]
    snake_position = [[250, 250], [240, 250], [230, 250]]
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score = 0
    pygame.init()  # initialize pygame modules

    #### display game window #####
    Icon = pygame.image.load("../Assets/snake.png")
    pygame.display.set_icon(Icon)
    display = pygame.display.set_mode((display_width, display_height))
    display.fill(window_color)
    pygame.display.update()
    Game_Running=True
    display_text = 'Press Space to start the game '
    display_final_score(display_text)
    pygame.mixer.music.load("../Assets/Snake_song2.mp3")

    # Setting the volume
    pygame.mixer.music.set_volume(0.3)

    # Start playing the song
    pygame.mixer.music.play(-1)

    while Game_Running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                display = pygame.display.set_mode((display_width, display_height))
                display.fill(window_color)
                pygame.display.update()
                display_text = 'Your Score is: ' + str(0)
                display_final_score(display_text)
                pygame.quit()
            # if keystroke is pressed check the direction
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    Game_Running = False
                    pygame.mixer.music.stop()
    
    final_score = play_game(snake_head, snake_position, apple_position, 1, apple_image, score)
    display = pygame.display.set_mode((display_width, display_height))
    display.fill(window_color)
    pygame.display.update()

    display_text = 'Your Score is: ' + str(final_score)
    display_final_score(display_text)
    pygame.quit()
    f = open("tempScore.txt", "a")
    f.write(str(final_score))
    f.close()


# %%
