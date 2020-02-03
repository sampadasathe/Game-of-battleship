import random
from ship import Ship
from board import Board
from position import Position
import numpy as np



class Player:

    # Each player has a name. There should be no need to change or delete this!
    def __init__(self, name):
        self.__name = name
        self.__results = []
        self.__hits = []
        self.__bool_targets = []
        self.__start_diagonal = (0,0)
        self.__board_blank = np.zeros((10,10),dtype = np.int32)
        self.__remember = ''
        self.__count_miss = 0
        self.__adjusted = False
        self.__adjacent_ship = []
        self.__check = False
        
    def get_name(self):
        return self.__name

    def __str__(self):
        return self.get_name()

    # get_board should return a Board object containing 5 ships:
    # 1 aircraft carrier (length = 5)
    # 1 battleship (length = 4)
    # 1 cruiser (length = 3)
    # 1 submarine (length = 3)
    # 1 destroyer (length = 2)
    # You can make your own fun names for the ships, but the number and lengths
    # of the ship will be validated by the framework. Printing the board will
    # show the first letter of each ship's name.

    # This implementation returns the first sample layout from this web page:
    # http://datagenetics.com/blog/december32011/index.html
    def get_board(self):
        ships_list = [Ship('Carrier', Position('C', 10), 5, True),
                      Ship('battleship', Position('B', 3), 4, False),
                      Ship('submarine', Position('F', 2), 3, True),
                      Ship('crusier', Position('I', 3), 3, False),
                      Ship('destroyer', Position('J', 7), 2, False)]
        return Board(ships_list)

    # Takes a random shot, making no effort to remember it
    def next_shot(self):
        pos = self.next_target()
        self.check_position(pos.get_row_idx(),pos.get_col_idx())        
        return pos

    # result is a tuple consisting of:
    # - the shot location (a Position object)
    # - whether the shot was a hit (True) or a miss (False)
    # - whether a ship was sunk (True) or not (False)
    def post_shot_result(self, result):
        if result[1]:
            pos = result[0]
            row = pos.get_row_idx()
            col = pos.get_col_idx()
            self.__hits.append((row,col))
            self.__bool_targets.append(True)
            self.__board_pos[row,col] = 2
        elif result[1] == False:
            self.__bool_targets.append(False)
        if len(self.__bool_targets) > 4:
            self.__bool_targets = []

        self.__results.append(result)
    
    def next_target(self):
        if len(self.__results) == 0:
            self.last_position = self.__start_diagonal
            self.row_max = 9
            self.col_max = 9
            self.__row = 0
            self.__col = 0
            pos = Position(chr(65),1)
        else:
            result = self.__results[len(self.__results) -1]
            last_pos = result[0]
            self.last_position = (last_pos.get_row_idx(), last_pos.get_col_idx())
            last = self.last_position
            if result[2] and len(self.__adjacent_ship) == 0:
                hit_first = self.__hits[0]
                self.__row = hit_first[0] + 1
                self.__col = hit_first[1] + 1
                self.__hits = []
                self.__remember = ''
                self.__count_miss = 0
#                print(self.__row, self.__col)
#                print('Entered non adjacent')
            elif result[2] and len(self.__adjacent_ship) >= 1:
                hit_first = self.__adjacent_ship[0]
                self.__row = hit_first[0]
                self.__col = hit_first[1]
                hits = self.__hits[0]
                row_data = hits[0]
                col_data = hits[1]
                self.__hits = []
                self.__hits = [(row_data, col_data)]
                self.__adjacent_ship = []
                self.__remember = ''
                self.__count_miss = 0
#                print('Sunk',self.__row, self.__col)
            else:
                self.__row = last[0] +1
                self.__col = last[1] + 1
            
            if self.__row == 10 and self.__col == 10:
                self.__row = 2
                self.__col = 0
                self.__start_diagonal = (2,0)
                self.col_max = 7
                self.row_max = 9
            elif result[2] and self.__adjusted == True and len(self.__hits) == 1:
#                print('Inside lets sink this bitch')
#                print(self.__board_pos)
                if self.__col-1 != 10 and self.__col-1 >= 0 and  self.__board_pos[self.__row, self.__col-1] == 2:
                    if self.__col-2 != 10 and self.__col-2 >= 0 and self.__board_pos[self.__row, self.__col-2] == 0 and self.__check == False:
                        self.__remember = 'l'
                        self.__col -= 2
                        self.__check = True
                        self.__adjusted = False
                elif self.__col-1 != 10 and self.__col-1 >= 0 and  self.__board_pos[self.__row, self.__col-1] == 0:
                    self.__remember = 'l'
                    self.__col -= 1
                    self.__check = True
                    self.__adjusted = False
                    
                if self.__col+1 != 10 and self.__board_pos[self.__row, self.__col+1] == 2:
                    if self.__col+2 != 10 and self.__board_pos[self.__row, self.__col+2] == 0 and self.__check == False:
                        self.__remember = 'r'
                        self.__col += 2
                        self.__check = True
                        self.__adjusted = False
                elif self.__col+1 != 10 and self.__col+1 >= 0 and  self.__board_pos[self.__row, self.__col+1] == 0:
                    self.__remember = 'r'
                    self.__col += 1
                    self.__check = True
                    self.__adjusted = False
                        
                if self.__row-1 != 10 and self.__row-1 >= 0 and self.__board_pos[self.__row-1, self.__col] == 2:
                    if self.__row-2 != 10 and self.__row-2 >= 0 and self.__board_pos[self.__row-2, self.__col] == 0 and self.__check == False:
                        self.__remember = 'u'
