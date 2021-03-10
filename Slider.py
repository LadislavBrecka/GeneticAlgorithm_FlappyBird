import pygame
from Constants import *


class Slider:
    def __init__(self, screen, posBarX=10, posBarY=5, width=200, height=10, colorBar=grey, colorSelector=blue, name='Slider'):
        self.screen = screen
        self.width  = width
        self.height = height
        self.name   = name
        self.selector = None
        self.colorBar = colorBar
        self.colorSelector = colorSelector
        self.r = height
        self.posBar = [posBarX, posBarY]
        self.posSelector = [self.posBar[0] + int(self.r / 2), self.posBar[1] + int(self.r / 2)]
        self.font = pygame.font.SysFont("monospace", 30)

    def DrawSlider(self):
        pygame.draw.rect(self.screen, self.colorBar, (self.posBar[0], self.posBar[1], self.width, self.height))
        self.selector = pygame.draw.circle(self.screen, self.colorSelector, (self.posSelector[0], self.posSelector[1]), self.r)

        label = self.font.render("Speed Slider", 1, (0, 0, 0))
        self.screen.blit(label, (self.posBar[0], self.posBar[1] - self.height * 4))

    def MoveSlider(self, posMouse):
        if posMouse is None:
            pass
        elif self.selector.collidepoint(posMouse):
            self.posSelector[0] = posMouse[0]

        if self.posSelector[0] > self.posBar[0] + self.width:
            self.posSelector[0] = self.posBar[0] + self.width

        if self.posSelector[0] < self.posBar[0]:
            self.posSelector[0] = self.posBar[0]

        selected = (self.posSelector[0] - self.posBar[0]) / self.width

        return selected





