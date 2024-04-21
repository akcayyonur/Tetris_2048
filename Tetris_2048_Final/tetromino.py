from tile import Tile # used for modeling each tile on the tetrominoes
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # the random module is used for generating random values
import numpy as np  # the fundamental Python module for scientific computing

# A class for modeling tetrominoes with 7 different types as I, O, Z, S, J, L, T
class Tetromino:
    # the dimensions of the game grid (defined as class variables)
    grid_height, grid_width = None, None

    # A constructor for creating a tetromino with a given shape (type)
    def __init__(self, type):
        self.type = type # set the shape of the tetromino based on the given type
        # determine the occupied (non-empty) cells in the tile matrix based on
        # the shape of this tetromino (see the documentation given with this code)
        occupied_tiles = []
        if type == 'I':
            n = 4 # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino I in its initial rotation state
            occupied_tiles.append((1, 0))  # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((1, 3))
        elif type == 'O':
            n = 2  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino O in its initial rotation state
            occupied_tiles.append((0, 0))  # (column_index, row_index)
            occupied_tiles.append((1, 0))
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 1))
        elif type == 'Z':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial rotation state
            occupied_tiles.append((0, 0))  # (column_index, row_index)
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 1))
        elif type == 'S':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino S in its initial rotation state
            occupied_tiles.append((1, 0))  # (column_index, row_index)
            occupied_tiles.append((2, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((0, 1))
        elif type == 'J':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino J in its initial rotation state
            occupied_tiles.append((1, 0))  # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((0, 2))
        elif type == 'L':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino L in its initial rotation
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((2, 2))
        elif type == 'T':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino T in its initial rotation state
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 1))
            occupied_tiles.append((1, 2))

        # create a matrix of numbered tiles based on the shape of this tetromino
        self.tile_matrix = np.full((n, n), None)
        # create the four tiles (minos) of this tetromino and place these tiles
        # into the tile matrix
        for i in range(len(occupied_tiles)):
            col_index, row_index = occupied_tiles[i][0], occupied_tiles[i][1]
            # create a tile for each occupied cell of this tetromino
            self.tile_matrix[row_index][col_index] = Tile()
        # initialize the position of this tetromino (as the bottom left cell in
        # the tile matrix) with a random horizontal position above the game grid
        self.bottom_left_cell = Point()
        self.bottom_left_cell.y = self.grid_height - 1
        self.bottom_left_cell.x = random.randint(0, self.grid_width - n)

    # A method that computes and returns the position of the cell in the tile
    # matrix specified by the given row and column indexes
    def get_cell_position(self, row, col):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        position = Point()
        # horizontal position of the cell
        position.x = self.bottom_left_cell.x + col
        # vertical position of the cell
        position.y = self.bottom_left_cell.y + (n - 1) - row
        return position

    # A method to return a copy of the tile matrix without any empty row/column,
    # and the position of the bottom left cell when return_position is set
    def get_min_bounded_tile_matrix(self, return_position=False):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        # determine rows and columns to copy (omit empty rows and columns)
        min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] is not None:
                    if row < min_row:
                        min_row = row
                    if row > max_row:
                        max_row = row
                    if col < min_col:
                        min_col = col
                    if col > max_col:
                        max_col = col
        # copy the tiles from the tile matrix of this tetromino
        copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if self.tile_matrix[row][col] is not None:
                    row_ind = row - min_row
                    col_ind = col - min_col
                    copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
        # return just the matrix copy when return_position is not set (as True)
        # the argument return_position defaults to False when a value is not given
        if not return_position:
            return copy
        # otherwise return the position of the bottom left cell in copy as well
        else:
            blc_position = cp.copy(self.bottom_left_cell)
            blc_position.translate(min_col, (n - 1) - max_row)
            return copy, blc_position

    # A method for drawing the tetromino on the game grid
    def draw(self):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
                # draw each occupied cell as a tile on the game grid
                if self.tile_matrix[row][col] is not None:
                    # get the position of the tile
                    position = self.get_cell_position(row, col)
                    # draw only the tiles that are inside the game grid
                    if position.y < self.grid_height:
                        self.tile_matrix[row][col].draw(position)

    # A method for moving this tetromino in a given direction by 1 on the grid
    def move(self, direction, game_grid):
        # check if this tetromino can be moved in the given direction by using
        # the can_be_moved method defined below
        if not (self.can_be_moved(direction, game_grid)):
            return False  # the tetromino cannot be moved in the given direction
        # move this tetromino by updating the position of its bottom left cell
        if direction == "left":
            self.bottom_left_cell.x -= 1
        elif direction == "right":
            self.bottom_left_cell.x += 1
        else:  # direction == "down"
            self.bottom_left_cell.y -= 1
        return True  # a successful move in the given direction

    # Rotate the tetromino 90 degrees counter clockwise
    def rotate_tetromino(self, direction, game_grid):
        # check if the tetromino can be rotated in the given direction by using the
        # can_be_rotated method defined below
        if not (self.can_be_rotated(direction, game_grid)):
            return False
        # Rotate tetromino 90 degree # up = clockwise
        if direction == "a":
            # get the copy of the tile matrix and the position of the bottom left
            # cell in the copy
            self.tile_matrix = np.rot90(self.tile_matrix, 1)
        return True

    # Method for checking if the tetromino can be rotated in the given direction
    def can_be_rotated(self, dir, game_grid):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        # get the copy of the tile matrix
        copy_of_tile_matrix = cp.copy(self.tile_matrix)
        copy_of_tile_matrix = np.rot90(copy_of_tile_matrix, 1)

        for row in range(n):
            for col in range(n):
                if dir == "a" and copy_of_tile_matrix[row][col] is not None:
                    # get the position of the tile
                    position = self.get_cell_position(row, col)
                    # check if the tile is inside the game grid
                    if position.y < 0 or position.x < 0 or position.x >= self.grid_width:
                        return False
        return True

    # A method for checking if this tetromino can be moved in a given direction
    def can_be_moved(self, dir, game_grid):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        # check for moving left or right
        if dir == "left" or dir == "right":
            for row in range(n):
                for col in range(n):
                    # direction = left --> check the leftmost tile of each row
                    if dir == "left" and self.tile_matrix[row][col] is not None:
                        # the position of the leftmost tile of the current row
                        leftmost = self.get_cell_position(row, col)
                        # if any leftmost tile is at x = 0
                        if leftmost.x == 0:
                            return False # this tetromino cannot be moved left
                        # if the grid cell on the left of a leftmost tile is occupied
                        if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                            return False # this tetromino cannot be moved left
                        # as the leftmost tile of the current row is checked
                        break  # end the inner for loop
                    # direction = right --> check the rightmost tile of each row
                    elif dir == "right" and self.tile_matrix[row][n - 1 - col] is not None:
                        rightmost = self.get_cell_position(row, n - 1 - col)
                        # if any rightmost tile is at x = grid_width - 1
                        if rightmost.x == self.grid_width - 1:
                            return False # this tetromino cannot be moved right
                        # if the grid cell on the right of a rightmost tile is occupied
                        if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                            return False # this tetromino cannot be moved right
                        # as the rightmost tile of the current row is checked
                        break  # end the inner for loop
                    # direction = up --> check the topmost tile of each column
        # direction = down --> check the bottommost tile of each column
        else:
            for col in range(n):
                for row in range(n - 1, -1, -1):
                    # if the current cell of the tetromino is occupied by a tile
                    if self.tile_matrix[row][col] is not None:
                        # the position of the bottommost tile of the current col
                        bottommost = self.get_cell_position(row, col)
                        # if any bottommost tile is at y = 0
                        if bottommost.y == 0:
                            return False # this tetromino cannot be moved down
                            # if the grid cell below any bottommost tile is occupied
                        if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                            return False # this tetromino cannot be moved down
                        # as the bottommost tile of the current row is checked
                        break  # end the inner for loop
        # if this method does not end by returning False before this line
        return True  # this tetromino can be moved in the given direction