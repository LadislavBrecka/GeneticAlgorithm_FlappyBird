import pygame
import sys
import os
import random
import math
from NeuralNetwork import NeuralNetwork
from Constants import *
from operator import attrgetter
import numpy as np
from Slider import Slider


def speed_slider(set_value, multiplicator):
    offset = 1 / multiplicator
    return (offset + set_value) * multiplicator


class Bird:
    ball_radius = 20
    jump_speed = gravity = 500
    travel_lenght = 3.5

    def __init__(self, brain=None):
        self.ball_x, self.ball_y = WIDTH / 8, HEIGHT / 2
        self.vert_speed = 0
        self.score = 0
        self.fitness = 0
        self.touch = False
        self.add_score = True
        self.position = 0
        self.distance = 0
        self.brain = NeuralNetwork(5, 10, 1, LEARNING_RATE)
        if brain is not None:
            self.brain.wih = brain.wih
            self.brain.who = brain.who

    def jump(self):
        self.vert_speed = self.jump_speed

    def draw(self, screen):
        pygame.draw.circle(screen, red, (int(self.ball_x), int(self.ball_y)), self.ball_radius)

    def update(self, delta_time, selected_value):
        self.ball_y -= self.vert_speed * delta_time * speed_slider(selected_value, SPEED_ORDER)
        self.vert_speed -= self.gravity * self.travel_lenght * delta_time * speed_slider(selected_value, SPEED_ORDER)
        self.distance += 1
        if self.vert_speed > 5000:
            self.vert_speed = 5000

        if self.vert_speed < -5000:
            self.vert_speed = -5000

    def think(self, inputs):
        answer = self.brain.query(inputs)
        if answer > 0.5:
            self.jump()


