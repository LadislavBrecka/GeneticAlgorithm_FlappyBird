from Flappy_class import FlappyGame, Bird
from NeuralNetwork import NeuralNetwork
import pygame
import sys
import numpy as np
from Constants import *

f = FlappyGame(POPULATION)

gameloop = True
time = pygame.time.get_ticks()
f.update(time)
new_pop = POPULATION
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN])

posMouse = None

# Game Loop
while gameloop:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                f.ball[0].jump()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                posMouse = pygame.mouse.get_pos()

    # Neural Network stuff
    if new_pop:
        temp = f.nearest_pipe()
        npipe_x = temp[0]
        j = temp[1]
        pipe_x = (npipe_x / WIDTH) * 0.99 + 0.01
        pipe_y1 = ((f.tubes[j] - f.half_space) / HEIGHT) * 0.99 + 0.01
        pipe_y2 = ((f.tubes[j] + f.half_space) / HEIGHT) * 0.99 + 0.01

        for i in range(new_pop):
            direction = (f.ball[i].vert_speed / 5000) * 0.99 + 0.01
            ball_y = (f.ball[i].ball_y / HEIGHT) * 0.99 + 0.01
            inputs = [ball_y, pipe_x, direction, pipe_y1, pipe_y2]
            f.ball[i].think(inputs)

    # Game sequence
    f.update(time)
    new_pop = f.collision()
    # print(new_pop)
    f.draw(posMouse)


