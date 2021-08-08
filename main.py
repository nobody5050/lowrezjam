import pygame, sys

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('lowrezjam 2021')
screen = pygame.display.set_mode((64, 64), pygame.SCALED)

player_image = pygame.image.load('./img/player/player.png').convert_alpha()

moving_left = False
moving_right = False

player_y_momentum = 0
air_timer = 0

true_scroll = [0,0]

level_number = 1

player_rect = pygame.Rect(24, 73, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

grass_image = pygame.image.load('./img/ground.png').convert_alpha()
dirt_image = pygame.image.load('./img/underground.png').convert_alpha()
stone_image = pygame.image.load('./img/stone.png').convert_alpha()
trunk_image = pygame.image.load('./img/wood.png').convert_alpha()

def load_map(path):
	f = open(path + '.txt','r')
	data = f.read()
	f.close()
	data = data.split('\n')
	game_map = []
	for row in data:
		game_map.append(list(row))
	return game_map

def collision_test(rect, tiles):
	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list

def move(rect, movement, tiles):
	collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
	rect.x += movement[0]
	hit_list = collision_test(rect, tiles)
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types['right'] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types['left'] = True
	rect.y += movement[1]
	hit_list = collision_test(rect, tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types['bottom'] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types['top'] = True
	return rect, collision_types

def draw_hardcoded():
	pygame.draw.rect(screen,(0, 255, 0),(63-scroll[0],57-scroll[1],10,10))

def advance_level():
	global game_map, level_number
	try:
		game_map = load_map('map' + str(level_number))
	except:
		print('no more levels!')
	level_number += 1
	return level_number

advance_level()

while True:

	screen.fill((34, 32, 52))

	true_scroll[0] += (player_rect.x-true_scroll[0]-32)/20
	true_scroll[1] += (player_rect.y-true_scroll[1]-32)/20
	scroll = true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

	tile_rects = []
	y = 0
	for layer in game_map:
		x = 0
		for tile in layer:
			if tile == '4':
				screen.blit(trunk_image, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '3':
				screen.blit(stone_image, (x*8-scroll[0],y*8-scroll[1]))
			if tile == '2':
				screen.blit(dirt_image,(x*8-scroll[0],y*8-scroll[1]))
			if tile == '1':
				screen.blit(grass_image,(x*8-scroll[0],y*8-scroll[1]))
			if tile != '0' and tile != '4':
				tile_rects.append(pygame.Rect(x*8,y*8,8,8))
			x += 1
		y += 1

	player_movement = [0, 0]
	if moving_right:
		player_movement[0] += 1
	if moving_left:
		player_movement[0] -= 1
	player_movement[1] += player_y_momentum
	player_y_momentum += 0.1
	if player_y_momentum > 1.5:
		player_y_momentum = 1.5

	player_rect, collisions = move(player_rect, player_movement, tile_rects)

	if collisions['bottom']:
		player_y_momentum = 0
		air_timer = 0
	else:
		air_timer += 0.05

	screen.blit(player_image,(player_rect.x-scroll[0],player_rect.y-scroll[1]))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_UP:
				if air_timer < 0.5:
					player_y_momentum = -1.5
					advance_level()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_LEFT:
				moving_left = False


	pygame.display.update()
	clock.tick(60)