class FlappyGame:

    def __init__(self, population):
        # Defined constants and variables for physics, size of screen etc..
        self.size = WIDTH, HEIGHT
        self.tube_speed = 100
        self.tube_pos = 500
        self.tube_width = 80
        self.tube_space = 250
        self.half_space = self.tube_space / 2
        self.tube_gap = 400
        self.prevtime = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.highest_score = 0
        self.population = population
        # Generating initial population
        self.ball = [Bird() for i in range(population)]
        # Genereting list of tubes
        self.tubes = []
        self.tubes_count = 3
        for i in range(self.tubes_count):
            self.tubes.append(random.randint(self.tube_space / 2 + 50, HEIGHT - self.tube_space / 2 - 50))
        # List for saving all birds, even deleted until new generation
        self.saved_birds = []
        i = 0
        for bird in self.ball:
            bird.position = i
            # self.saved_birds.append(bird)
            self.saved_birds.insert(i, bird)
            i += 1
        # Setting up screen and gameloop
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.screen.set_alpha(None)
        self.my_font1 = pygame.font.SysFont("monospace", 30)
        self.screen.fill(light_blue)
        # Slider
        self.slider = Slider(self.screen, posBarY=HEIGHT-20)
        self.selected_value = 0

    def draw(self, posMouse):
        if len(self.ball):
            # Filling screen
            self.screen.fill(light_blue)

            # Ball drawing
            for bird in self.ball:
                bird.draw(self.screen)

            # Moving segments left
            for i in range(self.tubes_count):
                # k = self.tube_pos + self.tube_gap * (i + 1)
                k = self.tube_pos + self.tube_gap * i
                if (k + self.tube_width > 0) and (k < WIDTH):
                    pygame.draw.rect(self.screen, green, (k, 0, self.tube_width,
                                     self.tubes[i] - self.half_space))
                    pygame.draw.rect(self.screen, green, (k, self.tubes[i] + self.half_space,
                                     self.tube_width, HEIGHT - self.tubes[i] - self.half_space))

            # Slider stuff
            self.slider.DrawSlider()
            self.selected_value = self.slider.MoveSlider(posMouse)

            # Displaying score
            score = max(bird.score for bird in self.ball)
            if score > self.highest_score:
                self.highest_score = score

            label1 = self.my_font1.render("Your score is %d" % score, 1, (0, 0, 0))
            label2 = self.my_font1.render("Highest score is %d" % self.highest_score, 1, (0, 0, 0))
            self.screen.blit(label1, (1, 1))
            self.screen.blit(label2, (WIDTH/2, 1))

    def update(self, time):
        if len(self.ball):
            # Computing delta time between frames
            delta_time = time - self.prevtime
            delta_time /= 1000

            # HERE GO CODE FOR GAME LOGIC
            for bird in self.ball:
                # Calibrating bird distance in term of distence to pipe
                x, i = self.nearest_pipe()
                gap = x - self.saved_birds[0].ball_x
                bird.distance -= gap
                bird.update(delta_time, self.selected_value)
                self.saved_birds[bird.position] = bird

            self.tube_pos -= self.tube_speed * delta_time * speed_slider(self.selected_value, SPEED_ORDER)

            # If statements for exceeding screen size
            # For x axis
            if self.tube_pos + self.tube_width < 0:  # constant is multiply of x_pos + width of tube
                del self.tubes[0]
                self.tubes.append(random.randint(self.half_space + 50, HEIGHT - self.half_space - 50))
                self.tube_pos += self.tube_gap
                for bird in self.ball:
                    bird.add_score = True

            # Deleting collided balls
            self.ball[:] = [bird for bird in self.ball if not bird.touch]

            # Saving time for computing delta time (frame lasting)
            self.prevtime = time
            # Updating display
            pygame.display.update()

        else:
            self.reset()

    def reset(self):
        # Clearing ball list, should be already empty
        self.ball = []

        # Here goes function for creating new birds derivated from previous
        self.ball = self.generate_new_pop()

        # Reseting list for saving all birds
        self.saved_birds = []
        i = 0
        for bird in self.ball:
            bird.position = i
            # self.saved_birds.append(bird)
            self.saved_birds.insert(i, bird)
            i += 1

        # Reseting position of tubes
        self.tube_pos = 500
        self.tubes = []
        for i in range(self.tubes_count):
            self.tubes.append(random.randint(self.tube_space / 2 + 50, HEIGHT - self.tube_space / 2 - 50))

        # New prevtime update
        self.prevtime = pygame.time.get_ticks()

    # Function, which calculate x and y coordinate of the nearest tube
    def nearest_pipe(self):
        if len(self.saved_birds):
            bird_x = self.saved_birds[0].ball_x
            pipe_pos = 0
            y = self.tubes[pipe_pos]
            x = self.tube_pos
            if x < bird_x:
                pipe_pos = 1
                y = self.tubes[pipe_pos]
                x = self.tube_pos + self.tube_gap
            return x, pipe_pos

    # Collision detection with tubes
    def collision(self):
        if len(self.ball):
            insquare = int(math.sqrt(2) * self.ball[0].ball_radius)

            for bird in self.ball:
                bird_x = bird.ball_x
                # Y smaller than screen
                if bird.ball_y < 0:
                    bird.touch = True
                    continue

                # Y larger than screen
                elif bird.ball_y > HEIGHT:
                    bird.touch = True
                    continue

                # Ball collide with pipes
                radius = bird.ball_radius - 2
                if ((bird_x + radius > self.tube_pos) and (bird_x + radius < self.tube_pos + self.tube_width)) or\
                   ((bird_x - radius > self.tube_pos) and (bird_x - radius < self.tube_pos + self.tube_width)):
                    if (bird.ball_y - radius < self.tubes[0] - self.half_space) or\
                       (bird.ball_y + radius > self.tubes[0] + self.half_space) or \
                       (bird.ball_y + radius < self.tubes[0] - self.half_space) or \
                       (bird.ball_y - radius > self.tubes[0] + self.half_space):
                        # There was a touch
                        bird.touch = True
                        continue

                # There wasnt a touch, so add to score
                if bird_x > self.tube_pos + self.tube_width and bird.add_score:
                    bird.score += 1
                    bird.add_score = False

        return len(self.ball)

# GA stuff, selecting the best bird for reproduction ######

    # Ruletta algorithm
    def pick_one(self):
        index = 0
        r = np.random.rand()
        while r > 0:
            r = r - self.saved_birds[index].fitness
            index += 1
        index -= 1
        bird = self.saved_birds[index]
        child = Bird(bird.brain)
        child.brain.mutate()
        return child

    # Function for calculating fitness value for birds
    def calculate_fitness(self):
        FitnessSum = 0
        for bird in self.saved_birds:
            FitnessSum += bird.distance

        for bird in self.saved_birds:
            if bird.fitness != 0:
                bird.fitness = 0
            bird.fitness = bird.distance / FitnessSum

    # Function for creating new generation of birds
    def generate_new_pop(self):
        new_birds = []
        self.calculate_fitness()
        
        random_population = random.uniform(RANDOMNESS[0], RANDOMNESS[1])
        random_population = int(random_population * self.population)

        for i in range(self.population - random_population):
            new_birds.insert(i, self.pick_one())

        for i in range(random_population):
            new_birds.insert(random.randint(0, self.population), Bird())

        return new_birds
