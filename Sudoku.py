from email.mime import base
from itertools import count
from os import access
from threading import local
from webbrowser import BaseBrowser
from cv2 import resize
from numpy import diff
import pygame
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
import random
import collections
from PIL import Image


pygame.init()
pygame.font.init()
pygame.display.set_caption('SUDOKU')

BLACK = [0, 0, 0]
ORANGE = [255, 129, 0]
WHITE = [255, 255, 255]
DARK_GRAY = [180, 180, 180]
DODGERBLUE = [30, 144, 255]
VERY_DARK_GRAY = [36, 36, 36]
BLUE = [7, 51, 220]

N = 9

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
        pygame.draw.rect(self.window, BLACK, (self.OFFSET, self.OFFSET, self.width - 50, self.width - 50))

    def draw(self):
        sizeBtwn = (self.width - 50) // self.rows
        x = self.OFFSET
        y = self.OFFSET

        for l in range(self.rows + 1):		
            if l == 3 or l == 6:
                pygame.draw.line(self.window, DODGERBLUE, (x, self.OFFSET), (x, self.width - self.OFFSET), 3)
                pygame.draw.line(self.window, DODGERBLUE, (self.OFFSET, y), (self.width - self.OFFSET, y), 3)
            elif l != 0 or l != 9:
                pygame.draw.line(self.window, DODGERBLUE, (x, self.OFFSET), (x, self.width - self.OFFSET))
                pygame.draw.line(self.window, DODGERBLUE, (self.OFFSET, y), (self.width - self.OFFSET, y))
    
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
        self.font_color = WHITE

    def draw(self):
        if self.value == 0:
            text = self.font.render("", True, self.font_color)
        else:
            text = self.font.render(str(self.value), True, self.font_color)
        textRect = text.get_rect()
        # textRect.center = (self.pos_x, self.pos_y - 2)
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
        pygame.draw.rect(self.window, BLACK, (25, 525, self.width - 50, 50))

    def draw(self):

        # Inner Vertical Lines
        for i in range(1, 9):
            pygame.draw.line(self.window, DODGERBLUE, (25 + i * 50, 525), (25 + i * 50, 575))

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
        text = self.font.render(output, True, WHITE)      
        textRect = text.get_rect()
        textRect.center = (125, 640)
        self.window.blit(text, textRect)

        # Game pause
        if not self.game_state:
            game_info = "PLAY"
        else:
            game_info = "PAUSE"

        # pygame.draw.circle(self.window, ORANGE, (330, 640), 25)
        # pygame.draw.circle(self.window, ORANGE, (420, 640), 25)
        # pygame.draw.rect(self.window, ORANGE, (325, 615, 100, 50))
        # text = self.font.render(game_info, True, WHITE)      
        # textRect = text.get_rect()
        # textRect.center = (375, 640)
        # self.window.blit(text, textRect)

        # pause button
        pause_button = pygame.image.load('images/pause-button.png')
        pause_button_x, pause_button_y = 275, 610  
        self.window.blit(pause_button, (pause_button_x, pause_button_y))

        # stop button
        stop_button = pygame.image.load('images/stop-button.png')
        stop_button_x, stop_button_y = 350, 610  
        self.window.blit(stop_button, (stop_button_x, stop_button_y))


class InfoField(Field):
    def __init__(self, width, pos_x, pos_y, value, window, const_value, available):
        super().__init__(width, pos_x, pos_y, value, window, const_value)
        self.available = available
        self.quantity = 9
        if not self.available:
            self.font_color = DODGERBLUE
            self.background = VERY_DARK_GRAY
        else:
            self.font_color =  WHITE
            self.background = BLACK

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
            self.font_color =  WHITE
            self.background = BLACK
        else:
            self.available = False
            self.font_color = DODGERBLUE
            self.background = VERY_DARK_GRAY


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
            pygame.draw.rect(self.window, VERY_DARK_GRAY, (self.positions[self.pos_num][0], self.positions[self.pos_num][1], self.width, self.width))

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


