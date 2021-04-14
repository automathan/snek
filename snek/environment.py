import random
import sys
from collections import deque
import gym
from gym import spaces
import numpy as np
import pygame as pg

class Snek(gym.Env):
    NOP, LEFT, RIGHT, UP, DOWN = range(5)

    def __init__(self):
        self.width = 15
        self.height = 15
        self.scale = 16
        self.player = Player((self.width // 2, self.height // 2))
        self.framerate = 2
        pg.init()
        self.screen = pg.display.set_mode((self.width * self.scale, self.height * self.scale))
        self.clock = pg.time.Clock()
            
    def step(self, action):
        # Pygame event handling (resolves some crashing)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.event.pump()
        
        if action == Snek.LEFT:
            self.player.dir = Player.DIR_LEFT
        if action == Snek.RIGHT:
            self.player.dir = Player.DIR_RIGHT
        if action == Snek.UP:
            self.player.dir = Player.DIR_UP
        if action == Snek.DOWN:
            self.player.dir = Player.DIR_DOWN
            
        self.player.tick()

        state = {}
        reward = 0
        done = False
        info = {}

        return state, reward, done, info

    def render(self, mode='human'):
        # Background
        pg.draw.rect(self.screen, (24, 24, 24), (0, 0, self.width * self.scale, self.height * self.scale))
        i = 120
        for pos in self.player.tail:
            pg.draw.rect(self.screen, (i, 24, 24), (self.scale * pos[0], self.scale * pos[1], self.scale, self.scale))
            i += 20
        pg.display.flip()
        self.clock.tick(int(self.framerate))

    def reset(self):
        pass

class Player:
    DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN = range(4)

    def __init__(self, start_pos):
        self.pos_x, self.pos_y = start_pos
        self.dir = Player.DIR_DOWN
        self.tail = deque([start_pos])
        self.len = 5

    def tick(self):
        if self.dir == Player.DIR_LEFT:
            self.pos_x -= 1
        if self.dir == Player.DIR_RIGHT:
            self.pos_x += 1
        if self.dir == Player.DIR_UP:
            self.pos_y -= 1
        if self.dir == Player.DIR_DOWN:
            self.pos_y += 1
        
        if len(self.tail) >= self.len:
            self.tail.pop()
        self.tail.appendleft((self.pos_x, self.pos_y))
        print(self.tail)
            
