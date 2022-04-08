import sys

from shipplayer import ShipPlayer

if __name__ == '__main__':
    name = input("Type your name: ").strip()
    sp = ShipPlayer(name)
    sp_comp = ShipPlayer('Computer')
    separator = '#' * 22
    try:
        while True:
            print(separator)

            # check if any player has already won
            for player in [sp, sp_comp]:
                if player.status == 'win':
                    print(f'{player.name} has won!')
                    print(separator)
                    print(f'ships for {sp.name}:')
                    sp.board_ships_own.print_board()
                    print(f'ships for {sp_comp.name}:')
                    sp_comp.board_ships_own.print_board()
                    sys.exit(1)

            sp_comp.auto_process_shot(sp.board_ships_own)
            sp_comp.board_ships_targets.print_board()
            print(separator)
            sp.process_shot(sp_comp.board_ships_own)
            sp.board_ships_targets.print_board()
    except KeyboardInterrupt:
        print('\n##########')
        print('Thank you')
        print('##########')
        sys.exit(1)
