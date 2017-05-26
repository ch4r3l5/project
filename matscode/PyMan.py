#! /usr/bin/env python
# -*- coding: utf-8 -*-

# > This file featured some comments already. However, I've taken the liberty
# > To explain most of the notes in further detail.
# > Any of the comments that feature a '>' within the comment are updated
# > or written in more detail by myself. Any without have come included with the
# > file and require no further explanation.

import os, sys

# > Pygame framework imported, allows the program to use scrpt hooks and commands that don't come default with Python
import pygame

# > Importing the level that was created in the Level001.py file
import level001

# > Importing the sprite that is defined in basicSprite.py
import basicSprite

#> This function includes various constant variables such as the display size, the keyboard inputs and so on.
from pygame.locals import *

# > Controller for various sound elements that occur in the program. (Startup Sound, etc.)
from pygame import mixer

# > Importing the helpers.py file
from helpers import *

# > Snakesprite is the pac-man image itself as the original version of the game started by
# > using a snake sprite as a test.
from snakeSprite import Snake,Ghost

# > Menu screen imported
from menu import *

# > Logo for menu imported
from image import *

# TODO
# > Arduino light interaction. Lives? Power-Pill counter?
# > Dynamic Arduino Scoreboard
# > Updated sprites and icons made in processing

# > A timer for the game clock. As a side note, we could also use this to output
# > a timer to the arduino instead of a scoreboard.
clock = pygame.time.Clock()

# > Error messages for sound and font failing to import.
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

BLOCK_SIZE = 24

# > Menu screen config
def mainmenu(screen):

	# > Options for the menu
	menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
		# > Launches the game
		[('Start Game', 1, None),

		# > Leads to menu_options as seen below.
		('Options',    2, None),

		# > Closes window
		('Exit',       3, None)])

	# > Options menu, not configured. Only option is to go back.
	menu_options = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                [('Back',  0, None),
                 ('opt 1',      200, None),
		 ('opt 2',      200, None)])


	# > Commands for configuring the menu display. Centers the images that are loaded on the
	# > "draw surface" (The window)
	menu.set_center(True, True)
	menu_options.set_center(True, True)

	# > Center the menu on the draw_surface (the entire screen here)
	menu.set_alignment('center', 'center')

	# > Create the state variables (Both variables are different as if they were the
	# > same the screen would wait for User Input to advance.
	state = 0
	prev_state = 1

	# > This command is from PyGame, this will "tell" pygame where the screen needs
	# > to be updated. This is efficient as the whole screen does not need updating,
	# > only a portion of it.
	rect_list = []

	# > Does not take input from the mouse, this is very resource efficient.
	pygame.event.set_blocked(pygame.MOUSEMOTION)

	# > The main while loop, this handles functionality for the loading screen.
	while 1:

		# Check if the state has changed, if it has, then post a user event to
		# the queue to force the menu to be shown at least once
		print prev_state,state

		if prev_state != state:
			print state
			bkg = load_image('bkg.jpg','data/images')
			screen.blit(bkg, (0, 0))
			pygame.display.flip()

			pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
			prev_state = state

		# > If the "E" key is pressed then the next event is called. The state
		# > of the "E" key is decided by the function 'pygame.event.wait'
		e = pygame.event.wait()

		# Update the menu, based on which "state" we are in - When using the menu
		# in a more complex program, definitely make the states global variables
		# so that you can refer to them by a name
		if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
			if state == 0:
				rect_list, state = menu.update(e, state)
			elif state == 1:
				break
				state = 0
			elif state == 2:
				rect_list, state = menu_options.update(e, state)
				print 'Options!',state
			else:
				print 'Exit!'
				pygame.quit()
				sys.exit()

		# Quit if the user presses the exit button
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Update the screen
		pygame.display.update(rect_list)

