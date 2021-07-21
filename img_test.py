import os
import pygame
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('replay')
clock = pygame.time.Clock()

images = os.listdir('data_v1')
images.sort()


for i in range(len(images)):
    if '.png' in images[i]:
        screen.fill((0, 0, 0))
        img = pygame.image.load('data_v1/{}'.format(images[i]))
        screen.blit(img, (0, 0))
        data = images[i].split('_')
        pygame.draw.circle(screen, (255, 0, 0), (int(data[2]), int(data[1])), 10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    clock.tick(10)
