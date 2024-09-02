class Ship:
    def __init__(self, X=0, Y=0, ship_len=0, axes=0) -> None:
        self.X = X
        self.Y = Y
        self.ship_len = ship_len
        self.axes=axes
    
    # def isShip(self, x, y):
    #     '''
    #     Возвращает наличие корабля в ячейке. Не используется? 
    #     '''
    #     print(list(range(self.Y, self.Y + self.ship_len)))
    #     if self.axes == 0:
    #         if self.X == x and y in range(self.Y, self.Y + self.ship_len):
    #             return True
    #     else:
    #         if self.Y == y and x in range(self.X, self.X + self.ship_len):
    #             return True
    #     return False
    
    def get_safety_zone(self, x, y, axis, ship_len):
        '''
        Возвращает ячейки, которые являются охранной зоной корабля (включая сам корабль)
        '''
        cells = []
        
        if axis == 0:
            for ind in range(x - 1, x + 2):
                for jnd in range(y - 1, y + ship_len + 1):
                    cells.append((ind, jnd))
        else:
            for ind in range(x - 1, x + ship_len+ 1):
                for jnd in range(y - 1, y + 2):
                    cells.append((ind, jnd))
        return cells
    
    def get_ship_cells(self, x, y, axis, ship_len):
        '''
        Возвращет ячейки, которые занимает корабль
        '''
        cells = []

        if axis == 0:
            ind = x
            for jnd in range(y, y + ship_len):
                cells.append((ind, jnd))
        else:
            jnd = y
            for ind in range(x, x + ship_len):
                cells.append((ind, jnd))
        return cells
    
    def isSunk(self, ship, moves):
        '''
        Проверяет потоплен ли корабль
        '''
        
        pass
    
    # @staticmethod
    # def setShip():

        
s = Ship(1,1,4,1)
# print(s.get_ship_cells( 3, 7, 0, 3))
# print(s.get_safety_zone(1, 8, 0, 3))


                
