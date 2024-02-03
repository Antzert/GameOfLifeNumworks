from ion import *
from math import ceil
from kandinsky import *
from random import getrandbits

class Game():
    def __init__(self, case_size):
        self.screen_size = (320, 222)
        self.size_of_case = case_size
        self.num_of_cases_in_x = ceil(self.screen_size[0] / self.size_of_case)
        self.num_of_cases_in_y = ceil(self.screen_size[1] / self.size_of_case)
        self.colors = {"gridColor": color(128, 128, 128), "cursorWhiteColor": color(200, 200, 200),"cursorBlackColor": color(50, 50, 50), "whiteColor": color(255, 255, 255), "blackColor": color(0, 0, 0)}
        self.map = [[False] * self.num_of_cases_in_y for _ in range(self.num_of_cases_in_x)]
        self.cursor = Cursor(self)
        self.main_loop()

    def main_loop(self):
        self.print_map()
        while True:
            self.cursor.print_cursor()
            event = True
            while event:
                if keydown(KEY_OK):
                    event = False
                    self.cursor.click()
                    while keydown(KEY_OK):continue
                elif keydown(KEY_BACKSPACE):
                    event = False
                    self.clear_map()
                    while keydown(KEY_BACKSPACE):continue
                elif keydown(KEY_EXE):
                    event = False
                    self.update_map()
                    while keydown(KEY_EXE):continue
                elif keydown(KEY_ANS):
                    event = False
                    self.random_map()
                    while keydown(KEY_ANS):continue
                elif keydown(KEY_UP):
                    event = False
                    self.cursor.move_up()
                    while keydown(KEY_UP):continue
                elif keydown(KEY_DOWN):
                    event = False
                    self.cursor.move_down()
                    while keydown(KEY_DOWN):continue
                elif keydown(KEY_LEFT):
                    event = False
                    self.cursor.move_left()
                    while keydown(KEY_LEFT):continue
                elif keydown(KEY_RIGHT):
                    event = False
                    self.cursor.move_right()
                    while keydown(KEY_RIGHT):continue

    def update_map(self):
        new_map = [[False] * len(self.map[0]) for _ in range(len(self.map))]
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                neighbors = self.count_neighbors(x, y)
                new_map[x][y] = (neighbors == 2 or neighbors == 3) if self.map[x][y] else neighbors == 3
        self.map = new_map
        self.print_map()

    def count_neighbors(self, x, y):
        count = 0
        rows, cols = len(self.map), len(self.map[0])

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_x, new_y = x + i, y + j
                if 0 <= new_x < rows and 0 <= new_y < cols:
                    count += self.map[new_x][new_y]

        return count

    def clear_map(self):
        self.map = [[False] * self.num_of_cases_in_y for _ in range(self.num_of_cases_in_x)]
        self.print_map()

    def random_map(self):
        for x in range(self.num_of_cases_in_x):
            for y in range(self.num_of_cases_in_y):
                self.map[x][y] = getrandbits(1)
        self.print_map()

    def print_map(self):
        for i in range(0, self.screen_size[0], self.size_of_case):
            fill_rect(i, 0, 1, self.screen_size[1], self.colors["gridColor"])
        for i in range(0, self.screen_size[1], self.size_of_case):
            fill_rect(0, i, self.screen_size[0], 1, self.colors["gridColor"])
        for x in range(self.num_of_cases_in_x):
            for y in range(self.num_of_cases_in_y):
                fill_rect(x * self.size_of_case + 1, y * self.size_of_case + 1, self.size_of_case - 1, self.size_of_case - 1,
                          self.colors["blackColor"] if self.map[x][y] else self.colors["whiteColor"])

class Cursor():
    def __init__(self, game):
        self.game = game
        self.location = [0, 0]

    def move_up(self):
        if self.location[1] != 0:
            self.reset_case()
            self.location[1] -= 1
        self.print_cursor()

    def move_down(self):
        if self.location[1] != self.game.num_of_cases_in_y - 1:
            self.reset_case()
            self.location[1] += 1
        self.print_cursor()

    def move_left(self):
        if self.location[0] != 0:
            self.reset_case()
            self.location[0] -= 1
        self.print_cursor()

    def move_right(self):
        if self.location[0] != self.game.num_of_cases_in_x - 1:
            self.reset_case()
            self.location[0] += 1
        self.print_cursor()

    def click(self):
        self.game.map[self.location[0]][self.location[1]] = not self.game.map[self.location[0]][self.location[1]]
        self.print_cursor()

    def reset_case(self):
        fill_rect(self.location[0] * self.game.size_of_case + 1, self.location[1] * self.game.size_of_case + 1,
                  self.game.size_of_case - 1, self.game.size_of_case - 1, self.game.colors["blackColor"] if
                  self.game.map[self.location[0]][self.location[1]] else self.game.colors["whiteColor"])

    def print_cursor(self):
        fill_rect(self.location[0] * self.game.size_of_case + 1, self.location[1] * self.game.size_of_case + 1,
                  self.game.size_of_case - 1, self.game.size_of_case - 1, self.game.colors["cursorBlackColor"] if
                  self.game.map[self.location[0]][self.location[1]] else self.game.colors["cursorWhiteColor"])

size_of_case = int(input("Taille des cases : "))
game = Game(size_of_case)
