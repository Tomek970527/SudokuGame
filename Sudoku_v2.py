import pygame
import time
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.font.init()
pygame.display.set_caption('SUDOKU')

class Grid:

    OFFSET = 25
    BLACK = [0, 0, 0]

    def __init__(self, width, pos_x, pos_y, window):
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rows = self.cols = 9
        self.window = window

    def create_grid(self, surface):
        sizeBtwn = (self.width - 50) // self.rows
        x = self.OFFSET
        y = self.OFFSET

        for l in range(self.rows + 1):		
            if l == 3 or l == 6:
                pygame.draw.line(surface, self.BLACK, (x, self.OFFSET), (x, self.width - self.OFFSET), 3)
                pygame.draw.line(surface, self.BLACK, (self.OFFSET, y), (self.width - self.OFFSET, y), 3)
            else:
                pygame.draw.line(surface, self.BLACK, (x, self.OFFSET), (x, self.width - self.OFFSET))
                pygame.draw.line(surface, self.BLACK, (self.OFFSET, y), (self.width - self.OFFSET, y))

            x += sizeBtwn
            y += sizeBtwn

        pygame.display.update()

class Field:

    BLACK = [0, 0, 0]

    def __init__(self, width, pos_x, pos_y, value):
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value
        self.font = pygame.font.SysFont('arial', 30)
        # print(pygame.font.get_fonts())

    def create_field(self, surface):
        if self.value == 0:
            text = self.font.render("2", True, self.BLACK)
        else:
            text = self.font.render(str(self.value), True, self.BLACK)
        textRect = text.get_rect()
        textRect.center = (self.pos_x, self.pos_y - 2)
        surface.blit(text, textRect)

        pygame.display.update()

class Info:
    def __init__(self, width, height, pos_x, pos_y):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y

    def create_info_field(self):
        pass

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = None
        self.grd = None
        self.flds = None
        self.run()

    def display_setup(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('SUDOKU')
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill((255, 255, 255))
        pygame.display.flip()

    def initialize_content(self):
        self.grd = Grid(500, 50, 50, self.window)
        self.flds = []
        for i in range(self.grd.rows):
            whole_row = []
            for j in range(self.grd.cols):
                fld = Field(50, ((i + 1) * 50), ((j + 1) * 50), 0)
                whole_row.append(fld)
            self.flds.append(whole_row)

    def redraw_content(self):
        self.grd.create_grid(self.window)
        for row in self.flds:
            for fld in row:
                fld.create_field(self.window)

    def user_actions(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -50
                self.dirny = 0
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 50
                self.dirny = 0
            else:
                self.dirnx = 0
                self.dirny = 0
                self.num = ""


    def run(self):
        self.display_setup()
        self.initialize_content()
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(10)
            self.redraw_content()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if running == False:
                    pygame.quit()
                self.user_actions()

if __name__ == "__main__":
    g = Game(500, 700)


