from db import DB

log = []

class move():
    def __init__(self) -> None:
        self.con = DB()

    def shot(self, player, X, Y): # player - игрок, который совершает ход
        if self._isShip((player + 1) % 2, X, Y):
            self.con.write_move(player, X, Y, 1)
        else:
            self.con.write_move(player, X, Y, 0)
        return 0

    def _isShip(self, player, X, Y):
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
            # print(i, ship)
            if axes == 0:
                if x == X and Y in range(y, y + ship_len):
                    return 1
            else:
                if y == Y and X in range(x, x + ship_len):
                    return 1
        return 0
    
    def _isSunk(self, player, ship):
        '''
        Проверяет потоплен ли корабль

        '''
        moves = self.con.get_moves(player)
        ship_cells = []

        for i in range(ship[4]):
            if ship[3] == 1: # ship[3] == axes
                ship_cells.append((ship[1] + i, ship[2])) # ship[1], ship[2] == X, Y
            else:
                ship_cells.append((ship[1], ship[2] + i)) # ship[1], ship[2] == X, Y

        moves = m.con.get_moves(1) # Можно сделать moves by x, y, axes и сократить количество итераций до макс 10
        for mov in moves:
            if (mov[1], mov[2]) in ship_cells: # mov[1], mov[2] == X, Y
                ship_cells.remove((mov[1], mov[2]))
        
        if ship_cells == []:
            return True
        
        else:
            return False
    
    def newgame(self):
        self.con.clear_moves()
        return 0
    
    def addShip(self, current_cell, previous_cell):
        coords = sorted([current_cell, previous_cell])

        axis = 0
        if coords[0][1] == coords[1][1]:
            ship_len = coords[1][2] - coords[0][2] + 1
        else:
            ship_len = coords[1][1] - coords[0][1] + 1
            axis = 1
        self.con.add_ship(0, coords[0][1], coords[0][2], axis, ship_len)
        
        print(coords[0], axis, ship_len)

        return 0

m = move()
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