class SudokuGenerator:
    def __init__(self, difficulty_level = 1):
        self.values_grid = []
        self.grid_to_solve = []
        self.empty_fields_positions = []
        self.number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.counter = 0
        self.size = 9
        self.difficulty_level = difficulty_level
        if self.algorithm():
            self.solvable = True
            self.prepare_grid()
        else:
            self.solvable = False

    # Fill the grid with zeros
    def initialize_grid(self):
        for _ in range(9):
            self.values_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Check if the grid is full
    def check_grid(self, row, col, value):
        for i in range(9):
            if self.values_grid[row][i] == value:
                return False

        for i in range(9):
            if self.values_grid[i][col] == value:
                return False

        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.values_grid[start_row + i][start_col + j] == value:
                    return False

        return True

    def prepare_grid(self):
        self.grid_to_solve = self.values_grid
        prepared_positions = False
        limit = 0
        if self.difficulty_level == 1:
            limit = 16
        elif self.difficulty_level == 2:
            limit = 32
        else:
            limit = 48
        count_positions = 0
        while not prepared_positions:
            if count_positions == limit:
                prepared_positions = True
            else:
                pos = random.randint(0,80)
                if pos not in self.empty_fields_positions:
                    self.empty_fields_positions.append(pos)
                    count_positions += 1
        # 3 Levels of difficulty
        # 80% filled - 64/81 fields filled - 17 empty
        # 60% filled - 48/81 fields filled - 33 empty
        # 40% filled - 32/81 fields filled - 49 empty
        # Clear random cells one by one - simultanously check if the grid is still solvable

    def fill_grid(self, row, col):
        # Check if it's already row = 8 and column = 9, if so -> stop bactracking
        if (row == self.size - 1 and col == self.size):
            return True
        # Check if this is the end of a row
        if col == self.size:
            row += 1
            col = 0
        # Check if the current cell has got any number greater than 0, if yes -> move to the next column
        if self.values_grid[row][col] > 0:
            return self.fill_grid(row, col + 1)
        # Shuffle available numbers to choose
        random.shuffle(self.number_list)
        for value in self.number_list:
            # Check if it is possible to insert this value
            if self.check_grid(row, col, value):
                # Assign value
                self.values_grid[row][col] = value

                if self.fill_grid(row, col + 1):
                    return True
            
            self.values_grid[row][col] = 0

        return False

    def compare_grid(self, actual_grid):
        for i in range(9):
            temp_values = [int(field.value) for field in actual_grid[i]]
            if not (collections.Counter(self.values_grid[i]) == collections.Counter(temp_values)):
                return False
        return True

    def draw_grid(self):
        for row in self.values_grid:
            print(row)

    def algorithm(self):
        self.initialize_grid()
        # row, col = self.find_next_empty()
        # print(row, col)
        if self.fill_grid(0, 0):
            return True
        else:
            return False


