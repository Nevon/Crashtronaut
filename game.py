#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
import sys

from retrogamelib import display
from retrogamelib import button
from retrogamelib import clock
from retrogamelib import font
from retrogamelib import gameobject
from retrogamelib.constants import *

from retrogamelib.util import *
from objects import *
from tileengine import *
from levels import *

class Game(object):
	
	def __init__(self):
		
		self.objects = gameobject.Group()
		self.coins = gameobject.Group()
		self.extralives = gameobject.Group()
		self.baddies = gameobject.Group()
		self.dead = gameobject.Group()
		self.springs = gameobject.Group()
		self.FallingPlatforms = gameobject.Group()
		self.MovingPlatforms = gameobject.Group()
		
		Player.groups = [self.objects]
		Platform.groups = [self.objects]
		Coin.groups = [self.objects, self.coins]
		ExtraLife.groups = [self.objects, self.extralives]
		Points.groups = [self.objects]
		Poof.groups = [self.objects]
		Baddie.groups = [self.objects, self.baddies]
		Death.groups = [self.objects, self.dead]
		Spring.groups = [self.objects, self.springs]
		FallingPlatform.groups = [self.objects, self.FallingPlatforms]
		MovingPlatform.groups = [self.objects, self.MovingPlatforms]
		
		self.font = font.Font(GAMEBOY_FONT, (225, 225, 225))
		self.background = load_image("gfx/background.png")
		self.lifeicon = load_image("gfx/life.png")
		
		self.score = 0
		self.level = 1
		self.lives = 5
		self.fuel = 100
		self.show_win_screen = False
		
		self.engine = TileEngine()
		self.camera = pygame.Rect(0, 0, GBRES[0], GBRES[1])

	def start_level(self, level):
		self.show_win_screen = False
		if self.lives > 0:
			for obj in self.objects:
				obj.kill()
			self.player = Player(fuel=self.fuel)
			self.engine.parse_level(level)
			self.camera.centerx = self.player.rect.centerx
		else:
			self.won = False
			self.playing = False
			self.lose()

	def kill_player(self):
		if self.player.alive():
			self.lives -= 1
			self.player.kill()
			Death(self.player.rect.center)
			#pygame.mixer.music.stop()
			play_sound("sfx/die.ogg")
			
	def change_fuel(self, fuel, mode=1):
		self.fuel += fuel*mode
		self.player.fuel += fuel*mode
		if self.fuel > 100:
			self.fuel = 100
		elif self.fuel < 0:
			self.fuel = 0
		if self.player.fuel > 100:
			self.player.fuel = 100
		elif self.player.fuel < 0:
			self.player.fuel = 0

	def win(self):
		splash = display.get_surface().copy()
		pos = 0
		time = 50
		while 1:
			button.handle_input()
			clock.tick()
			if pos < 74:
				pos += 2
			else:
				time -= 1
				if time <= 0:
					break
			screen = display.get_surface()
			screen.blit(splash, (0, 0))
			ren = self.font.render("'Fraid there are no more levels yet.")
			screen.blit(ren, (80-ren.get_width()/2, pos))
			display.update()
		self.playing = False

	def lose(self):
		splash = display.get_surface().copy()
		pos = 0
		time = 50
		while 1:
			button.handle_input()
			clock.tick()
			if pos < 74:
				pos += 2
			else:
				time -= 1
				if time <= 0:
					break
			screen = display.get_surface()
			screen.blit(splash, (0, 0))
			ren = self.font.render("Game over!")
			screen.blit(ren, (80-ren.get_width()/2, pos))
			display.update()
		self.playing = False
		self.won = False

	def pause(self):
		pygame.mixer.music.pause()
		button.handle_input()
		play_sound("sfx/pause.ogg")
		while not button.is_pressed(START):
			button.handle_input()
			ren = self.font.render("PAUSED")
			screen = display.get_surface()
			screen.blit(ren, (80-ren.get_width()/2, 
				74-ren.get_height()/2))
			display.update()
		play_sound("sfx/pause.ogg")
		pygame.mixer.music.unpause()

	def loop(self):
		self.playing = True
		while self.playing:
			
		   self.handle_input()
		   self.update()
		   self.draw()
	
	def handle_input(self):
		button.handle_input()
		if button.is_pressed(START):
			self.pause()
		if button.is_pressed(A_BUTTON) and button.is_held(SELECT):
			self.playing = False
			
	def update(self):
		clock.tick()
		for object in self.objects:
			if (object.rect.right >= self.camera.left and \
				object.rect.left <= self.camera.right) or \
				object.always_update == True:
				object.update(self.engine.tiles)
				object.always_update = True
		
		# Move the camera
		self.camera.centerx = self.player.rect.centerx
		if self.camera.left < 0:
			self.camera.left = 0
		if self.camera.right > len(self.engine.tiles[0])*16:
			self.camera.right = len(self.engine.tiles[0])*16
		
		# Check if we won the level
		if self.player.rect.right > len(self.engine.tiles[0])*16:
			if len(LEVELS) == self.level-1:
				self.win()
			else:
				self.playing = False
		
		# Check if we fell off a cliff
		if self.player.rect.top > len(self.engine.tiles)*16:
			self.kill_player()
		
		# Make sure we don't move off the far left of the level
		if self.player.rect.left < 0:
			self.player.rect.left = 0
			
		#Subtract fuel if we're flying
		if self.player.flying:
			self.change_fuel(1, mode=-1)
		
		# Get rich quick!
		for c in self.coins:
			if self.player.rect.colliderect(c.rect):
				c.kill()
				self.score += 25
				self.change_fuel(1, mode=1)
				Poof(c.rect.center)
				play_sound("sfx/coin.ogg")
				
		# Extra lives!
		for l in self.extralives:
			if self.player.rect.colliderect(l.rect):
				l.kill()
				self.lives += 1
				Poof(l.rect.center)
				#Play 1-up sound
		
		# Will you live, or die?
		for b in self.baddies:
			if self.player.rect.colliderect(b.rect):
				if self.player.jump_speed > 0 and \
					self.player.rect.bottom < b.rect.top+10 and \
					b.alive():
					b.kill()
					Poof(b.rect.center)
					self.player.jump_speed = -3
					self.player.rect.bottom = b.rect.top-1
					play_sound("sfx/pounce.ogg")
					self.score += 50
					Points(50, b.rect.center, self.font)
				else:
					if b.alive():
						self.kill_player()
		
		# Boinnnng!
		for s in self.springs:
			if self.player.rect.colliderect(s.rect):
				if self.player.jump_speed > 0:
					self.player.jump_speed = -8
					if not s.bouncing:
						play_sound("sfx/bounce.ogg")
					s.bounce()
					self.player.jumping = True
					
		# Check if the player is standing on a collapsible platform!
		for p in self.FallingPlatforms:
			if p.touched:
				continue
			for i in range(p.rect.left, p.rect.left+p.rect.width):
				if self.player.rect.collidepoint(i , p.rect.top-1):
					p.touched = True
					break
		
		# Check if the player is on a horizontally moving platform
		for p in self.MovingPlatforms:
			if p.axis == 2:
				continue
			for i in range(p.rect.left, p.rect.left+p.rect.width):
				if self.player.rect.collidepoint(i , p.rect.top-1):
					if p.dir == 1:
						self.player.move(p.speed,0,self.engine.tiles)
					else:
						self.player.move(p.speed,0, self.engine.tiles)
	
	def draw(self):
		screen = display.get_surface()

		screen.fill(GB_SCREEN_COLOR)
		screen.blit(self.background, ((-self.camera.x/2) % 160, 0))
		screen.blit(self.background, (((-self.camera.x/2) - 160) % -160, 0))
		screen.blit(self.background, (((-self.camera.x/2) + 160) % 160, 0))

		for object in self.objects:
			object.draw(screen, self.camera)
		
		ren = self.font.render("score    level      x%d" % self.lives)
		screen.blit(ren, (4, 4))
		ren = self.font.render("%06d    %d-1" % (self.score, self.level-1))
		screen.blit(ren, (4, 14))
		screen.blit(self.lifeicon, (160-30, 2))
		ren = self.font.render("Fuel: %1.0d" % self.fuel + "%") 
		screen.blit(ren, (4, 134))
		
		if not self.player.alive() and not self.dead:
			self.start_level(LEVELS[self.level-2])
		
		display.update()
