class Ship:
    def __init__(self, X, Y, ship_len, axes=0) -> None:
        self.X = X
        self.Y = Y
        self.ship_len = ship_len
        self.axes=axes
    
    def isShip(self, x, y):
        print(list(range(self.Y, self.Y + self.ship_len)))
        if self.axes == 0:
            if self.X == x and y in range(self.Y, self.Y + self.ship_len):
                return True
        else:
            if self.Y == y and x in range(self.X, self.X + self.ship_len):
                return True
        return False
    
    def isSafetyZone(self, x, y):

        if self.axes == 0:
            if x in range(self.X - 1, self.X + 2) and y in range(self.Y, self.Y + self.ship_len):
                return True
        else:
            if y in range(self.Y - 1, self.Y + 2) and x in range(self.X, self.X + self.ship_len):
                return True
        return False
    
    def isSunk(self, ship, moves):
        '''
        Проверяет потоплен ли корабль
        '''
        
        pass
    
    # @staticmethod
    # def setShip():

        
s = Ship(1,1,4,1)
print(s.isShip(4,1))


                