class Menu:
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.big_font = pygame.font.SysFont('arial', 30)
        self.small_font = pygame.font.SysFont('arial', 20)
        self.font_color = DODGERBLUE
        self.window = window
        self.difficulty = None

    def draw(self):
        sudoku_title = pygame.image.load('images/sudoku-title.png')
        sudoku_title_x, sudoku_title_y = 37, 100
        self.window.blit(sudoku_title, (sudoku_title_x, sudoku_title_y))

        # play button; area x: 218 - 282, y: 500 - 564
        play_button = pygame.image.load('images/play-button.png')
        play_button_x, play_button_y = 218, 500  
        self.window.blit(play_button, (play_button_x, play_button_y))

        # Image resizing
        basewidth = 300
        resized_add = "-resized.png"
        path = "images/level-title"
        
        try:    
            level_title = pygame.image.load('images/level-title-resized.png')
            level_title_x, level_title_y = 100, 200
            self.window.blit(level_title, (level_title_x, level_title_y))
        except FileNotFoundError:
            self.image_resize(path, basewidth)
            level_title = pygame.image.load('images/level-title-resized.png')
            level_title_x, level_title_y = 100, 200
            self.window.blit(level_title, (level_title_x, level_title_y))

        # 3 levels of difficulty to choose
        basewidth = 125
        paths = ["images/easy-level.png", "images/medium-level.png", "images/hard-level.png"]
        for i in range(3):
            level_name = pygame.image.load(paths[i])
            if i == 1:
                level_name_x, level_name_y = 50 + (i * 105), 300
            elif i == 0:
                level_name_x, level_name_y = 20 + (i * 150), 300
            else:
                level_name_x, level_name_y = 50 + (i * 150), 300
            self.window.blit(level_name, (level_name_x, level_name_y))

        pygame.draw.line(self.window, BLUE, (150, 320), (150, 350), 1)
        pygame.draw.line(self.window, BLUE, (350, 320), (350, 350), 1)
        
        # text = self.small_font.render(texts[3], True, self.font_color)
        # textRect = text.get_rect()
        # textRect.center = (118,350)
        # self.window.blit(text, textRect)

    def image_resize(self, name, basewidth):
        path = name + ".png"
        new_path = name + "-resized.png"
        img = Image.open(path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(new_path)

    def actions(self,  mouse_pos):
        play_cond1 = 282 >= mouse_pos[0] >= 218
        play_cond2 = 564 >= mouse_pos[1] >= 500
        easy_cond1 = 282 >= mouse_pos[0] >= 218
        easy_cond2 = 282 >= mouse_pos[1] >= 218
        medium_cond1 = 282 >= mouse_pos[0] >= 218
        medium_cond2 = 282 >= mouse_pos[1] >= 218
        hard_cond1 = 282 >= mouse_pos[0] >= 218
        hard_cond2 = 282 >= mouse_pos[1] >= 218

        if play_cond1 and play_cond2:
            return 2
        elif easy_cond1 and easy_cond2:
            self.difficulty = 1
            return 1
        elif medium_cond1 and medium_cond2:
            self.difficulty = 2
            return 1
        elif hard_cond1 and hard_cond2:
            self.difficulty = 3
            return 1
        else:
            return 0

class Game:
    def __init__(self):
        pass

class GameEnd:
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 30)
        self.font_color = DODGERBLUE
        self.window = window
        self.play_again_btn_pos = ()
        self.play_again_btn_size = ()
        self.exit_btn_pos = ()
        self.exit_btn_size = ()
        self.texts = []

    def create_text_object(self, content, pos):
        text = self.font.render(content, True, self.font_color)
        textRect = text.get_rect()
        textRect.center = pos
        self.window.blit(text, textRect)

    def draw(self):
        self.texts = ["CONGRATULATIONS", "FINISHED IN", "07:15",  "PLAY AGAIN", "EXIT"]

        self.create_text_object(self.texts[0], (self.width // 2, 100))
        self.create_text_object(self.texts[1], (self.width // 2, (self.height // 2) - 50))
        self.create_text_object(self.texts[2], (self.width // 2, (self.height // 2)))
        self.create_text_object(self.texts[3], ((self.width // 4) + 50, (self.height // 2) + 200))
        self.create_text_object(self.texts[4], ((self.width // 4) * 3, (self.height // 2) + 200))

        self.play_again_btn_size = self.font.size(self.texts[3])
        self.play_again_btn_pos += ((self.width // 4) + 50 - (self.play_again_btn_size[0] // 2), )
        self.play_again_btn_pos += ((self.height // 2) + 200 - (self.play_again_btn_size[1] // 2), )
        self.exit_btn_size = self.font.size(self.texts[4])
        self.exit_btn_pos += (((self.width // 4) * 3) - (self.exit_btn_size[0] // 2), )
        self.exit_btn_pos += ((self.height // 2) + 200 - (self.exit_btn_size[1] // 2), )

    def actions(self, mouse_pos):
        play_again_cond1 = self.play_again_btn_pos[0] + self.play_again_btn_size[0] >= mouse_pos[0] >= self.play_again_btn_pos[0]
        play_again_cond2 = self.play_again_btn_pos[1] + self.play_again_btn_size[1] >= mouse_pos[1] >= self.play_again_btn_pos[1]
        exit_cond1 = self.exit_btn_pos[0] + self.exit_btn_size[0] >= mouse_pos[0] >= self.exit_btn_pos[0]
        exit_cond2 = self.exit_btn_pos[1] + self.exit_btn_size[1] >= mouse_pos[0] >= self.exit_btn_pos[1]

        if play_again_cond1 and play_again_cond2:
            pass
        elif exit_cond1 and exit_cond2:
            pass


class PlayGame:
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
        self.filled_grid = None
        self.menu = None
        self.ending = None
        self.displayed_fields = []
        self.displayed_fields_row = 0
        self.displayed_fields_col = 0
        self.menu_actions = {}
        self.game_actions = {}
        self.ending_actions = {}
        # self.first_display_position = [0, 0]
        self.run()


    # SETTING UP GAME DISPLAY
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

    # OBJECT INITIALIZATION
    def initialize_menu(self):
        self.menu = Menu(self.width, self.height, self.window)
        self.menu_actions = {
            0: True,
            1: self.initialize_content(),
            2: False
        }
        
    def initialize_content(self):
        # self.menu = Menu(self.width, self.height, self.window)
        # self.ending = GameEnd(self.width, self.height, self.window)
        self.filled_grid = SudokuGenerator()
        self.grid = Grid(500, 50, 50, self.window)
        self.fields = []
        self.info_fields = []
        position = 0
        self.game_actions = {
            0: True,
            1: self.initialize_ending(),
            2: False
        }
        for i in range(self.grid.rows):
            whole_row = []
            for j in range(self.grid.cols):
                if self.filled_grid.solvable:
                    # print(self.filled_grid.values_grid[i][j])
                    if position in self.filled_grid.empty_fields_positions:
                        field = Field(50, ((j + 1) * 50), ((i + 1) * 50), 0, self.window, False)
                    else:
                        field = Field(50, ((j + 1) * 50), ((i + 1) * 50), self.filled_grid.values_grid[i][j], self.window, True)
                else:
                    field = Field(50, ((j + 1) * 50), ((i + 1) * 50), 0, self.window, False)
                position += 1
                whole_row.append(field)
            self.fields.append(whole_row)
        self.cursor = Cursor(50, 1, self.window, self.positions)
        self.info = Info(500, 50, 25, 525, self.window)
        for i in range(self.info.cols):
            info_field = InfoField(50, 50 * (i + 1), 550, i + 1, self.window, True, True)
            self.info_fields.append(info_field)

    def initialize_ending(self):
        self.ending = GameEnd(self.width, self.height, self.window)

    # REDRAWING CONTENT IN WINDOWS: MENU, GAME, ENDING
    def redraw_menu(self):
        self.window.fill(BLACK)
        self.menu.draw()
        pygame.display.update()

    def redraw_game_content(self):
        self.window.fill(BLACK)
        self.grid.draw_background()
        self.info.draw_background()
        self.info.draw()
        self.cursor.draw()
        self.grid.draw()
        self.displayed_fields.append((self.displayed_fields_col, self.displayed_fields_row))
        # Numbers to choose display
        for info_field in self.info_fields:
            info_field.draw()
        # Gradual grid display
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                if (j, i) in self.displayed_fields:
                    field.draw()
        
        if self.displayed_fields_col == 8 and self.displayed_fields_row < 8:
            self.displayed_fields_row += 1
            self.displayed_fields_col = 0
        elif self.displayed_fields_col < 8:
            self.displayed_fields_col += 1
        elif self.displayed_fields_col == 8 and self.displayed_fields_row == 8:
            # Regular grid display
            for i, row in enumerate(self.fields):
                for j, field in enumerate(row):
                    field.draw()
        
        self.info.draw()
        pygame.display.update()

    def redraw_ending(self):
        self.window.fill(BLACK)
        self.ending.draw()
        pygame.display.update()

    # ACTIONS HANDLER FOR THE "MAIN" WINDOW - ALL THE ACTIONS START HERE
    def menu_stage(self):
        # menu_actions = {
        #   0: nothing_happens,
        #   1: initialize_game (adding difficulty level),
        #   2: close_menu -> play game
        # }
        self.redraw_menu()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[0]:
                    output = self.menu.actions(pygame.mouse.get_pos())
                    if output in (0, 2):
                        return self.menu_actions[output]
                    elif output == 1:
                        self.menu_actions[output]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return False 
        return True

    # ACTIONS HANDLER FOR THE "GAME" WINDOW - ALL THE ACTIONS START HERE
    def game_stage(self):
        # game_actions = {
        #   0: nothing_happens,
        #   1: pause_game,
        #   2: end_game -> ending window,
        #   3: complete_game   
        # }
        self.redraw_game_content()
        self.quantity_check()
        if self.filled_grid.compare_grid(self.fields):
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[0]:
                    self.cursor.value_to_insert = 0
                    self.cursor.selected = True
                    pygame.display.update()
                    self.cursor.check_position(pygame.mouse.get_pos(), self.info_fields)
                    self.insert_value()
                elif pygame.mouse.get_pressed(3)[2]:
                    self.cursor.selected = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pass
        
        return True
        
    # ACTIONS HANDLER FOR THE "ENDING" WINDOW - ALL THE ACTIONS START HERE
    def end_game_stage(self):
        # ending_actions = {
        #   0: nothing_happens,
        #   1: play_again -> main window,
        #   2: exit -> close window
        # }
        self.redraw_ending()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False   
        return True

    # INSERTING VALUE INTO THE GRID
    def insert_value(self):
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
            if temp_pos == 0 and not self.fields[row][8].const_value:
                self.fields[row][8].value = self.cursor.value_to_insert
            elif not self.fields[row][temp_pos - 1].const_value:
                self.fields[row][temp_pos - 1].value = self.cursor.value_to_insert

    # CHECKING POSSIBLE VALUES TO INSERT
    def quantity_check(self):
        for info_field in self.info_fields:
            info_field.update_quantity(self.fields)

    # MAIN LOOP FOR THE WHOLE APPLICATION
    def run(self):
        self.display_setup()
        self.initialize_menu()
        running = True
        menu_opened = True
        game_running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(100)
            if menu_opened:
                menu_opened = self.menu_stage()
                # if not menu_opened:
                #     self.initialize_content()
                    # self.info.start_time = datetime.now()
            elif not menu_opened and game_running:
                game_running = self.game_stage()
                if not game_running:
                    self.initialize_ending()
            elif not game_running:
                running = self.end_game_stage()
        

if __name__ == "__main__":
    g = PlayGame()


