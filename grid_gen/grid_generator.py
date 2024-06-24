# Stochastic sudoku board generator. Pick a cell, assign a digit to it,
# check the rest, and repeat. If the board becomes unsolvable, roll back
# changes and pick another number.
# Generate a certain amount of valid sudoku boards and store them in a big
# Numpy array.
# Copyright (C) 2024 Álvaro L.G.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import random as rng

def generate_incidence_lookup():
	#There are 81 cells un a sudoku, and every cell updates other 20
	# and itself, 21 in total
	incidence = np.zeros(shape=(81,21), dtype = int)

	for cell_index in range(81):
		cell_row_index = cell_index // 9
		cell_col_index = cell_index % 9
		cell_box_index = (cell_row_index//3)*3 + (cell_col_index//3)

		affected = 0
		for check_cell in range(81):
			check_row_index = check_cell // 9
			check_col_index = check_cell % 9
			check_box_index = (check_row_index//3)*3 + (check_col_index//3)
			if ((check_row_index == cell_row_index) 
	   		or (check_col_index == cell_col_index) 
			or (check_box_index == cell_box_index)):
				incidence[cell_index][affected] = check_cell
				affected += 1
	print(incidence.tolist())

incidence = [
	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 28, 37, 46, 55, 64, 73],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 29, 38, 47, 56, 65, 74],[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 30, 39, 48, 57, 66, 75],[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 31, 40, 49, 58, 67, 76],[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 32, 41, 50, 59, 68, 77],[0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78],[0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79],[0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80],[0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27,36,45,54,63,72],[0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 28,37,46,55,64,73],[0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29,38,47,56,65,74],[3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 30,39,48,57,66,75],[3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 31,40,49,58,67,76],[3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 32,41,50,59,68,77],
	[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 33,42,51,60,69,78],
	[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 34,43,52,61,70,79],
	[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 35,44,53,62,71,80],
	[0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,36,45,54,63,72],
	[0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28,37,46,55,64,73],
	[0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 29,38,47,56,65,74],
	[3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26,30,39,48,57,66,75],
	[3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26,31,40,49,58,67,76],
	[3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26,32,41,50,59,68,77],
	[6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,33,42,51,60,69,78],
	[6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,34,43,52,61,70,79],
	[6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,35,44,53,62,71,80],
	[0, 9, 18, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,38,45,46,47,54,63,72],
	[1, 10, 19, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,37,38,45,46,47,55,64,73],
	[2, 11, 20, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,37,38,45,46,47,56,65,74],
	[3, 12, 21, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39,40,41,48,49,50,57,66,75],
	[4, 13, 22, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39,40,41,48,49,50,58,67,76],
	[5, 14, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39,40,41,48,49,50,59,68,77],
	[6, 15, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42,43,44,51,52,53,60,69,78],
	[7, 16, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42,43,44,51,52,53,61,70,79],
	[8, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42,43,44,51,52,53,62,71,80],
	[0, 9, 18, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43,44,45,46,47,54,63,72],
	[1, 10, 19, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42,43,44,45,46,47,55,64,73],
	[2, 11, 20, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42,43,44,45,46,47,56,65,74],
	[3, 12, 21, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42,43,44,48,49,50,57,66,75],
	[4, 13, 22, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42,43,44,48,49,50,58,67,76],
	[5, 14, 23, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42,43,44,48,49,50,59,68,77],
	[6, 15, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,43,44,51,52,53,60,69,78],
	[7, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,43,44,51,52,53,61,70,79],
	[8, 17, 26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,43,44,51,52,53,62,71,80],
	[0, 9, 18, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49,50,51,52,53,54,63,72],
	[1, 10, 19, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48,49,50,51,52,53,55,64,73],
	[2, 11, 20, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48,49,50,51,52,53,56,65,74],
	[3, 12, 21, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48,49,50,51,52,53,57,66,75],
	[4, 13, 22, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48,49,50,51,52,53,58,67,76],
	[5, 14, 23, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48,49,50,51,52,53,59,68,77],
	[6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48,49,50,51,52,53,60,69,78],
	[7, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48,49,50,51,52,53,61,70,79],
	[8, 17, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48,49,50,51,52,53,62,71,80],
	[0, 9, 18, 27, 36, 45, 54, 55, 56, 57, 58, 59, 60, 61,62,63,64,65,72,73,74],
	[1, 10, 19, 28, 37, 46, 54, 55, 56, 57, 58, 59, 60,61,62,63,64,65,72,73,74],
	[2, 11, 20, 29, 38, 47, 54, 55, 56, 57, 58, 59, 60,61,62,63,64,65,72,73,74],
	[3, 12, 21, 30, 39, 48, 54, 55, 56, 57, 58, 59, 60,61,62,66,67,68,75,76,77],
	[4, 13, 22, 31, 40, 49, 54, 55, 56, 57, 58, 59, 60,61,62,66,67,68,75,76,77],
	[5, 14, 23, 32, 41, 50, 54, 55, 56, 57, 58, 59, 60,61,62,66,67,68,75,76,77],
	[6, 15, 24, 33, 42, 51, 54, 55, 56, 57, 58, 59, 60,61,62,69,70,71,78,79,80],
	[7, 16, 25, 34, 43, 52, 54, 55, 56, 57, 58, 59, 60,61,62,69,70,71,78,79,80],
	[8, 17, 26, 35, 44, 53, 54, 55, 56, 57, 58, 59, 60,61,62,69,70,71,78,79,80],
	[0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 66, 67,68,69,70,71,72,73,74],
	[1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 66,67,68,69,70,71,72,73,74],
	[2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 66,67,68,69,70,71,72,73,74],
	[3, 12, 21, 30, 39, 48, 57, 58, 59, 63, 64, 65, 66,67,68,69,70,71,75,76,77],
	[4, 13, 22, 31, 40, 49, 57, 58, 59, 63, 64, 65, 66,67,68,69,70,71,75,76,77],
	[5, 14, 23, 32, 41, 50, 57, 58, 59, 63, 64, 65, 66,67,68,69,70,71,75,76,77],
	[6, 15, 24, 33, 42, 51, 60, 61, 62, 63, 64, 65, 66,67,68,69,70,71,78,79,80],
	[7, 16, 25, 34, 43, 52, 60, 61, 62, 63, 64, 65, 66,67,68,69,70,71,78,79,80],
	[8, 17, 26, 35, 44, 53, 60, 61, 62, 63, 64, 65, 66,67,68,69,70,71,78,79,80],
	[0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 72, 73,74,75,76,77,78,79,80],
	[1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 72,73,74,75,76,77,78,79,80],
	[2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 72,73,74,75,76,77,78,79,80],
	[3, 12, 21, 30, 39, 48, 57, 58, 59, 66, 67, 68, 72,73,74,75,76,77,78,79,80],
	[4, 13, 22, 31, 40, 49, 57, 58, 59, 66, 67, 68, 72,73,74,75,76,77,78,79,80],
	[5, 14, 23, 32, 41, 50, 57, 58, 59, 66, 67, 68, 72,73,74,75,76,77,78,79,80],
	[6, 15, 24, 33, 42, 51, 60, 61, 62, 69, 70, 71, 72,73,74,75,76,77,78,79,80],
	[7, 16, 25, 34, 43, 52, 60, 61, 62, 69, 70, 71, 72,73,74,75,76,77,78,79,80],
	[8, 17, 26, 35, 44, 53, 60, 61, 62, 69, 70, 71, 72,73,74,75,76,77,78,79,80]
]

