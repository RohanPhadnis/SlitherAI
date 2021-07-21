import random
import math
import time
import threading
import pygame
from pygame.locals import *
from PIL import Image
import numpy


pygame.init()
window = pygame.surface.Surface(size=[5000, 5000])
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('slither')
START_RAD = 10
START = time.time()
d = {}


class GameObj:

    def __init__(self, pos: list, color: tuple, rad: int = 5):
        self.pos = pos
        self.color = color
        self.rad = rad
        self.rect = None
        self.draw()

    def draw(self):
        self.rect = pygame.draw.circle(window, self.color, self.pos, self.rad)


class Food(GameObj):

    def __init__(self, pos: list = None, rad: int = 5, color: tuple = None):
        if color is None:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if pos is None:
            pos = [random.randint(0, window.get_width()), random.randint(0, window.get_height())]
        super().__init__(pos=pos, rad=rad, color=color)


class SnakeBod(GameObj):

    def __init__(self, pos: list, color: tuple = (0, 255, 0), rad: int = START_RAD):
        super().__init__(pos, color, rad)
        self.old_pos = self.pos.copy()

    def update_pos(self, new_pos: list):
        self.old_pos = self.pos.copy()
        self.pos = new_pos.copy()


class Snake:

    def __init__(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pos = [random.randint(0, window.get_width()), random.randint(0, window.get_height())]
        self.body = [SnakeBod(pos=[pos[0], pos[1] + n * 5], color=self.color) for n in range(10)]
        self.vel = [0, -1]
        self.mag = 1
        self.game_over = False
        self.boost_rate = 0.25
        self.boost_stamp = 0
        self.size = 300

    # def draw(self):
    #     for b in range(0, len(self.body), self.body[0].rad // 2):
    #         self.body[b].rad = len(self.body) // 100 + START_RAD
    #         self.body[b].draw()
    #     # pygame.draw.circle(window, (255, 255, 255), [self.body[0].pos[0] + self.vel[0], self.body[0].pos[1] + self.vel[1]], 5)
    #     pygame.draw.circle(window, (255, 255, 255), [self.body[0].pos[0] + 2 * self.vel[1], self.body[0].pos[1] - 2 * self.vel[0]], 7)
    #     pygame.draw.circle(window, (255, 255, 255), [self.body[0].pos[0] - 2 * self.vel[1], self.body[0].pos[1] + 2 * self.vel[0]], 7)
    #     self.size = 300 + 0.05 * len(self.body)

    def move(self):
        global foods
        if not self.game_over:
            self.motion()
            if len(self.body) <= 10:
                self.mag = 1
            self.body[0].update_pos([self.body[0].pos[0] + self.vel[0] * self.mag, self.body[0].pos[1] + self.vel[1] * self.mag])
            self.body[0].rad = len(self.body) // 100 + START_RAD
            self.body[0].draw()
            for b in range(1, len(self.body)):
                if self.body[b].pos != self.body[b-1].pos:
                    if self.mag == 1:
                        self.body[b].update_pos(self.body[b-1].old_pos)
                    else:
                        self.body[b].update_pos([(self.body[b-1].pos[0] + self.body[b-1].old_pos[0]) / 2, (self.body[b-1].pos[1] + self.body[b-1].old_pos[1]) / 2])
                self.body[b].rad = len(self.body) // 100 + START_RAD
                self.body[b].draw()
            pygame.draw.circle(window, (255, 255, 255),
                               [self.body[0].pos[0] + 2 * self.vel[1], self.body[0].pos[1] - 2 * self.vel[0]], 7)
            pygame.draw.circle(window, (255, 255, 255),
                               [self.body[0].pos[0] - 2 * self.vel[1], self.body[0].pos[1] + 2 * self.vel[0]], 7)
            self.size = 300 + 0.05 * len(self.body)
            if self.mag == 2 and time.time() - self.boost_stamp > self.boost_rate:
                foods.append(Food(pos=self.body[-1].pos, color=self.color))
                self.body.pop(len(self.body)-1)
                self.boost_stamp = time.time()
            if self.body[0].pos[0] > window.get_width() or self.body[0].pos[0] < 0 or self.body[0].pos[1] > window.get_height() or self.body[0].pos[1] < 0:
                self.die()

    def motion(self, **kwargs):
        pass

    def increase(self, num):
        for n in range(num):
            self.body.append(SnakeBod(pos=self.body[-1].old_pos, color=self.color))

    def die(self):
        global foods
        for b in range(0, len(self.body), self.body[0].rad // 2):
            foods.append(Food(rad=10, pos=self.body[b].pos.copy(), color=self.color))
        self.game_over = True


class SnakePlayer(Snake):

    def __init__(self):
        super().__init__()

    def motion(self, **kwargs):
        if len(kwargs) > 0:
            if kwargs['press']:
                self.mag = 2
            else:
                self.mag = 1
            x = kwargs['pos'][0] - 300
            y = kwargs['pos'][1] - 300
            hyp = math.sqrt(x**2 + y**2)
            self.vel = [x * 5 / hyp, y * 5 / hyp]


class SnakeBotV1(Snake):

    def __init__(self):
        super(SnakeBotV1, self).__init__()
        self.freq = 5
        self.stamp = 0

    def motion(self):
        if time.time() - self.stamp > self.freq:
            self.stamp = time.time()
            self.vel = [random.random() * 5]
            self.vel.append(math.sqrt(25 - self.vel[0] ** 2))
            self.mag = random.choice([1, 1, 2])
            self.vel[0] *= random.choice([1, -1])
            self.vel[1] *= random.choice([1, -1])


foods = [Food(rad=random.randint(1, 3)+5) for _ in range(window.get_width() // 5)]
snakes = [SnakeBotV1() for _ in range(window.get_width() // 50)]
vel = [1, 1]
mouse_pos = (0, 0)
boost = False
player = SnakePlayer()
started = False
hyp_calc = lambda pos1, pos2: math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def collisions():
    global foods, snakes, started, player

    while not player.game_over and len(snakes) > 0:
        if started:

            for f in foods:
                for s in snakes:
                    if s.body[0].rect.colliderect(f.rect) or hyp_calc(player.body[0].pos, f.pos) <= 20:
                        try:
                            foods.remove(f)
                        except ValueError:
                            pass
                        else:
                            foods.append(Food(rad=f.rad))
                            s.increase(f.rad - 5)

            for s1 in snakes:
                for s2 in snakes:
                    if s1 is not s2:
                        for b in range(0, len(s2.body), s2.body[0].rad // 2):
                            if s1.body[0].rect.colliderect(s2.body[b].rect):
                                s1.die()

            for s in snakes:
                if s.game_over:
                    snakes.remove(s)


def player_perspective():
    global foods, snakes, started, player
    while not player.game_over and len(snakes) > 0:
        if started:
            for f in foods:
                if player.body[0].rect.colliderect(f.rect) or hyp_calc(player.body[0].pos, f.pos) <= 20:
                    foods.remove(f)
                    foods.append(Food(rad=f.rad))
                    player.increase(f.rad - 5)
            for s1 in snakes:
                for b in range(0, len(player.body), START_RAD // 2):
                    if len(player.body) > b and len(s1.body) > 0 and s1.body[0].rect.colliderect(player.body[b].rect):
                        s1.die()
                for b in range(0, len(s1.body), s1.body[0].rad // 2):
                    if len(player.body) > 0 and len(s1.body) > b and player.body[0].rect.colliderect(s1.body[b].rect):
                        player.die()


def data_col():
    global d, snakes, labels
    while not player.game_over and len(snakes) > 0:
        if started:
            image = Image.fromarray(d['x'])
            image.save('data_v1/{}_{}_{}_{}.png'.format(d['stamp'], d['y'][0], d['y'][1], d['y'][2]))


other_thread = threading.Thread(target=collisions)
other_thread.start()
player_thread = threading.Thread(target=player_perspective)
player_thread.start()
data_thread = threading.Thread(target=data_col)
data_thread.start()

while not player.game_over and len(snakes) > 0:
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (255, 0, 0), (0, 0, window.get_width(), window.get_height()), 10)
    player.motion(press=boost, pos=mouse_pos)
    player.move()
    for f in foods:
        f.draw()
    for s in snakes:
        s.move()
    screen.fill((0, 0, 0))
    rect = [player.body[0].pos[0] - player.size, player.body[0].pos[1] - player.size, player.size * 2, player.size * 2]
    blit_pos = [0, 0]
    if rect[0] < 0:
        blit_pos[0] = abs(rect[0])
        rect[0] = 0
        rect[2] = player.size * 2
    if rect[1] < 0:
        blit_pos[1] = abs(rect[1])
        rect[1] = 0
        rect[3] = player.size * 2
    if rect[0] + rect[2] > window.get_width():
        blit_pos[0] = window.get_width() - (rect[0] + rect[2])
        rect[0] = window.get_width() - player.size * 2
        rect[2] = player.size * 2
    if rect[1] + rect[3] > window.get_height():
        blit_pos[1] = window.get_height() - (rect[1] + rect[3])
        rect[1] = window.get_height() - player.size * 2
        rect[3] = player.size * 2
    subsurf = pygame.transform.scale(pygame.Surface.subsurface(window, rect), (600, 600))
    screen.blit(subsurf, blit_pos)
    for event in pygame.event.get():
        if event.type == QUIT:
            player.die()
        elif event.type == MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                boost = True
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                boost = False
    pygame.display.update()
    d = {'x': pygame.surfarray.array3d(screen), 'y': [mouse_pos[0], mouse_pos[1], int(boost)],
         'stamp': int(time.time() * 100)}
    started = True
    if time.time() - START >= 120:
        player.die()
