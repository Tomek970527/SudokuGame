import pygame
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

pygame.init()
pygame.font.init()
pygame.display.set_caption('SUDOKU')

class Square(ABC):
    def __init__(self, width, pos_x, pos_y):
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y

    @abstractmethod
    def draw(self):
        pass

class Grid(Square):

    OFFSET = 25
    BLACK = [0, 0, 0]
    ORANGE = [255, 129, 0]
    WHITE = [255, 255, 255]

    def __init__(self, width, pos_x, pos_y, window):
        super().__init__(width, pos_x, pos_y)
        self.rows = self.cols = 9
        self.window = window

    def draw_background(self):
        pygame.draw.rect(self.window, self.WHITE, (self.OFFSET, self.OFFSET, self.width - 50, self.width - 50))

    def draw(self):
        sizeBtwn = (self.width - 50) // self.rows
        x = self.OFFSET
        y = self.OFFSET

        for l in range(self.rows + 1):		
            if l == 3 or l == 6:
                pygame.draw.line(self.window, self.ORANGE, (x, self.OFFSET), (x, self.width - self.OFFSET), 3)
                pygame.draw.line(self.window, self.ORANGE, (self.OFFSET, y), (self.width - self.OFFSET, y), 3)
            elif l != 0 or l != 9:
                pygame.draw.line(self.window, self.ORANGE, (x, self.OFFSET), (x, self.width - self.OFFSET))
                pygame.draw.line(self.window, self.ORANGE, (self.OFFSET, y), (self.width - self.OFFSET, y))
    
            x += sizeBtwn
            y += sizeBtwn

        pygame.draw.line(self.window, self.BLACK, (self.OFFSET, self.OFFSET), (self.OFFSET, self.width - self.OFFSET), 3)
        pygame.draw.line(self.window, self.BLACK, (self.OFFSET, self.OFFSET), (self.width - self.OFFSET, self.OFFSET), 3)
        pygame.draw.line(self.window, self.BLACK, (19 * self.OFFSET, self.OFFSET), (19*self.OFFSET, self.width - self.OFFSET), 3)
        pygame.draw.line(self.window, self.BLACK, (self.OFFSET, 19 * self.OFFSET), (self.width - self.OFFSET, 19 * self.OFFSET), 3)


# Each field has got only one position
class Field(Square):

    BLACK = [0, 0, 0]

    def __init__(self, width, pos_x, pos_y, value, window, const_value):
        super().__init__(width, pos_x, pos_y)
        self.value = value
        self.font = pygame.font.SysFont('arial', 30)
        self.const_value = const_value
        self.window = window
        self.font_color = [0, 0, 0]

    def draw(self):
        if self.value == 0:
            text = self.font.render("", True, self.font_color)
        else:
            text = self.font.render(str(self.value), True, self.font_color)
        textRect = text.get_rect()
        textRect.center = (self.pos_x, self.pos_y - 2)
        self.window.blit(text, textRect)

        # pygame.display.update()

