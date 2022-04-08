import random

import questionary


class Board:
    def __init__(self):
        self.empty_char = 'O'
        self.nk_char = '-'
        self.ship_char = 'X'
        self.board = [[self.nk_char for _ in range(10)] for _ in range(10)]

        self.ships = []
        self.ships_sink = []
        self.shots = []
        self.shots_details = []
        self.not_empty_fields = []
        self.col_marks = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.row_marks = [str(i) for i in range(1, 11)]
        self.ships_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    @staticmethod
    def insert_spaces(txt_list):
        return ' '.join(txt_list)

    def print_board(self):
        questionary.print(f'{" " * 3}{self.insert_spaces(self.col_marks)}',
                          style="fg:blue")
        for i, row in enumerate(self.board):
            questionary.print(f'{self.row_marks[i].ljust(3)}', end='',
                              style="fg:blue")
            for char in self.insert_spaces(row):
                if char == self.empty_char:
                    questionary.print(f'{char}', end='', style="fg:red")
                elif char == self.ship_char:
                    questionary.print(f'{char}', end='', style="fg:green")
                else:
                    questionary.print(f'{char}', end='')
            questionary.print('')

    def place_ships(self):
        for ship in self.ships_sizes:
            self.place_ship(ship)

    def place_ship(self, ship_size):
        directions = ['up', 'down', 'left', 'right']
        random.shuffle(directions)
        while True:
            col = random.choice([i for i in range(10)])
            row = random.choice([i for i in range(10)])

            if (row, col) in self.not_empty_fields:
                continue

            ship_placed = False
            direction = ''
            for direction in directions:
                if direction == 'up':
                    if row - ship_size + 1 >= 0:
                        ready_to_place = True
                        for i in range(ship_size):
                            if (row - i, col) in self.not_empty_fields:
                                ready_to_place = False
                        if not ready_to_place:
                            continue
                        ship_fields = []
                        for i in range(ship_size):
                            self.board[row - i][col] = self.ship_char
                            ship_fields.append((row - i, col))
                        self.ships.append(ship_fields)
                        ship_placed = True
                        break
                    else:
                        continue
                elif direction == 'down':
                    if row + ship_size <= 10:
                        ready_to_place = True
                        for i in range(ship_size):
                            if (row + i, col) in self.not_empty_fields:
                                ready_to_place = False
                        if not ready_to_place:
                            continue
                        ship_fields = []
                        for i in range(ship_size):
                            self.board[row + i][col] = self.ship_char
                            ship_fields.append((row + i, col))
                        self.ships.append(ship_fields)
                        ship_placed = True
                        break
                    else:
                        continue
                elif direction == 'left':
                    if col - ship_size + 1 >= 0:
                        ready_to_place = True
                        for i in range(ship_size):
                            if (row, col - i) in self.not_empty_fields:
                                ready_to_place = False
                        if not ready_to_place:
                            continue
                        ship_fields = []
                        for i in range(ship_size):
                            self.board[row][col - i] = self.ship_char
                            ship_fields.append((row, col - i))
                        self.ships.append(ship_fields)
                        ship_placed = True
                        break
                    else:
                        continue
                elif direction == 'right':
                    if col + ship_size <= 10:
                        ready_to_place = True
                        for i in range(ship_size):
                            if (row, col + i) in self.not_empty_fields:
                                ready_to_place = False
                        if not ready_to_place:
                            continue
                        ship_fields = []
                        for i in range(ship_size):
                            self.board[row][col + i] = self.ship_char
                            ship_fields.append((row, col + i))
                        self.ships.append(ship_fields)
                        ship_placed = True
                        break
                    else:
                        continue
            if ship_placed:
                self.update_not_empty_fields(row, col, ship_size, direction)
                break

    def update_not_empty_fields(self, row, col, ship_size, direction):
        if direction == 'up':
            for row_diff in range(row - ship_size, row + 2):
                for col_diff in range(col - 1, col + 2):
                    self.not_empty_fields.append((row_diff, col_diff))
        elif direction == 'down':
            for row_diff in range(row - 1, row + ship_size + 1):
                for col_diff in range(col - 1, col + 2):
                    self.not_empty_fields.append((row_diff, col_diff))
        elif direction == 'left':
            for row_diff in range(row - 1, row + 2):
                for col_diff in range(col - ship_size, col + 2):
                    self.not_empty_fields.append((row_diff, col_diff))
        elif direction == 'right':
            for row_diff in range(row - 1, row + 2):
                for col_diff in range(col - 1, col + ship_size + 1):
                    self.not_empty_fields.append((row_diff, col_diff))

    def get_field_row_col(self, field_mark):
        col_field = self.col_marks.index(field_mark[0])
        row_field = int(field_mark[1:]) - 1
        if row_field > 9 or row_field < 0:
            raise ValueError
        return row_field, col_field

    def get_shot(self, field_mark):
        row_board, col_board = self.get_field_row_col(field_mark)
        self.shots.append((row_board, col_board))
        if self.check_if_hit(row_board, col_board):
            ship = self.get_ship_for_row_col(row_board, col_board)
            if self.check_if_sink(ship):
                self.ships_sink.append(ship)
                return 'hit and sunk', ship
            else:
                return 'hit not sunk', None
        else:
            return 'mishit', None

    def note_shot(self, mark, field_mark, ship):
        row_board, col_board = self.get_field_row_col(field_mark)
        self.shots.append((row_board, col_board))
        self.shots_details.append((row_board, col_board, field_mark, mark))
        if mark == 'mishit':
            self.board[row_board][col_board] = self.empty_char
        elif mark == 'hit and sunk':
            self.board[row_board][col_board] = self.ship_char
            self.ships_sink.append(ship)
            self.mark_empty_around_ship(ship)
        elif mark == 'hit not sunk':
            self.board[row_board][col_board] = self.ship_char

    def get_ship_for_row_col(self, row_board, col_board):
        for ship in self.ships:
            if (row_board, col_board) in ship:
                return ship

    def check_if_hit(self, row_board, col_board):
        return self.board[row_board][col_board] == self.ship_char

    def check_if_sink(self, ship):
        for row_ship, col_ship in ship:
            if (row_ship, col_ship) not in self.shots:
                return False
        return True

    def check_if_all_ships_sunk(self):
        return len(self.ships_sizes) == len(self.ships_sink)

    def mark_empty_around_ship(self, ship):
        for field_ship in ship:
            for i in range(field_ship[0] - 1, field_ship[0] + 2):
                for j in range(field_ship[1] - 1, field_ship[1] + 2):
                    if (i, j) not in ship:
                        if 0 <= i <= 9 and 0 <= j <= 9:
                            self.board[i][j] = self.empty_char
                            self.shots.append((i, j))
