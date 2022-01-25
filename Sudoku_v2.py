import pygame
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

pygame.init()
pygame.font.init()
pygame.display.set_caption('SUDOKU')

BLACK = [0, 0, 0]
ORANGE = [255, 129, 0]
WHITE = [255, 255, 255]
DARK_GRAY = [180, 180, 180]

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

    def __init__(self, width, pos_x, pos_y, window):
        super().__init__(width, pos_x, pos_y)
        self.rows = self.cols = 9
        self.window = window

    def draw_background(self):
        pygame.draw.rect(self.window, WHITE, (self.OFFSET, self.OFFSET, self.width - 50, self.width - 50))

    def draw(self):
        sizeBtwn = (self.width - 50) // self.rows
        x = self.OFFSET
        y = self.OFFSET

        for l in range(self.rows + 1):		
            if l == 3 or l == 6:
                pygame.draw.line(self.window, ORANGE, (x, self.OFFSET), (x, self.width - self.OFFSET), 3)
                pygame.draw.line(self.window, ORANGE, (self.OFFSET, y), (self.width - self.OFFSET, y), 3)
            elif l != 0 or l != 9:
                pygame.draw.line(self.window, ORANGE, (x, self.OFFSET), (x, self.width - self.OFFSET))
                pygame.draw.line(self.window, ORANGE, (self.OFFSET, y), (self.width - self.OFFSET, y))
    
            x += sizeBtwn
            y += sizeBtwn

        pygame.draw.line(self.window, BLACK, (self.OFFSET, self.OFFSET), (self.OFFSET, self.width - self.OFFSET), 3)
        pygame.draw.line(self.window, BLACK, (self.OFFSET, self.OFFSET), (self.width - self.OFFSET, self.OFFSET), 3)
        pygame.draw.line(self.window, BLACK, (19 * self.OFFSET, self.OFFSET), (19*self.OFFSET, self.width - self.OFFSET), 3)
        pygame.draw.line(self.window, BLACK, (self.OFFSET, 19 * self.OFFSET), (self.width - self.OFFSET, 19 * self.OFFSET), 3)


# Each field has got only one position
class Field(Square):
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
        pygame.draw.rect(self.window, WHITE, (25, 525, self.width - 50, 50))

    def draw(self):

        # Inner Vertical Lines
        for i in range(1, 9):
            pygame.draw.line(self.window, ORANGE, (25 + i * 50, 525), (25 + i * 50, 575))

        # Horizontal lines
        pygame.draw.line(self.window, BLACK, (25, 525), (475, 525), 3)
        pygame.draw.line(self.window, BLACK, (25, 575), (475, 575), 3)
        # Outer Vertical lines
        pygame.draw.line(self.window, BLACK, (25, 525), (25, 575), 3)
        pygame.draw.line(self.window, BLACK, (475, 525), (475, 575), 3)

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
        text = self.font.render(output, True, BLACK)      
        textRect = text.get_rect()
        textRect.center = (125, 640)
        self.window.blit(text, textRect)

        # Game pause
        if not self.game_state:
            game_info = "PLAY"
        else:
            game_info = "PAUSE"

        pygame.draw.circle(self.window, ORANGE, (330, 640), 25)
        pygame.draw.circle(self.window, ORANGE, (420, 640), 25)
        pygame.draw.rect(self.window, ORANGE, (325, 615, 100, 50))
        text = self.font.render(game_info, True, WHITE)      
        textRect = text.get_rect()
        textRect.center = (375, 640)
        self.window.blit(text, textRect)


