from player import *
from board import *
from cell import *

a = Player('A') 
b = Player('B') 
print(a) 
print(b)

board = Board('board1.txt')

print('>>> Test function add_player:') 
board.add_player(a)
print(board.cell_list[0].get_occupy_list_str()) 
board.add_player(b)
print(board.cell_list[0].get_occupy_list_str())

print('>>> Test function access_cell:') 
starting_cell_id = 0
starting_cell = board.access_cell(starting_cell_id)
print(starting_cell) 
print(starting_cell.get_occupy_list_str())

winning_cell_id = 19
winning_cell = board.access_cell(winning_cell_id) 
print(winning_cell) 
print(winning_cell.get_occupy_list_str()) # print empty string since no player in the winning cell