#                        print('Inside up')
                        self.__row = self.__row - 2
                        self.__check = True
                        self.__adjusted = False
#                        print('uppp',self.__row,self.__col)
                elif self.__row-1 != 10 and self.__row-1 >= 0 and  self.__board_pos[self.__row-1, self.__col] == 0:
#                    print("Why though")
                    self.__remember = 'u'
                    self.__row -= 1
                    self.__check = True
                    self.__adjusted = False
                      
                if self.__row+1 != 10 and self.__board_pos[self.__row+1, self.__col] == 2:
                    if self.__row+2 != 10 and self.__board_pos[self.__row+2, self.__col] == 0 and self.__check == False:
                        self.__remember = 'd'
                        self.__row = self.__row + 2
                        self.__check = True
                        self.__adjusted = False
                elif self.__row+1 != 10 and self.__row+1 >= 0 and  self.__board_pos[self.__row+1, self.__col] == 0:
                    self.__remember = 'd'
                    self.__row += 1
                    self.__check = True
                    self.__adjusted = False
                
            elif ((result[1] == False and len(self.__hits) > 0) or result[1]) and result[2] == False:
                if len(self.__hits) > 0:
                    tup = self.__hits[len(self.__hits)-1]
                    row = tup[0]
                    col = tup[1] 
                    self.__row = row
                    self.__col = col
                if len(self.__hits) > 1 and result[1] == False and self.__adjusted == False:
                    self.__count_miss += 1
#                    print(self.__count_miss)
                if len(self.__hits) > 1 and result[1]:
                    if self.__col-1 != 10 and self.__board_pos[self.__row, self.__col-1] == 0 and self.__remember == 'l':
                        self.go_left(self.__row, self.__col)
                        if (self.__row, self.__col) in self.__hits:
                            self.go_right(self.__row, self.__col)
                    
                    elif self.__col+1 != 10 and self.__board_pos[self.__row, self.__col+1] == 0 and self.__remember == 'r':
                        self.go_right(self.__row, self.__col)
                        if (self.__row, self.__col) in self.__hits:
                            self.go_left(self.__row, self.__col)
                        
                    elif self.__row-1 != 10 and self.__board_pos[self.__row-1, self.__col] == 0 and self.__remember == 'u':
                        
                        self.go_up(self.__row, self.__col)
                        if (self.__row, self.__col) in self.__hits:
                            self.go_down(self.__row, self.__col)
                      
                    elif self.__row+1 != 10 and self.__board_pos[self.__row+1, self.__col] == 0 and self.__remember == 'd':
#                        print('Down')
                        self.go_down(self.__row, self.__col)
                        if (self.__row, self.__col) in self.__hits:
                            self.go_up(self.__row, self.__col)
#                        print('Down', self.__row, self.__col)
                elif len(self.__hits) == 1:
                    
                    if self.__col-1 != 10 and self.__board_pos[self.__row, self.__col-1] == 0:
                        
                        self.go_left(self.__row, self.__col)
                    
                    elif self.__col+1 != 10 and self.__board_pos[self.__row, self.__col+1] == 0:
                        
                        self.go_right(self.__row, self.__col)
                        
                    elif self.__row-1 != 10 and self.__board_pos[self.__row-1, self.__col] == 0:
                        
                        self.go_up(self.__row, self.__col)
                      
                    elif self.__row+1 != 10 and self.__board_pos[self.__row+1, self.__col] == 0:
                        
                        self.go_down(self.__row, self.__col)
#                        print('Len1 down',self.__row,self.__col)
                    
                        
                elif len(self.__hits) > 1 and result[1] == False and (self.__count_miss == 0 or self.__count_miss == 1):
                     hit_first = self.__hits[0]
                     self.__row = hit_first[0]
                     self.__col = hit_first[1]
                     if self.__remember == 'd':
                         if self.__row-1 != 10 and self.__board_pos[self.__row-1, self.__col] == 0:
                             
                             self.go_up(self.__row, self.__col)
                     elif self.__remember == 'u':
                         if self.__row+1 != 10 and self.__board_pos[self.__row+1, self.__col] == 0:
                            
                            self.go_down(self.__row, self.__col)
                     elif self.__remember == 'l':
                         if self.__col+1 != 10 and self.__board_pos[self.__row, self.__col+1] == 0:
                             
                             self.go_right(self.__row, self.__col)
                     elif self.__remember == 'r':
                         if self.__col-1 != 10 and self.__board_pos[self.__row, self.__col-1] == 0:
                             
                             self.go_left(self.__row, self.__col)
                elif len(self.__hits) > 1 and result[1] == False and self.__count_miss == 2:
                    next_ship = self.__hits[1]
                    row_val = next_ship[0]
                    col_val = next_ship[1]
                    self.__adjacent_ship.append((row_val,col_val))
