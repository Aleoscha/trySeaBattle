import sqlite3
connection_string = "ships.db"

class DB:
    def __init__(self, connection_string="ships.db"):
        self.connection_string = connection_string

    def write_move(self, player, X, Y, result):
        '''
        Записывает ход
        Игрок: 0 / 1
        X: 1..10
        Y: 1..10
        result: {0: 'Мимо', 1:'Попал', 2:'Потопил',}
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("INSERT INTO moves VALUES (?, ?, ?, ?, 1)", (player, X, Y, result))
        con.commit()
        con.close()
        return True
    
    def get_moves(self, player=None):
        con = sqlite3.connect(self.connection_string)
        if player != None:
            cur = con.execute("SELECT * FROM moves WHERE player = ?", (player,))
        else:
            cur = con.execute("SELECT * FROM moves")
        res = cur.fetchall()
        # print(res, 'moves')
        con.close()
        return res

    
    def add_ship(self, player, X, Y, axis, ship_len):
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("INSERT INTO ships VALUES (?, ?, ?, ?, ?)", (player, X, Y, axis, ship_len))
        con.commit()
        con.close()
        return True

    # def del_ship(self, player, X, Y):
    #     con = sqlite3.connect(self.connection_string)
    #     cur = con.execute("INSERT INTO moves VALUES (?, ?, ?, ?, 1)", (player, X, Y, axis, ship_len))
    #     con.commit()
    #     con.close()
    #     return True

    def get_ships(self, player):
        '''
        Возвращает все корабли, которые начинаются в координатах X или Y. 
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT * FROM ships WHERE player = ?", (player,))
        res = cur.fetchall()
        # print(res)
        con.close()
        return res
    
    def get_ships_by_XY(self, player, X, Y):
        '''
        Возвращает все корабли, которые начинаются в координатах X или Y. 
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT * FROM ships WHERE player = ? AND (X = ? OR Y = ?)", (player, X, Y))
        res = cur.fetchall()
        # print(res)
        con.close()
        return res
    
    def get_shots_on_target(self, player):
        '''
        Возвращает количество попаданий игрока
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT COUNT(*) FROM moves WHERE player = ? AND result = ?", (player, 1))
        res = cur.fetchone()
        # print(res)
        con.close()
        return res

    def can_add(self, player):
        '''
        Проверяет, что кол-во кораблей игрока меньше 10
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT COUNT(ship_len) FROM ships WHERE player = ?", (player,))
        res = cur.fetchone()
        # print(res[0])
        con.close()
        if res[0] < 10:
            # print(True)
            return True
        else:
            # print(False)
            return False
        
    def get_cell_status(self, player, X, Y):
        '''
        Возвращает результат хода Игрока:Player в ячейку: X, Y
        -1: Ход не осуществлялся
         0: Мимо
         1: Попал
        '''

        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT * FROM moves WHERE player = ? and X = ? AND y = ?", (player, X, Y))
        res = cur.fetchone()
        # print(res)
        con.close()
        if res == None:
            return -1
        else:
            return res[3]
        
    def clear_moves(self):
        '''
        Удаляет все ходы
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("DELETE FROM moves")
        con.commit()
        # print(res)
        con.close()
        return 0
    
    def clear_ships(self):
        '''
        Удаляет корабли
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("DELETE FROM ships")
        con.commit()
        # print(res)
        con.close()
        return 0
    
    def get_game_status(self):
        '''
        Получает значение статуса игры (стадии)
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT stage FROM game")
        # cur = con.execute("SELECT game_status_0 * game_status_1 FROM games")
        cur = cur.fetchone()[0]
        # print(cur)
        con.close()
        return cur
    
    def next_game_status(self):
        '''
        Изменяет значение статуса игры (стадии)
        '''
        con = sqlite3.connect(self.connection_string)
        current_status = self.get_game_status()
        if current_status < 3:
            cur = con.execute("UPDATE game SET stage = ? WHERE gameid = 1", (current_status + 1,))  
            con.commit()
        con.close()
        return 0
    

    def get_game_turn(self):
        '''
        Получает значение очереди игрока
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT turn FROM game WHERE gameid = 1")
        cur = cur.fetchone()[0]
        print(cur)
        con.close()
        return cur
    
    def next_game_turn(self):
        '''
        Изменяет значение очереди игрока (Передает ход)
        '''
        con = sqlite3.connect(self.connection_string)
        current_turn = self.get_game_turn()
        cur = con.execute("UPDATE game SET turn = ? WHERE gameid = 1", ((current_turn + 1) % 2,))  
        con.commit()
        con.close()
        return 0
    
    def get_ship_lens(self, player):
        '''
        player: Игрок, длину кораблей которого мы получаем
        Возвращает словарь длин кораблей 
        '''
        con = sqlite3.connect(self.connection_string)
        cur = con.execute("SELECT ship_len, COUNT(*) FROM ships WHERE player = ? GROUP BY ship_len", (player,))
        cur = cur.fetchall()
        # print(cur, ' cur')
        ans = {}
        for c in cur:
            ans[c[0]] = c[1]
        # print(ans, ' ans')

        con.close()
        return ans


db = DB(connection_string=connection_string)
# print(db.get_shots_on_target(1)[0])
# db.get_ship_lens(0)
# print(db.get_cell_status(0, 3, 9))
# db.get_game_turn()
# db.next_game_turn()
# db.get_game_turn()
# db.clear_ships()
# db.clear_moves()

# db.add_ship(1, 6, 8, 1, 2)



# db.write_move(1, 4, 4, 1)
# db.add_ship(0, 2, 5, 2, 4)

# t = db.get_ship_types(0)
# print(sorted(t))

# print(db.get_ships_by_XY(0, 3, 3))