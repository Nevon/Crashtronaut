# -*- coding: utf-8 -*-

import pygame
import os
import sys
import math

from retrogamelib import gameobject
from retrogamelib import button
from retrogamelib.constants import *
from retrogamelib.util import *

class Collidable(gameobject.Object):
	
	def __init__(self):
		gameobject.Object.__init__(self, self.groups)
		self.offsetx = 0
		self.offsety = 0
		self.always_update = False
	
	def draw(self, surface, camera):
		surface.blit(self.image, (self.rect.x - camera.x + self.offsetx, 
			self.rect.y - camera.y + self.offsety))
			
	def on_collision(self, dx, dy):
		pass
	
	def get_surrounding(self, pos):
		center = (pos[0], pos[1])
		topleft	 = (pos[0]-1, pos[1]-1)
		midtop	  = (pos[0],   pos[1]-1)
		topright	= (pos[0]+1, pos[1]-1)
		midleft	 = (pos[0]-1, pos[1])
		midright	= (pos[0]+1, pos[1])
		bottomleft  = (pos[0]-1, pos[1]+1)
		midbottom   = (pos[0],   pos[1]+1)
		bottomright = (pos[0]+1, pos[1]+1)
		return (topleft, midtop, topright, midleft, midright,
			bottomleft, midbottom, bottomright, center)
	
	def move(self, dx, dy, tiles):
		sides = [0, 0, 0, 0]
		tile_pos = (self.rect.centerx//16, self.rect.centery//16)
		
		coltiles = []
		for pos in self.get_surrounding(tile_pos):
			if pos[0] > -1 and pos[0] < len(tiles[0]) and \
				pos[1] > -1 and pos[1] < len(tiles):
				tile = tiles[pos[1]][pos[0]]
				if isinstance(tile, Platform):
					coltiles.append(tile)
		
		if dx != 0:
			self.__move(dx, 0, coltiles)
		if dy != 0:
			self.__move(0, dy, coltiles)
	
	def __move(self, dx, dy, tiles):
		self.rect.x += dx
		self.rect.y += dy
		collided = False
		for tile in tiles:
			if self.rect.colliderect(tile.rect):
				if tile.slant == 0:
					self.rect_respond(dx, dy, tile)
				else:
					self.slant_respond(dx, dy, tile)
	
	def rect_respond(self, dx, dy, tile):
		if dx > 0:
			self.rect.right = tile.rect.left
		elif dx < 0:
			self.rect.left = tile.rect.right
		if dy > 0:
			self.rect.bottom = tile.rect.top
		elif dy < 0:
			self.rect.top = tile.rect.bottom
		self.on_collision(dx, dy)
	
	def slant_respond(self, dx, dy, tile):
		top = None
		if tile.slant < 0:
			if self.rect.left >= tile.rect.left:
				x = self.rect.left - tile.rect.left
				top = tile.rect.top+x-1
		if tile.slant > 0:
			if self.rect.right <= tile.rect.right:
				x = tile.rect.right - self.rect.right
				top = tile.rect.top+x-1
		if top:
			if self.rect.bottom > top:
				self.rect.bottom = top
				self.on_collision(0, dy)

class Player(Collidable):
	
	def __init__(self, fuel=100):
		Collidable.__init__(self)
	   
		self.right_images = [
			load_image("gfx/player-1.png"),
			load_image("gfx/player-2.png"),
			load_image("gfx/player-jet-1.png"),
			load_image("gfx/player-jet-2.png")
		]
		self.left_images = []
		for img in self.right_images:
			self.left_images.append(pygame.transform.flip(img, 1, 0))
		
		self.images = self.right_images
		self.image = self.images[0]
		self.rect = pygame.Rect(8, 16, 6, 16)
	   
		self.facing = 1
		self.jump_speed = 0
		self.frame = 0
		self.jumping = True
		self.flying = False
		self.offsetx = -5
		self.z = 0
		self.fuel = fuel
	
	def on_collision(self, dx, dy):		
		if dy > 0 or dy < 0:			
			self.jump_speed = 2	   
		if dy > 0:			
			self.jumping = False	

	def update(self, tiles):
		self.frame += 1
		imgframe = 0
		
		moving = False
		if button.is_held(LEFT):
			self.facing = -1
			moving = True
			self.move(-2, 0, tiles)
		if button.is_held(RIGHT):
			self.facing = 1
			moving = True
			self.move(2, 0, tiles)
		if button.is_pressed(A_BUTTON):
			if not self.jumping:
				play_sound("sfx/jump.ogg")
				self.jump_speed = -5
				self.jumping = True
		
		if self.jumping:
			if button.is_pressed(A_BUTTON) and self.jump_speed >= -2 and self.jump_speed <= 5:
				if button.is_held(A_BUTTON):
					self.flying = True
			if not button.is_held(A_BUTTON):
				self.flying = False
		else:
			self.flying = False
		
		if self.facing < 0:
			self.images = self.left_images
		else:
			self.images = self.right_images
		
		if moving:
			imgframe = self.frame/3%2
		if self.jumping:
			imgframe = 1
		if self.flying:
			imgframe = 2+(self.frame/2%2)
		
		self.image = self.images[imgframe]
		
		if not self.flying:
			if button.is_held(A_BUTTON) and not self.flying:
				self.jump_speed += 0.4
			else:
				self.jump_speed += 0.8
		else:
			if self.fuel <= 0:
				self.fuel = 0
				self.flying = False
			else:
				play_sound("sfx/burn.ogg", 0.2)
				self.jump_speed = -1
		if self.jump_speed > 5:
			self.jump_speed = 5
		
		self.move(0, self.jump_speed, tiles)
		if self.jump_speed > 3:
			self.jumping = True

class Platform(Collidable):
	
	def __init__(self, pos, imagepos, slant=0 ):
		Collidable.__init__(self)
		if type(imagepos) == tuple or type(imagepos) == list:
			self.sheet = load_image("gfx/platform.png")
			self.image = pygame.Surface((16, 16))
			self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
			self.image.blit(self.sheet, (-imagepos[0]*16, 
				-imagepos[1]*16, 16, 16))
		else:
			self.image = load_image(imagepos)
		self.rect = self.image.get_rect(topleft = pos)
		self.slant = slant  #1 for up slope right, -1 for down slope right
		self.z = -3
		
	def update(self, tiles):
		gameobject.Object.update(self)
		
class FallingPlatform(Platform):
	def __init__(self, pos, imagepos):
		Platform.__init__(self, pos, imagepos)
		self.timer = 0.5
		self.fall = False
		self.touched = False
		self.shake = 1
		
	def update(self, tiles):
		if self.timer <= 0:
			self.fall = True
		elif self.touched:
			self.timer -= 0.03
			if self.timer <= 0.2:
				if self.shake%2 == 0:
					self.rect.move_ip(1,0)
					self.shake -= 1
				else:
					self.rect.move_ip(-1,0)
					self.shake += 1
			
		if self.fall:
			self.jump_speed = 2
			self.rect.move_ip(0, self.jump_speed)
			if self.rect.top > 200:
				self.kill()
				
class MovingPlatform(Platform):
	def __init__(self, pos, axis=1, dir=1, length=16, speed=1):
		#axis: 1 = horizontal movement. 2 = vertical movement.
		#dir: 1 = right/down, 2 = left/up
		Platform.__init__(self, pos, "gfx/longblock.png")
		self.axis = axis
		self.dir = dir
		self.length = length
		self.speed = speed
		self.startx = self.rect.left
		self.starty = self.rect.top
		
	def update(self, tiles):
		if self.axis == 1:
			if self.dir == 1:
				if self.rect.left <= self.startx+self.length:
					self.rect.move_ip(self.speed, 0)
				else:
					self.dir = 2
			else:
				if self.rect.left >= self.startx:
					self.rect.move_ip(-self.speed, 0)
				else:
					self.dir = 1
		else:
			if self.dir == 1:
				if self.rect.top <= self.starty+self.length:
					self.rect.move_ip(0, self.speed)
				else:
					self.dir = 2
			else:
				if self.rect.top >= self.starty:
					self.rect.move_ip(0, -self.speed)
				else:
					self.dir = 1

class Baddie(Collidable):
	
	def __init__(self, pos):
		Collidable.__init__(self)
		self.left_images = [
			load_image("gfx/alien-1.png"), 
			load_image("gfx/alien-2.png"),
		]
		self.right_images = []
		for img in self.left_images:
			self.right_images.append(pygame.transform.flip(img, 1, 0))
		self.images = self.left_images
		
		self.image = self.images[0]
		self.rect = pygame.Rect(pos[0], pos[1], 8, 11)
		self.offsetx = -2
		self.frame = 0
		self.dx = -1
		self.z = -1
	
	def update(self, tiles):
		self.frame += 1
		self.image = self.images[self.frame/4%2]
		self.move(self.dx, 3, tiles)
		if self.dx > 0:
			self.images = self.right_images
		else:
			self.images = self.left_images
		
	def on_collision(self, dx, dy):
		if dx < 0 or dx > 0:
			self.dx = -self.dx

class Coin(Collidable):
	
	def __init__(self, pos):
		Collidable.__init__(self)
		self.images = [
			load_image("gfx/nut-1.png"), load_image("gfx/nut-2.png"),
			load_image("gfx/nut-3.png"), load_image("gfx/nut-4.png"),
		]
		self.image = self.images[0]
		self.rect = self.image.get_rect(topleft = pos)
		self.frame = 0
		self.always_update = True
		self.z = -2
	
	def update(self, tiles):
		self.frame += 1
		self.image = self.images[self.frame/4%4]

class ExtraLife(Collidable):
	def __init__(self, pos):
		Collidable.__init__(self)
		self.image = load_image("gfx/life.png")
		newpos = (pos[0]+self.image.get_width()/2, pos[1]+self.image.get_height()/2)
		self.rect = self.image.get_rect(topleft = newpos)
		self.z = -2
	def update(self, tiles):
		pass

class Points(Collidable):
	
	def __init__(self, score, pos, font):
		Collidable.__init__(self)
		self.image = font.render("%d" % score)
		self.rect = self.image.get_rect(center = pos)
		self.life = 10
	
	def update(self, tiles):
		self.life -= 1
		if self.life <= 0:
			self.kill()
		self.rect.move_ip(0, -1)

class Poof(Collidable):
	
	def __init__(self, pos):
		Collidable.__init__(self)
		self.images = [
			load_image("gfx/poof-1.png"), load_image("gfx/poof-2.png"),
			load_image("gfx/poof-3.png"),
		]
		self.image = self.images[0]
		self.rect = self.image.get_rect(center = pos)
		self.frame = 0
	
	def update(self, tiles):
		self.frame += 1
		self.image = self.images[self.frame/2%3]
		if self.frame >= 6:
			self.kill()

class Death(Collidable):
	
	def __init__(self, pos):
		Collidable.__init__(self)
		self.image = load_image("gfx/player-3.png")
		self.rect = self.image.get_rect(center = pos)
		self.x = self.rect.centerx
		self.jump_speed = -10
		self.life = 100
	
	def update(self, tiles):
		if self.rect.top > 200:
			self.kill()
		self.jump_speed += 0.5
		self.rect.move_ip(0, self.jump_speed)

class Spring(Collidable):
	
	def __init__(self, pos):
		Collidable.__init__(self)
		self.images = [
			load_image("gfx/spring-1.png"), load_image("gfx/spring-2.png"),
		]
		self.image = self.images[0]
		self.rect = self.image.get_rect(topleft = pos)
		self.bouncing = 0
	
	def bounce(self):
		self.bouncing = 2
	
	def update(self, tiles):
		if self.bouncing > 0:
			self.bouncing -= 1
			self.image = self.images[1]
		else:
			self.image = self.images[0]