# > The initialization of the game
# > Initialization and appearing on the screen are 2 different things
# > When an object, function or on screen asset is 'initialized' it is
# > Loaded into temporary memory in order to execute.
# > In this instance, the program is preparing to display the main game screen, configure
# > the window size and set constant parameters for the game.
class PyManMain:
    """The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

    def __init__(self, width=640,height=480):
        """Initialize"""
        pygame.init()

        """Set the window Size"""
        self.width = width
        self.height = height

        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))
	pygame.display.set_caption("Mac Pan - Matthew Rollings")


	# Setup the sounds
	# > Pygame.mixer was seen imported at the top of the code. This plays the
	# > introduction audio you usually hear at the start of a game of pacman.
	pygame.mixer.init()
	self.sounds={'die':mixer.Sound("die.ogg"),'intro':mixer.Sound("intro.ogg")}

	self.sounds['intro'].play()

	# Setup the variables
	# > These variables are used to determine which direction there is no collision
	# > Allowing the program to determine whether or not pac-man came make a turn or
	# > whether it is in a corner.
	self.collisiontol=5;
	self.collisions=0;

	# > Main loop used for game functionality
    def MainLoop(self):
        """This is the Main Loop of the Game"""
	while 1:

		# > Loading all of the graphic components
		mainmenu(self.screen)
		"""Load All of our Sprites"""
		self.LoadSprites();

		# > Background assets loaded from earlier.
		"""Create the background"""
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0,0,0))


		"""Draw the blocks onto the background, since they only need to be
		drawn once"""
		self.block_sprites.draw(self.background)
		self.gwall_sprites.draw(self.background)
		-
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

					# > Determining which way to turn (if any)
				elif event.type == KEYDOWN: #or event.type == KEYUP
					if ((event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP) or (event.key == K_DOWN)):
						self.snake.MoveKeyDown(event.key)

			# > Sprites for the enemies and the pac-man itself are loaded and upadted depending on direction
			"""Update the sprites"""
			self.snake_sprites.update(self.block_sprites)
			self.ghost_sprites.update(self.block_sprites)
			self.ghost2_sprites.update(self.block_sprites)
			self.ghost3_sprites.update(self.block_sprites)
			self.ghost4_sprites.update(self.block_sprites)

			# > If the player collides with one of the ghosts the game prints "Game Over"
			# > As an end game state
			# > In terms of how this completed in the code
			# > If there is one or more collisions (self.collisions+=1) then the code
			# > is told to print "gameover as a state"
			if pygame.sprite.collide_rect(self.ghost,self.snake) or pygame.sprite.collide_rect(self.ghost2,self.snake) or pygame.sprite.collide_rect(self.ghost3,self.snake) or pygame.sprite.collide_rect(self.ghost4,self.snake):
				self.collisions+=1
				print "Col+1",self.collisions
				if self.collisions==self.collisiontol:
					print "gameover"
					break
			else:
				self.collisions=0

				# > This is the point updating. An arduino scoreboard would
				# > Need to be plugged into this area, or at least it would be
				# > sensible to do so as this is the section that handles pelets collision
			"""Check for a snake collision/pellet collision"""
			lstCols = pygame.sprite.spritecollide(self.snake, self.pellet_sprites, True)

			# > The amount of pellets eaten.
			# > This is the "points" section
			"""Update the amount of pellets eaten"""
			self.snake.pellets = self.snake.pellets + len(lstCols)
			self.score=self.snake.pellets*10

			# > This displays the background and the maze
			"""Do the Drawing"""
			self.screen.blit(self.background, (0, 0))
			if pygame.font:
				font = pygame.font.Font(None, 36)
				text = font.render("Score %s" % self.score, 1, (255, 255, 255))
				textpos = text.get_rect(x=0)
				self.screen.blit(text, textpos)

			# > This draws the sprites and the pellets, this is going from
			# > Initializing to actually outputting.
			self.pellet_sprites.draw(self.screen)
			self.snake_sprites.draw(self.screen)
			self.ghost_sprites.draw(self.screen)
			self.ghost2_sprites.draw(self.screen)
			self.ghost3_sprites.draw(self.screen)
			self.ghost4_sprites.draw(self.screen)

			# > The display
			pygame.display.flip()

			# > Clock here as a timer for survival
			clock.tick(40)
			#print clock.get_fps()

			# > This is the death sound that plays during the "Gameover" state
		self.sounds['die'].play()

		# > This is loading the sprites
    def LoadSprites(self):
        """Load all of the sprites that we need"""
        """calculate the center point offset"""
        x_offset = (BLOCK_SIZE/2)
        y_offset = (BLOCK_SIZE/2)


        """Load the level"""
        level1 = level001.level()
        layout = level1.getLayout()
        img_list = level1.getSprites()


		# > The pellet sprites are grouped
		# > The block sprites are grouped
		# > The Wall sprites are grouped
		# > This is an example of a style of Object Oriented Programming, assigning
		# > The groups of items as a bluprint of one object to save typing the
		# > same code over and over.
        self.pellet_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.gwall_sprites = pygame.sprite.Group()

        for y in xrange(len(layout)):
            for x in xrange(len(layout[y])):
                """Get the center point for the rects"""
                centerPoint = [(x*BLOCK_SIZE)+x_offset,(y*BLOCK_SIZE+y_offset)]
                if layout[y][x]==level1.BLOCK:
                    self.block_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.BLOCK]))
                elif layout[y][x]==level1.GWALL:
                    self.gwall_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.GWALL]))
                elif layout[y][x]==level1.SNAKE:
                    self.snake = Snake(centerPoint,img_list[level1.SNAKE])
                elif layout[y][x]==level1.PELLET:
                    self.pellet_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.PELLET]))
                elif layout[y][x]==level1.GHOST:
                    self.ghost = Ghost(centerPoint,img_list[level1.GHOST])
                elif layout[y][x]==level1.GHOST2:
                    self.ghost2 = Ghost(centerPoint,img_list[level1.GHOST2])
                elif layout[y][x]==level1.GHOST3:
                    self.ghost3 = Ghost(centerPoint,img_list[level1.GHOST3])
                elif layout[y][x]==level1.GHOST4:
                    self.ghost4 = Ghost(centerPoint,img_list[level1.GHOST4])-
        """Create the Snake group"""
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))
	self.ghost_sprites = pygame.sprite.RenderPlain((self.ghost))
	self.ghost2_sprites = pygame.sprite.RenderPlain((self.ghost2))
	self.ghost3_sprites = pygame.sprite.RenderPlain((self.ghost3))
	self.ghost4_sprites = pygame.sprite.RenderPlain((self.ghost4))
if __name__ == "__main__":
	MainWindow = PyManMain(500,575)
	MainWindow.MainLoop()
