import random
import sys
from collections import deque
import gym
import pygame as pg

class Snek(gym.Env):
    NOP, LEFT, RIGHT, UP, DOWN = range(5)

    def __init__(self):
        self.width = 9
        self.height = 9
        self.scale = 16
        self.player = Player(self, (self.width // 2, self.height // 2))
        self.food = Food((random.randint(0, self.width - 1), random.randint(0, self.height - 1)))
        self.framerate = 20
        pg.init()
        pg.display.set_caption('Snek')
        self.screen = pg.display.set_mode((self.width * self.scale, self.height * self.scale))
        self.clock = pg.time.Clock()

    def step(self, action):
        state = {}
        reward = 0
        done = False
        info = {}

        # Pygame event handling (resolves some crashing)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.event.pump()

        if action == Snek.LEFT and self.player.dir != Player.DIR_RIGHT:
            self.player.dir = Player.DIR_LEFT
        if action == Snek.RIGHT and self.player.dir != Player.DIR_LEFT:
            self.player.dir = Player.DIR_RIGHT
        if action == Snek.UP and self.player.dir != Player.DIR_DOWN:
            self.player.dir = Player.DIR_UP
        if action == Snek.DOWN and self.player.dir != Player.DIR_UP:
            self.player.dir = Player.DIR_DOWN

        self.player.tick()
        if self.player.pos_x == self.food.pos_x and self.player.pos_y == self.food.pos_y:
            self.player.len += 1
            self.food.pos_x = random.randint(0, self.width - 1)
            self.food.pos_y = random.randint(0, self.height - 1)

        # Death
        if (self.player.pos_x, self.player.pos_y) in list(self.player.tail)[1:]:
            reward = -1
            done = True

        return state, reward, done, info

    def render(self, mode='human'):
        # Background
        pg.draw.rect(self.screen, (24, 24, 24),
                     (0, 0, self.width * self.scale, self.height * self.scale))

        for i, pos in enumerate(self.player.tail):
            pg.draw.rect(self.screen, (160 if i % 2 == 0 else 140, 24, 24),
                         (self.scale * pos[0], self.scale * pos[1], self.scale, self.scale))

        pg.draw.rect(self.screen, (24, 140, 24), (self.scale * self.food.pos_x,
                     self.scale * self.food.pos_y, self.scale, self.scale))

        pg.display.flip()
        self.clock.tick(int(self.framerate))

    def reset(self):
        self.player = Player(self, (self.width // 2, self.height // 2))
        self.food = Food((random.randint(0, self.width - 1), random.randint(0, self.height - 1)))
        return {}

class Player:
    DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN = range(4)

    def __init__(self, env, start_pos):
        self.pos_x, self.pos_y = start_pos
        self.dir = Player.DIR_DOWN
        self.tail = deque([start_pos])
        self.len = 1
        self.env = env

    def tick(self):
        if self.dir == Player.DIR_LEFT:
            self.pos_x = (self.pos_x - 1) % self.env.width
        if self.dir == Player.DIR_RIGHT:
            self.pos_x = (self.pos_x + 1) % self.env.width
        if self.dir == Player.DIR_UP:
            self.pos_y = (self.pos_y - 1) % self.env.height
        if self.dir == Player.DIR_DOWN:
            self.pos_y = (self.pos_y + 1) % self.env.height

        if len(self.tail) >= self.len:
            self.tail.pop()
        self.tail.appendleft((self.pos_x, self.pos_y))

class Food:
    def __init__(self, pos):
        self.pos_x, self.pos_y = pos
