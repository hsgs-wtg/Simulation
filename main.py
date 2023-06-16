# Import
import sys
from time import sleep
import pygame
from drone import Drone

pygame.init()

# Constants
WIDTH = 1000
HEIGHT = 700
BOARD_SIDE = 500
OFFSET_X = 50
OFFSET_Y = 50

COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

FPS = 30

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Get drone and terminal points
field_type = int(sys.argv[1])
picture = {
    1: "draw\\board1.png",
    2: "draw\\board2.png",
    3: "draw\\board3.png",
}

board = pygame.image.load(picture[field_type])

# Fix board
board_width = board.get_width()
board_height = board.get_height()

ratio_width = BOARD_SIDE / board_width
ratio_height = BOARD_SIDE / board_height

board = pygame.transform.scale(board, (BOARD_SIDE, BOARD_SIDE))

# Create the drone
drone = Drone(100, 100, 10,
              ((OFFSET_X, OFFSET_Y), (OFFSET_X + BOARD_SIDE, OFFSET_Y + BOARD_SIDE)),
              ratio_width, ratio_height
              )

delta_x = 1
delta_y = 0

drone.set_start_position(0, 0)
drone.set_movement(delta_x, delta_y)

def main_draw():
    screen.fill(COLOR_WHITE)
    screen.blit(board, (OFFSET_X, OFFSET_Y))

# Control loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if delta_x > -1:
                    delta_x -= 1
            if event.key == pygame.K_RIGHT:
                if delta_x < 1:
                    delta_x += 1
            if event.key == pygame.K_UP:
                if delta_y < 1:
                    delta_y += 1
            if event.key == pygame.K_DOWN:
                if delta_y > -1:
                    delta_y -= 1

            drone.set_movement(delta_x, delta_y)
            
    main_draw()
    drone.process()
    drone.draw(screen)

    pygame.display.update()

    sleep(1 / FPS)