def stochastic_generate_board(seed: int = 1):
	rng.seed(seed)
	#TODO Find out the best way to pack the info. Available digit, written digit, and tried digits. I suspect the best way is to use a python dynamic list instead of a numpy array
	board_numeric = np.zeros(shape=(9,9),dtype=int)
	#TODO Remove the board_categorical approach and use a 81x?? array that holds all the available digits serialized row first. That way, using an incidence lookup table, cells can be updated directly without computing the row, col and box indices.
	available = [1,2,3,4,5,6,7,8,9]
	board_categorical = {
		'available_in_row': {
			0:available.copy(),
			1:available.copy(),
			2:available.copy(),
			3:available.copy(),
			4:available.copy(),
			5:available.copy(),
			6:available.copy(),
			7:available.copy(),
			8:available.copy(),
		},
		'available_in_col': {
			0:available.copy(),
			1:available.copy(),
			2:available.copy(),
			3:available.copy(),
			4:available.copy(),
			5:available.copy(),
			6:available.copy(),
			7:available.copy(),
			8:available.copy(),
		},
		'available_in_box': {
			0:available.copy(),
			1:available.copy(),
			2:available.copy(),
			3:available.copy(),
			4:available.copy(),
			5:available.copy(),
			6:available.copy(),
			7:available.copy(),
			8:available.copy(),
		}
	}

	def get_available_digits_for_cell(cell_index: int):
		cell_row_index = cell_index // 9
		cell_col_index = cell_index % 9
		cell_box_index = (cell_row_index//3)*3 + (cell_col_index//3)

		#Extract the available digits for the row, column and box of the selected cell
		available_in_row = board_categorical['available_in_row'][cell_row_index]
		available_in_col = board_categorical['available_in_col'][cell_col_index]
		available_in_box = board_categorical['available_in_box'][cell_box_index]
		print("Available row: ", available_in_row)
		print("Available col: ",available_in_col)
		print("Available box: ",available_in_box)

		#The available digits for the selected cell are only the ones that are available in the three categories, row, column and box.
		available_in_cell = list(set(available_in_row) & set(available_in_col) & set(available_in_box))
		return available_in_cell

	def put_digit_in_board(cell_index: int, digit: int):
		cell_row_index = cell_index // 9
		cell_col_index = cell_index % 9
		cell_box_index = (cell_row_index//3)*3 + (cell_col_index//3)
		board_numeric[cell_row_index][cell_col_index] = digit

		board_categorical['available_in_row'][cell_row_index].remove(digit)
		print("Available row: ", board_categorical['available_in_row'][cell_row_index])
		board_categorical['available_in_col'][cell_col_index].remove(digit)
		print("Available col: ", board_categorical['available_in_col'][cell_col_index])
		board_categorical['available_in_box'][cell_box_index].remove(digit)
		print("Available box: ", board_categorical['available_in_box'][cell_box_index])

	def pop_digit_from_board(cell_index: int):
		print("Popping cell: ", cell_index, end=" ")
		cell_row_index = cell_index // 9
		cell_col_index = cell_index % 9
		cell_box_index = (cell_row_index//3)*3 + (cell_col_index//3)
		digit = board_numeric[cell_row_index][cell_col_index]
		board_numeric[cell_row_index][cell_col_index] = 0
		print("Digit: ", digit)

		board_categorical['available_in_row'][cell_row_index].append(digit)
		print("Available row: ", board_categorical['available_in_row'][cell_row_index])
		board_categorical['available_in_col'][cell_col_index].append(digit)
		print("Available col: ", board_categorical['available_in_col'][cell_col_index])
		board_categorical['available_in_box'][cell_box_index].append(digit)
		print("Available box: ", board_categorical['available_in_box'][cell_box_index])

	#From 0 to 80

	#Create a list of indices that represent the order in which the cells will be filled in
	cell_random_access_list = list(range( 81))
	rng.shuffle(cell_random_access_list)

	for cell_index in cell_random_access_list:
		#TODO
		print("TODO")
	return board_numeric

def generate_batch(num):
	root_seed = 1
	rng.seed(root_seed)
	batch_seeds= [rng.randint() for _ in range(num)]
	board_batch = np.empty(shape=(num,9,9), dtype=int)
	for i in range(num):
		board_batch[i] = stochastic_generate_board(batch_seeds[i])


if __name__ == "__main__":
	print("Sudoku board generator. Copyright (C) 2024 Álvaro L.G.\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it under the GNU GPL License.")
	#generate_batch(10000)
	#print(generate_board())
	#generate_incidence_lookup()