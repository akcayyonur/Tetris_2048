################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types (shapes)

# The main function where this program starts execution
def start():
   # set main window canvas
   stddraw.setCanvasSize(600, 600)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, 16.5)
   stddraw.setYscale(-0.5, 15.5)
   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(16, 17)
   # set game settings
   game_speed, grid_results, game_type = prepare_screen()
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   info_w = 5 # do not change this value
   game_w = grid_w + info_w
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 38 * grid_h, 60 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, game_w - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w, info_w, game_speed, game_type)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino(grid_h, grid_w)
   grid.current_tetromino = current_tetromino
   # create the next tetromino to enter the game grid
   # by using the create_tetromino function defined below
   next_tetromino = create_tetromino(grid_h, grid_w)
   grid.next_tetromino = next_tetromino

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
            # if the a key has been pressed
         elif key_typed == "a":
            # rotate the active tetromino counter-clockwise
            current_tetromino.rotate_tetromino(key_typed, grid)
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      # place the active tetromino on the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         grid.update_grid(tiles, pos)
         game_over = grid.game_over
         # game over menu
         if game_over:
            is_restarted = game_over_screen(grid_h, game_w, grid.score)
            if is_restarted:
               grid = GameGrid(grid_h, grid_w, info_w, game_speed, game_type)
            else:
               start() # returns the main menu
         # check if any row is filled and clear this rows
         grid.clear_tiles()
         # assign the next tetromino to the current tetromino
         # by using the create_tetromino function defined below
         current_tetromino = next_tetromino
         grid.current_tetromino = current_tetromino
         # create the next tetromino that will used the next time
         next_tetromino = create_tetromino(grid_h, grid_w)
         grid.next_tetromino = next_tetromino

      # display the game grid and the current tetromino
      grid.display()

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = ["I", "J", "L", "O", "S", "T", "Z"]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(0, 0, 0)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 1.5
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, button_blc_y + 1, text_to_display)
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break # break the loop to end the method and start the game

# Function promps, when the game is initialized at the first.
# It gets the difficulty(game speed) from the user.
# @return it returns the speed of the game, which is delay of game.
def prepare_screen():
   # setting default colors.
   background_color = Color(42, 69, 99); button_color = Color(25, 255, 228); text_color = Color(31, 160, 239); black_color = Color(0, 0, 0); white_color = Color(255, 255, 255)
   # creating a short method, to do conversions.
   pixelToCoordinate = lambda x, in_min, in_max, out_min, out_max : int( round( ((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min) ) )
   stddraw.setXscale(0,500); stddraw.setYscale(0,500)
   gridResults = [12, 20]
   # setting a default game speed.
   gameSpeed = 0
   # setting a default game type.
   game_type = ""
   # a loop that runs the window fully, it draw all neccessary elements, and gets input from the user.
   while True:
      # clearing the background, to be able to create an doubleBuffering affect on canvas
      stddraw.clear(background_color)
      # drawing the boundaries of game mode options
      stddraw.setPenColor(Color(0,255,0)); stddraw.filledRectangle(245-75/2,315,85,50);
      stddraw.setPenColor(Color(255, 255, )); stddraw.filledRectangle(245-75/2,215,85,50);
      stddraw.setPenColor(Color(255, 0, 0)); stddraw.filledRectangle(245-75/2,115,85,50)
      stddraw.setPenColor(button_color); stddraw.filledRectangle(250-75/2,320,75,40); stddraw.filledRectangle(250-75/2,220,75,40); stddraw.filledRectangle(250-75/2,120,75,40)
      #drawing the boundaries of header
      stddraw.setPenColor(Color(255, 255, 255));stddraw.filledRectangle(185 - 75 / 2, 415, 205, 50);
      stddraw.setPenColor(button_color);stddraw.filledRectangle(190 - 75 / 2, 420, 195, 40);
      # drawing the texts of game mod buttons
      stddraw.setPenColor(black_color); stddraw.boldText(250,340,"EASY"); stddraw.boldText(250,240,"MEDIUM"); stddraw.boldText(250,140,"HARD")
      # drawing the text for header
      stddraw.setPenColor(black_color);stddraw.boldText(250, 440, "CHOSE DIFFICULTY")
      # showing results, with the most less value
      stddraw.show(10)
      # mouse press check, to find where mouse is"
      if stddraw.mousePressed():
         # getting mouse position after check
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # catching the game difficulty
         if   ((mouse_x >= 250-75/2 and mouse_x <= 250-75/2 + 40) and (mouse_y >= (320) and mouse_y <= (320) + 40)): gameSpeed = 400; game_type = "easy";   return gameSpeed, tuple(gridResults), game_type
         elif ((mouse_x >= 250-75/2 and mouse_x <= 250-75/2 + 40) and (mouse_y >= (220) and mouse_y <= (220) + 40)): gameSpeed = 250; game_type = "medium"; return gameSpeed, tuple(gridResults), game_type
         elif ((mouse_x >= 250-75/2 and mouse_x <= 250-75/2 + 40) and (mouse_y >= (120) and mouse_y <= (120) + 40)): gameSpeed = 150; game_type = "hard";   return gameSpeed, tuple(gridResults), game_type

# Function for displaying the game over screen
def game_over_screen(grid_h, game_w, current_score):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(0, 0, 0)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (game_w - 1) / 2, grid_h - 5
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = game_w - 6, 1.5
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 2.75
   # display game over text
   stddraw.setPenColor(Color(255, 0, 0))
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(80)
   game_over_text = "Game Over!"
   stddraw.boldText(img_center_x, (button_blc_y + img_center_y) / 2, game_over_text)
   # display the current score text
   stddraw.setFontSize(40)
   stddraw.text(img_center_x, (button_blc_y + img_center_y) / 2 - 1.5, "Your score: " + str(current_score))

   # display the restart game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the restart game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Restart the Game"
   stddraw.text(img_center_x, button_blc_y + 0.75, text_to_display)


   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               return True # return True to indicate that the game should be restarted

         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y - 2 and mouse_y <= button_blc_y - 2 + button_h:
               return False # return False to indicate that the game should be returned to the main menu


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__== '__main__':
   start()