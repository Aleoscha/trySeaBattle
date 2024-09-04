from db import DB
from ship import Ship

s = Ship()

log = [[],[]]

class move():
    def __init__(self) -> None:
        self.con = DB()

    def shot(self, player, X, Y): # player - игрок, который совершает ход
        if self.con.get_game_turn() == player:
            if self._isShip((player + 1) % 2, X, Y, game_mode=True):
                self.con.write_move(player, X, Y, 1)
                if self._are_ya_winning_son(player):
                    self.con.next_game_status(player)
                    print(player, 'Победил')

            else:
                self.con.write_move(player, X, Y, 0)
                # c_g_t = self.con.get_game_turn()
                self.con.next_game_turn()
                # print(f'{c_g_t} -> {self.con.get_game_turn()} : изменилась очередь')
                
        return 0

    def _isShip(self, player, X, Y, game_mode=False):
        '''
        Возвращает 1, если в ячейке находится корабль
        Иначе 0
        '''
        ships = self.con.get_ships_by_XY(player, X, Y)
        # print(ships)
        i = 0
        for ship in ships:
            x = ship[1]
            y = ship[2]
            axes = ship[3]
            ship_len = ship[4]
            i += 1  
            if axes == 0:
                if x == X and Y in range(y, y + ship_len):
                    if game_mode and self._is_sunk(ship, X, Y):
                        print('Пошел ко дну')

                    return 1
            else:
                if y == Y and X in range(x, x + ship_len):
                    if game_mode and self._is_sunk(ship, X, Y):
                        print('Пошел ко дну')

                    return 1
        return 0
    
    def _is_sunk(self, ship,  cur_x = 0, cur_y = 0):
        '''
        Потоплен ли корабль
        Передается корабль (player, X, Y, axis, len) и X, Y на которые происходит атака, т.к. в данный момент этот ход ещё не записан в БД
        '''
        player = ship[0]
        X = ship[1]
        Y = ship[2]
        axis = ship[3]
        ship_len = ship[4]

        moves = self.con.get_moves((player + 1) % 2)
        moves.append((player, cur_x, cur_y, 1, 0))
        # print("История ходов в теле is_sunk: ", moves)
        ship_cells = s.get_ship_cells(X, Y, axis, ship_len)

        for mov in moves:
            if (mov[1], mov[2]) in ship_cells: # mov[1], mov[2] == X, Y
                ship_cells.remove((mov[1], mov[2]))
        # print(ship_cells, 'after')

        if ship_cells != []:
            # print('Капитан, корабль на плаву! ', ship_cells)
            return 0
        else:
            # print('Капитан, корабль потоплен! ', ship_cells)
            self._fill_miss_gap(ship, moves)
            return 1
        
    def _fill_miss_gap(self, ship, moves):
        safety_cells = s.get_safety_zone(ship[1], ship[2], ship[3], ship[4])
        for move in moves:
            if (move[1], move[2]) in safety_cells:
                safety_cells.remove((move[1], move[2]))
                # print(safety_cells)
        for s_c in safety_cells:
            print((ship[0] + 1) % 2, s_c[0], s_c[1], 0)
            self.con.write_move((ship[0] + 1) % 2, s_c[0], s_c[1], 0)
            print(ship[0], s_c[0], s_c[1], 0)
        return 0
    


    def _are_ya_winning_son(self, player):
        if self.con.get_shots_on_target(player)[0] < 20:
            return False
        else:
            print('You are winning')
            return True



    
    def newgame(self):
        self.con.clear_moves()
        return 0
    
    def addShip(self, current_cell, previous_cell):
        coords = sorted([current_cell, previous_cell])
        # print(current_cell)
        axis = 0
        if coords[0][1] == coords[1][1]:
            ship_len = coords[1][2] - coords[0][2] + 1
        else:
            ship_len = coords[1][1] - coords[0][1] + 1
            axis = 1

        if not self._is_ships_near(coords[0][0], coords[0][1], coords[0][2], axis, ship_len) and self._is_correct_len(coords[0][0], ship_len):
            self.con.add_ship(coords[0][0], coords[0][1], coords[0][2], axis, ship_len)
        else:
            print('Невозможно добавить корабль!')
        # print(coords[0], axis, ship_len)

        return 0
    
    def _is_ships_near(self, player, X, Y, axis, ship_len):  #Проверяет наличие кораблей рядом с устанавливаемым кораблем
        ships = self.con.get_ships(player)
        safety_zone = s.get_safety_zone(X, Y, axis, ship_len)
        # print(safety_zone)
        for ship in ships:
            ship_cells = s.get_ship_cells(ship[1], ship[2], ship[3], ship[4])
            for ship_cell in ship_cells:
                if ship_cell in safety_zone:
                    # print((X, Y, axis, ship_len),ship_cell, ship)
                    return True
        return False
    
    def _is_correct_len(self, player, ship_len):
        example_lens = {1:4, 2:3, 3:2, 4:1}
        if ship_len > 4:
            return False
        ship_lens = self.con.get_ship_lens(player)
        # print(ship_lens, 'bla bla bla')
        if ship_len in ship_lens:
            if ship_lens[ship_len] < example_lens[ship_len]:
                # print(ship_lens[ship_len] < example_lens[ship_len], ship_lens[ship_len], example_lens[ship_len])
                return True
            else:
                # print(ship_lens[ship_len] < example_lens[ship_len], ship_lens[ship_len], example_lens[ship_len])
                return False
        else:
            # print(ship_len, ship_lens, example_lens)
            return True


m = move()
# m._is_ships_near(0, 3, 8 , 0, 1)
# m._is_correct_len(0, 1)
# m._is_sunk((1, 1, 1, 1, 1), 1, 1)
# ship = m.con.get_ships(1)[0]
# print(m._isShip(1, 6, 4))
# ship_cells = []

# for i in range(ship[4]):
#     if ship[3] == 1:
#         ship_cells.append((ship[1] + i, ship[2]))

# print(ship_cells)

# moves = m.con.get_moves(1)
# for mov in moves:
#     if (mov[1], mov[2]) in ship_cells:
#         ship_cells.remove((mov[1], mov[2]))

# print(ship_cells)

# print(moves, ' Все хооды')

# print(m._isSunk(ship))