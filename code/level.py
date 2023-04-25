import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water
from pytmx.util_pygame import load_pygame
from support import *

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()

		# setup player
		self.setup()
		self.overlay = Overlay(self.player)

	def setup(self):
		# Map objects setup
		tmx_data = load_pygame('../data/map.tmx')

		# House
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in  tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x, y, surf in  tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

		# Fence
		for x, y, surf in  tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

		# Water
		water_frames = import_folder('../graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)
		# Trees

		# Wildflowers


		# Player setup
		self.player = Player((640, 360), self.all_sprites)
		Generic(
			pos = (0,0),
			surf = pygame.image.load("../graphics/world/ground.png").convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def run(self,dt):
		self.display_surface.fill('black')
		# self.all_sprites.draw(self.display_surface)
		self.all_sprites.custom_draw(self.player)
		self.all_sprites.update(dt)
		self.overlay.display()


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	# updates camera as player moves
	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)