import random

from board import Board


class ShipPlayer:
    def __init__(self, name):
        self.board_ships_own = Board()
        self.board_ships_own.place_ships()
        self.board_ships_targets = Board()
        self.name = name
        self.status = ''

    def print_field_mark(self, field_mark):
        print(f'Field mark by {self.name}: {field_mark}')

    def print_mark(self, field_mark, mark):
        print(f'{mark} for {field_mark} ({self.name})')

    def process_shot(self, board: Board):
        mark, ship = '', None
        while True:
            field_mark = input("Type field (A1 - J10)").upper().strip()
            try:
                mark, ship = board.get_shot(field_mark)
                break
            except ValueError:
                print('incorrect field value')
                continue
            except IndexError:
                print('incorrect field value')
                continue

        self.print_field_mark(field_mark)
        self.board_ships_targets.note_shot(mark, field_mark, ship)
        self.print_mark(field_mark, mark)
        if self.board_ships_targets.check_if_all_ships_sunk():
            self.status = 'win'
            print('all ships at bottom of the sea')

    @staticmethod
    def get_check_fields(ship_part):
        if len(ship_part) == 1:
            field = ship_part[0]
            return [(field[0] - 1, field[1]),
                    (field[0] + 1, field[1]),
                    (field[0], field[1] - 1),
                    (field[0], field[1] + 1)]
        else:
            field1 = ship_part[0]
            field2 = ship_part[1]
            if field1[0] == field2[0]:
                max_col = -1
                min_col = 10
                for field in ship_part:
                    if field[1] > max_col:
                        max_col = field[1]
                    if field[1] < min_col:
                        min_col = field[1]
                return [(field1[0], min_col - 1), (field1[0], max_col + 1)]
            else:
                max_row = -1
                min_row = 10
                for field in ship_part:
                    if field[0] > max_row:
                        max_row = field[0]
                    if field[0] < min_row:
                        min_row = field[0]
                return [(max_row + 1, field1[1]), (min_row - 1, field1[1])]

    def auto_process_shot(self, board: Board):
        col_board, row_board = -1, -1
        if self.status == 'ship_on_target':
            ship_part = []
            for last_row_board, last_col_board, last_field_mark, last_mark in \
                    self.board_ships_targets.shots_details[::-1]:
                if last_mark == 'hit not sunk':
                    ship_part.append((last_row_board, last_col_board))
                elif last_mark == 'hit and sunk':
                    break

            check_fields = self.get_check_fields(ship_part)
            for check_field_row, check_field_col in check_fields:
                if 0 <= check_field_row <= 9 and 0 <= check_field_col <= 9:
                    if (check_field_row, check_field_col) not in \
                            self.board_ships_targets.shots:
                        row_board = check_field_row
                        col_board = check_field_col
        else:
            while True:
                col_board = random.choice([i for i in range(10)])
                row_board = random.choice([i for i in range(10)])
                if (row_board, col_board) not in \
                        self.board_ships_targets.shots:
                    break

        field_mark = f'{self.board_ships_targets.col_marks[col_board]}' \
                     f'{str(row_board + 1)}'
        self.print_field_mark(field_mark)

        mark, ship = board.get_shot(field_mark)
        self.board_ships_targets.note_shot(mark, field_mark, ship)
        self.print_mark(field_mark, mark)

        if mark == 'hit not sunk':
            self.status = 'ship_on_target'
        elif mark == 'hit and sunk':
            self.status = 'ship_not_on_target'

        if self.board_ships_targets.check_if_all_ships_sunk():
            self.status = 'win'
            print('all ships at bottom of the sea')