#                    print('Ship pos',self.__hits[1])
                    hit_first = self.__hits[0]
                    self.__row = hit_first[0]
                    self.__col = hit_first[1]
                    self.__count_miss -=1
                    self.__adjusted = True
#                    print('Inside adjacent case',self.__row, self.__col)
                    if self.__remember == 'r':
                        if self.__row+1 != 10 and self.__board_pos[self.__row+1, self.__col] == 0:
#                            print('Inside adjacent case right', self.__row, self.__col)
                            self.go_down(self.__row, self.__col)
                    elif self.__remember == 'l':
#                        print('Inside adjacent case left', self.__row, self.__col)
                        if self.__row-1 != 10 and self.__board_pos[self.__row-1, self.__col] == 0:
                            self.go_up(self.__row, self.__col)
                    elif self.__remember == 'd':
#                        print('Inside adjacent case down', self.__row, self.__col)
                        if self.__col+1 != 10 and self.__board_pos[self.__row, self.__col+1] == 0:
                             
                            self.go_right(self.__row, self.__col)
                    elif self.__remember == 'u':
#                        print('Inside adjacent case up', self.__row, self.__col)
                        if self.__col-1 != 10 and self.__board_pos[self.__row, self.__col-1] == 0:
                             
                            self.go_left(self.__row, self.__col)
            
#            print('Inside len 1',self.__row, self.__col)
            if self.__row > 9 and self.__start_diagonal[1]==0:
                if(self.__start_diagonal[0] + 2 != 10):
                    self.__row = self.__start_diagonal[0] + 2
                    self.__col = self.__start_diagonal[1]
                    self.__start_diagonal = ()
                    self.__start_diagonal = (self.__row, 0)
                self.__hits = []
                if self.col_max - 2 > 0:
                    self.col_max -= 2
                else:
                    self.__row = 0
                    self.__col = 2
                    self.__start_diagonal = ()
                    self.__start_diagonal = (0,2)
                    self.col_max = 9
                    self.row_max = 7
                    
            
            elif self.__col > 9 and self.__start_diagonal[0]==0:
                if(self.__start_diagonal[1] + 2 != 10):
                    self.__row = self.__start_diagonal[0]
                    self.__col = self.__start_diagonal[1] + 2
                    self.__start_diagonal = ()
                    self.__start_diagonal = (0, self.__col)
                self.__hits = []
                if self.row_max - 2 > 0:
                    self.row_max -= 2
                else:
                    self.row = -1
                    self.col = -1
        

        pos = Position(chr(self.__row+65), self.__col+1)   
        return pos
            
    def go_left(self, row, col):
        self.__remember = ''
        self.__remember = 'l'
        self.__col = self.__col - 1
        position = Position(chr(self.__row+65), self.__col+1)
        isValid = position.validate()
        if isValid == False:
            self.__col = self.__col + 1
            self.go_right(self.__row, self.__col)
        
     
    def go_right(self, row, col):
        self.__remember = ''
        self.__remember = 'r'
        self.__col = self.__col + 1
        position = Position(chr(self.__row+65), self.__col+1)
        isValid = position.validate()
        if isValid == False:
            self.__col = self.__col - 1
            self.go_up(self.__row, self.__col)
        
         
    def go_up(self, row, col):
        self.__remember = ''
        self.__remember = 'u'
        self.__row = self.__row - 1
        position = Position(chr(self.__row+65), self.__col+1)
        isValid = position.validate()
        if isValid == False:
            self.__row = self.__row + 1
            self.go_down(self.__row, self.__col)
        
         
    def go_down(self, row, col):
        self.__remember = ''
        self.__remember = 'd'
        self.__row = self.__row + 1
        position = Position(chr(self.__row+65), self.__col+1)
        isValid = position.validate()
        if isValid == False:
            print(isValid)
            self.__row = self.__row - 1
        

        
        
    def blank_board(self):
        board_blank = np.zeros((10,10),dtype = np.int32)
        return board_blank


    def check_position(self,row,col):
        if len(self.__results) == 0:
            board_pos = self.__board_blank
            board_pos[int(row),int(col)] = 1
            self.__board_pos = board_pos
        else:
            board_pos = self.__board_pos
            board_pos[int(row),int(col)] = 1
            self.__board_pos = board_pos
        return board_pos

        
        