class Info(Grid):
    def __init__(self, width, height, pos_x, pos_y, window):
        super().__init__(width, pos_x, pos_y, window)
        self.height = height
        self.rows = 1
        self.start_time = datetime.now()
        self.font = pygame.font.SysFont('arial', 25)
        self.game_state = False

    def draw_background(self):
        pygame.draw.rect(self.window, self.WHITE, (25, 525, self.width - 50, 50))

    def draw(self):

        # Inner Vertical Lines
        for i in range(1, 9):
            pygame.draw.line(self.window, self.ORANGE, (25 + i * 50, 525), (25 + i * 50, 575))

        # Horizontal lines
        pygame.draw.line(self.window, self.BLACK, (25, 525), (475, 525), 3)
        pygame.draw.line(self.window, self.BLACK, (25, 575), (475, 575), 3)
        # Outer Vertical lines
        pygame.draw.line(self.window, self.BLACK, (25, 525), (25, 575), 3)
        pygame.draw.line(self.window, self.BLACK, (475, 525), (475, 575), 3)

        # Game timer
        current_time = datetime.now()
        time_delta = current_time - self.start_time
        minutes = int(round(time_delta.total_seconds() // 60, 0))
        seconds = int(round(((time_delta.total_seconds() / 60) - minutes) * 60, 0))
        if minutes < 10 and seconds < 10:
            output = f"0{minutes}:0{seconds}"
        elif minutes < 10 and seconds >= 10:
            output = f"0{minutes}:{seconds}"
        elif minutes >= 10 and seconds >= 10:
            output = f"{minutes}:{seconds}"
        elif minutes >= 10 and seconds < 10:
            output = f"{minutes}:0{seconds}"
        elif seconds == 60 and minutes < 10:
            output = f"0{minutes}:00"
        elif seconds == 60 and minutes >= 10:
            output = f"{minutes}:00"
        text = self.font.render(output, True, self.BLACK)      
        textRect = text.get_rect()
        textRect.center = (125, 640)
        self.window.blit(text, textRect)

        # Game pause
        if not self.game_state:
            game_info = "PLAY"
        else:
            game_info = "PAUSE"

        pygame.draw.circle(self.window, self.ORANGE, (330, 640), 25)
        pygame.draw.circle(self.window, self.ORANGE, (420, 640), 25)
        pygame.draw.rect(self.window, self.ORANGE, (325, 615, 100, 50))
        text = self.font.render(game_info, True, self.WHITE)      
        textRect = text.get_rect()
        textRect.center = (375, 640)
        self.window.blit(text, textRect)


class InfoField(Field):

    DARK_GRAY = [180, 180, 180]
    BLACK = [0, 0, 0]
    ORANGE = [255, 129, 0]
    WHITE = [255, 255, 255]

    def __init__(self, width, pos_x, pos_y, value, window, const_value, available):
        super().__init__(width, pos_x, pos_y, value, window, const_value)
        self.available = available
        self.quantity = 9
        if not self.available:
            self.font_color = self.ORANGE
            self.background = self.DARK_GRAY
        else:
            self.font_color =  self.BLACK
            self.background = self.WHITE

    def draw(self):
        pygame.draw.rect(self.window, self.background, (self.pos_x - 25, self.pos_y - 25, self.width, self.width))
        super().draw()


# Reads the current value of the field, moves around the grid
class Cursor():

    DARK_GRAY = [180, 180, 180]

    def __init__(self, width, pos_num, window, positions):
        self.width = width
        self.pos_num = pos_num
        self.window = window
        self.positions = positions

    def draw(self):
        pygame.draw.rect(self.window, self.DARK_GRAY, (self.positions[self.pos_num][0], self.positions[self.pos_num][1], self.width, self.width))

    def move_cursor(self, delta):
        if delta == 1 and self.pos_num % 9 != 0:
            self.pos_num += delta
        elif delta == -1 and self.pos_num % 9 != 1:
            self.pos_num += delta
        elif delta == 9 and self.pos_num < 73:
            self.pos_num += delta
        elif delta == -9 and self.pos_num > 9:
            self.pos_num += delta
        

class Game:

    LIGHT_BLUE = [52, 204, 255]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = None
        self.grid = None
        self.fields = None
        self.info_fields = None
        self.cursor = None
        self.info = None
        self.positions = {}
        self.run()

    def display_setup(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('SUDOKU')
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill((255, 255, 255))
        pygame.display.flip()
        start_x = start_y = 25
        for i in range(1,82):
            self.positions[i] = (start_x, start_y)
            if i % 9 == 0:
                start_y += 50
                start_x -= 400
            else:
                start_x += 50

    def initialize_content(self):
        self.grid = Grid(500, 50, 50, self.window)
        self.fields = []
        self.info_fields = []
        for i in range(self.grid.rows):
            whole_row = []
            for j in range(self.grid.cols):
                field = Field(50, ((i + 1) * 50), ((j + 1) * 50), 0, self.window, True)
                whole_row.append(field)
            self.fields.append(whole_row)
        self.cursor = Cursor(50, 1, self.window, self.positions)
        self.info = Info(500, 50, 25, 525, self.window)
        for i in range(self.info.cols):
            if i % 2:
                info_field = InfoField(50, 50 * (i + 1), 550, i + 1, self.window, True, False)
            else:
                info_field = InfoField(50, 50 * (i + 1), 550, i + 1, self.window, True, True)
            self.info_fields.append(info_field)

    def redraw_content(self):
        self.window.fill((211, 211, 211))
        self.grid.draw_background()
        self.info.draw_background()
        self.info.draw()
        self.cursor.draw()
        self.grid.draw()
        for i, row in enumerate(self.fields):
            self.info_fields[i].draw()
            for field in row:
                field.draw()
        self.info.draw()
        pygame.display.update()

    def user_actions(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.delta = -1
            elif keys[pygame.K_RIGHT]:
                self.delta = 1
            elif keys[pygame.K_UP]:
                self.delta = -9
            elif keys[pygame.K_DOWN]:
                self.delta = 9
            else:
                self.delta = 0
        self.cursor.move_cursor(self.delta)

    def run(self):
        self.display_setup()
        self.initialize_content()
        running = True
        clock = pygame.time.Clock()
        while running:
            pygame.time.delay(50)
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


