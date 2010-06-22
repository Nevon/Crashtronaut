#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   menu.py

import time
import pygame
import os
import sys
from retrogamelib import display
from retrogamelib import button
from retrogamelib import clock
from retrogamelib import font
from retrogamelib import gameobject
from retrogamelib import dialog
from retrogamelib.constants import *
from retrogamelib.util import *

from game import *
from levels import *

def run_menu():
	play_music("sfx/title_screen.ogg")
	timer = 0
	game = Game()
	set_global_sound_volume(0.75)
	
	while True:
		clock.tick()
		button.handle_input()
		
		if button.is_pressed(START):
			
			play_music("sfx/ChibiNinja.ogg", -1)
			whitefont = font.Font(GAMEBOY_FONT, GB_SCREEN_COLOR)
			box = dialog.DialogBox((152, 46), (50, 50, 50), 
				GB_SCREEN_COLOR, whitefont)
			box.set_dialog([
				"GET THEM DARN ALIENS!"
			])
			box.set_scrolldelay(2)
			while not box.over():
				clock.tick()
				button.handle_input()
				if button.is_pressed(A_BUTTON):
					box.progress()
				screen = display.get_surface()
				screen.fill(GB_SCREEN_COLOR)
				screen.blit(game.background, (0, 0))
				box.draw(screen, (4, 4))
				display.update()
			
			
			game.won = True
			game.level = 1
			game.lives = 5
			game.score = 0

			# Play each level
			for lvl in LEVELS:
				game.start_level(lvl)
				game.level += 1
				game.loop()
				if not game.player.alive():
					break
			
			# If we got to the end of the game, display credits
			if game.won:
				pos = 144
				credits = [
					"Credits",
					"",
					"",
					"Programming by",
					"Tommy Brunn",
					"pymike",
					"saluk",
					"",
					"",
					"Art by",
					"Tommy Brunn",
					"",
					"",
					"Sound Mixing",
					"Tommy Brunn",
					"",
					"",
					"Music",
					"Eric Skiff",
					"thechad1138",
					"",
					"",
					"Special Thanks To",
					"SFXR by DrPetter",
					"pymike",
					"saluk",
					"",
					"",
					"",
					"",
					"",
					"",
					"",
					"",
					"",
					"",
					"",
					"",
					"",
					" Thanks for playing!!"]
				while pos > -144-(len(credits)*7):
					button.handle_input()
					if button.is_pressed(START):
						break
					screen = display.get_surface()
					screen.fill(GB_SCREEN_COLOR)
					screen.blit(game.background, (0, 0))
					
					clock.tick()
					pos -= 0.5
					y = 0
					for c in credits:
						ren = game.font.render(c)
						screen.blit(ren, (80-ren.get_width()/2, pos+y))
						y += 10
					display.update()
		   
			play_music("sfx/title_screen.ogg")
			
		#Draw main menu
		screen = display.get_surface()
		screen.fill(GB_SCREEN_COLOR)
		#screen.blit(load_image("gfx/menu.png"), (0, 0))
		ren = game.font.render("Press Start")
		timer += 1
		timer = timer % 30
		if timer < 15:
			screen.blit(ren, (80-ren.get_width()/2, 
				104-ren.get_height()/2))
		display.update()
