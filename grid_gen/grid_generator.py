# Generate a certain amount of valid sudoku grids and store them in a big
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

def generate_grid(seed: int = 1):
	rng.seed(seed)
	grid_numeric = np.empty(shape=(9,9),dtype=int)
	available = [1,2,3,4,5,6,7,8,9]
	grid_categorical = {
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
	#From 0 to 80

	#Create a list of indices that represent the order in which the cells will be filled in
	cell_random_access_list = list(range( 81))
	rng.shuffle(cell_random_access_list)

	for cell_index in cell_random_access_list:
		print()
		print("Cell: ", cell_index)
		cell_row_index = cell_index // 9
		cell_col_index = cell_index % 9
		cell_box_index = (cell_row_index//3)*3 + (cell_col_index//3)

		#Extract the available digits for the row, column and box of the selected cell
		available_in_row = grid_categorical['available_in_row'][cell_row_index]
		available_in_col = grid_categorical['available_in_col'][cell_col_index]
		available_in_box = grid_categorical['available_in_box'][cell_box_index]
		print("Available row: ", available_in_row)
		print("Available col: ",available_in_col)
		print("Available box: ",available_in_box)

		#The available digits for the selected cell are only the ones that are available in the three categories, row, column and box.
		available_in_cell = list(set(available_in_row) & set(available_in_col) & set(available_in_box))
		print("Available cell: ", available_in_cell)

		#The algorithm shouldn't reach a state where a cell cannot be assigned a digit, raise an ugly exception if that occurs
		if len(available_in_cell) == 0:
			msg = f"No digits available for cell[index={cell_index}][row={cell_row_index}][col={cell_col_index}][box={cell_box_index}]"
			raise ProcessLookupError(msg)

		#Pick a random digit from the list, add it to the numerical grid and update the available digits in the categorical grid
		digit = rng.choice(available_in_cell)
		print("Digit: ", digit)

		grid_numeric[cell_row_index][cell_col_index] = digit

		grid_categorical['available_in_row'][cell_row_index].remove(digit)
		print("Available row: ", grid_categorical['available_in_row'][cell_row_index])
		grid_categorical['available_in_col'][cell_col_index].remove(digit)
		print("Available col: ", grid_categorical['available_in_col'][cell_col_index])
		grid_categorical['available_in_box'][cell_box_index].remove(digit)
		print("Available box: ", grid_categorical['available_in_box'][cell_box_index])

	return grid_numeric

def generate_batch(num):
	root_seed = 1
	rng.seed(root_seed)
	batch_seeds= [rng.randint() for _ in range(num)]
	grid_batch = np.empty(shape=(num,9,9), dtype=int)
	for i in range(num):
		grid_batch[i] = generate_grid(batch_seeds[i])


if __name__ == "__main__":
	#generate_batch(10000)
	print(generate_grid())