class InfoField(Field):
    def __init__(self, width, pos_x, pos_y, value, window, const_value, available):
        super().__init__(width, pos_x, pos_y, value, window, const_value)
        self.available = available
        self.quantity = 9
        if not self.available:
            self.font_color = ORANGE
            self.background = DARK_GRAY
        else:
            self.font_color =  BLACK
            self.background = WHITE

    def draw(self):
        pygame.draw.rect(self.window, self.background, (self.pos_x - 25, self.pos_y - 25, self.width, self.width))
        super().draw()

    def update_quantity(self, fields):
        count = 0
        for row in fields:
            for field in row:
                if field.value == self.value and self.value != 0:
                    count += 1
        self.quantity = 9 - count
        if self.quantity > 0:
            self.available = True
            self.font_color =  BLACK
            self.background = WHITE
        else:
            self.available = False
            self.font_color = ORANGE
            self.background = DARK_GRAY


# Reads the current value of the field, moves around the grid
class Cursor():
    def __init__(self, width, pos_num, window, positions):
        self.width = width
        self.pos_num = pos_num
        self.window = window
        self.positions = positions
        self.selected = False
        self.value_to_insert = 0

    def draw(self):
        if self.selected:
            pygame.draw.rect(self.window, DARK_GRAY, (self.positions[self.pos_num][0], self.positions[self.pos_num][1], self.width, self.width))

    def check_position(self, mouse_pos, info_fields):
        for key, value in self.positions.items():
            cond1 = mouse_pos[0] > value[0] and mouse_pos[0] < value[0] + 50
            cond2 = mouse_pos[1] > value[1] and mouse_pos[1] < value[1] + 50
            if cond1 and cond2 and key < 100:
                self.pos_num = key
            elif cond1 and cond2 and self.selected and key > 100:
                if info_fields[key - 101].available:
                    self.value_to_insert = key - 100

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
    def __init__(self, width = 500, height = 700):
        self.width = width
        self.height = height
        self.window = None
        self.grid = None
        self.fields = None
        self.info_fields = None
        self.cursor = None
        self.info = None
        self.positions = {}
        self.info_positions = {}
        self.delta = 0
        self.run()

    def display_setup(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('SUDOKU')
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill((255, 255, 255))
        pygame.display.flip()
        start_x = start_y = 25
        for i in range(1, 82):
            self.positions[i] = (start_x, start_y)
            if i % 9 == 0:
                start_y += 50
                start_x -= 400
            else:
                start_x += 50
        start_x = 25
        start_y = 525
        for i in range(101, 110):
            self.positions[i] = (start_x, start_y)
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
        if self.cursor.selected:
            self.cursor.move_cursor(self.delta)

    def insert_value(self):
        # self.cursor.pos_num
        # self.cursor.value_to_insert
        if self.cursor.value_to_insert != 0:
            temp_row = self.cursor.pos_num / 9
            if temp_row <= 1:
                row = 0
            elif 1 < temp_row <= 2:
                row = 1
            elif 2 < temp_row <= 3:
                row = 2
            elif 3 < temp_row <= 4:
                row = 3
            elif 4 < temp_row <= 5:
                row = 4
            elif 5 < temp_row <= 6:
                row = 5
            elif 6 < temp_row <= 7:
                row = 6
            elif 7 < temp_row <= 8:
                row = 7
            elif 8 < temp_row <= 9:
                row = 8
            temp_pos = self.cursor.pos_num % 9
            if temp_pos == 0:
                self.fields[8][row].value = self.cursor.value_to_insert
            else:
                self.fields[temp_pos - 1][row].value = self.cursor.value_to_insert

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        self.cursor.value_to_insert = 0
                        self.cursor.selected = True
                        pygame.display.update()
                        self.cursor.check_position(pygame.mouse.get_pos(), self.info_fields)
                        self.insert_value()
                        if self.cursor.value_to_insert != 0:
                            for info_field in self.info_fields:
                                info_field.update_quantity(self.fields)
                                print(f"Number: {info_field.value} | Quantity: {info_field.quantity} | Available: {info_field.available}")
                    elif pygame.mouse.get_pressed(3)[2]:
                        self.cursor.selected = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            pass
                if running == False:
                    pygame.quit()
                # self.user_actions()

if __name__ == "__main__":
    g = Game()


