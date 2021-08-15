import pygame, sys

clock = pygame.time.Clock()
dt = min(clock.tick(60)/1000, 0.016)

pygame.init()
pygame.display.set_caption('lowrezjam 2021')
screen = pygame.display.set_mode((64, 64), pygame.SCALED)
font = pygame.font.Font("font.ttf", 10)
timer = font.render("", True, (255, 255, 255))
talking_text = font.render("", True, (255, 255, 255))

level_number = 1

def title():
	title = True
	while title:

		image = pygame.image.load('./img/title.png')

		screen.blit(image, (0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					title = False
		pygame.display.update()
		dt = min(clock.tick(60)/1000, 0.016)

title()

dt = min(clock.tick(60)/1000, 0.016)
player_image = pygame.image.load('./img/player/player.png').convert_alpha()

moving_left = False
moving_right = False

player_y_momentum = 0
air_timer = 0

true_scroll = [0,0]

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
	global animation_frames
	animation_name = path.split('/')[-1]
	animation_frame_data = []
	n = 0
	for frame in frame_durations:
		animation_frame_id = animation_name + '_' + str(n)
		img_loc = path + '/' + animation_frame_id + '.png'
		# player_animations/idle/idle_0.png
		animation_image = pygame.image.load(img_loc).convert()
		animation_image.set_colorkey((255,255,255))
		animation_frames[animation_frame_id] = animation_image.copy()
		for i in range(frame):
			animation_frame_data.append(animation_frame_id)
		n += 1
	return animation_frame_data

def change_action(action_var,frame,new_value):
	if action_var != new_value:
		action_var = new_value
		frame = 0
	return action_var,frame
		

animation_database = {}

#animation_database['run'] = load_animation('player_animations/run',[7,7])
#animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])

player_rect = pygame.Rect(20, 65, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

game_map = {}

player_action = 'idle'
player_frame = 0
player_flip = False

grass_image = pygame.image.load('./img/ground.png').convert_alpha()
dirt_image = pygame.image.load('./img/underground.png').convert_alpha()
stone_image = pygame.image.load('./img/stone.png').convert_alpha()
trunk_image = pygame.image.load('./img/wood.png').convert_alpha()
plank_image = pygame.image.load('./img/plank.png').convert_alpha()
stair_image = pygame.image.load('./img/stair.png').convert_alpha()
stair_flipped = pygame.image.load('./img/stair_flipped.png').convert_alpha()

door_bottom = pygame.image.load('./img/door_bottom.png').convert_alpha()
door_top = pygame.image.load('./img/door_top.png').convert_alpha()


leaf_top_left = pygame.image.load('./img/leaf_twoSide_topleft.png').convert_alpha()
leaf_bottom_left = pygame.image.load('./img/leaf_twoSide_bottomLeft.png').convert_alpha()
leaf_top_right = pygame.image.load('./img/leaf_twoSide_topRight.png').convert_alpha()
leaf_bottom_right = pygame.image.load('./img/leaf_twoSide_bottomRight.png').convert_alpha()
leaf_bottom = pygame.image.load('./img/leaf_oneSide_bottom.png')
leaf_top = pygame.image.load('./img/leaf_oneSide_top.png')

tuft_image = pygame.image.load('./img/tuft.png').convert_alpha()
aaa_img = pygame.image.load('./img/aaaaaaaaaaaaaa.png').convert_alpha()
aaa2 = pygame.image.load('./img/aaaaaaaaaaaaaa2.png').convert_alpha()
interact_img = pygame.image.load('./img/interact.png').convert_alpha()
locked_dialouge = pygame.image.load('./img/locked.png').convert_alpha()
egg = pygame.image.load('./img/egg.png').convert_alpha()
win = pygame.image.load('./img/win.png').convert_alpha()

tile_index = {1:grass_image,
			2:dirt_image,
			3:stone_image,
			4:trunk_image
			}

showing_interact = False
showing_dialouge = False

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
	#pygame.draw.rect(screen,(0, 255, 0),(63-scroll[0],57-scroll[1],10,10))
	screen.blit(aaa_img, (50-scroll[0], 109-scroll[1]))
	screen.blit(aaa_img, (114-scroll[0], 109-scroll[1]))
	screen.blit(aaa2, (114-scroll[0], 234-scroll[1]))
	screen.blit(aaa2, (50-scroll[0], 234-scroll[1]))
	screen.blit(aaa2, (50-scroll[0], 234-scroll[1]))
	screen.blit(aaa2, (50-scroll[0], 234-scroll[1]))
	screen.blit(aaa2, (50-scroll[0], 234-scroll[1]))
	screen.blit(aaa2, (50-scroll[0], 234-scroll[1]))
	screen.blit(aaa2, (50-scroll[0], 234-scroll[1]))


def advance_level():
	global game_map, level_number
	try:
		game_map = load_map('map' + str(level_number))
	except:
		print('no more levels!')
	level_number += 1
	return level_number

advance_level()
Game = True

showing_dialouge = False

time_in_course = 0

while True:
	
	if level_number == 3 and player_rect.y > 200:
		advance_level()

	if player_rect.x > 223 and player_rect.x < 1306 and level_number == 4:
		time_in_course += dt
		timer = font.render(str(round(time_in_course, 2)), True, (255, 255, 255))

	if player_rect.x > 1306:
		win = True
		while win:
			image = pygame.image.load('./img/win.png')

			screen.blit(image, (0,0))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						title = False
			pygame.display.update()
			dt = min(clock.tick(60)/1000, 0.016)

	print(player_rect)
	
	if Game == True:
		if player_rect.x > 80 and player_rect.x < 200 and level_number == 2:
			Game = False
			advance_level()
	if Game == False:
		if player_rect.x < 80 or player_rect.x > 200:
			Game = True
	if Game == True and player_rect.y > 200 and player_rect.y < 201:
		advance_level()
	
	if level_number == 2 or level_number == 3:
		screen.fill((130, 139, 245))
	else:
		screen.fill((54, 58, 66))

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
			if tile == 'f':
				screen.blit(stair_flipped, (x*8-scroll[0], y*8-scroll[1]))
			if tile == 's':
				screen.blit(stair_image, (x*8-scroll[0], y*8-scroll[1]))
			if tile == 'p':
				screen.blit(plank_image, (x*8-scroll[0], y*8-scroll[1]))
			if tile == 'D':
				screen.blit(door_top, (x*8-scroll[0], y*8-scroll[1]))
			if tile == 'd':
				screen.blit(door_bottom, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '5':
				screen.blit(tuft_image, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '6':
				screen.blit(leaf_top_left, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '7':
				screen.blit(leaf_top_right, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '8':
				screen.blit(leaf_bottom_left, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '9':
				screen.blit(leaf_bottom_right, (x*8-scroll[0], y*8-scroll[1]))
			if tile == 'b':
				screen.blit(leaf_bottom, (x*8-scroll[0], y*8-scroll[1]))
			if tile == 't':
				screen.blit(leaf_top, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '4':
				screen.blit(trunk_image, (x*8-scroll[0], y*8-scroll[1]))
			if tile == 'q':
				screen.blit(trunk_image, (x*8-scroll[0], y*8-scroll[1]))
			if tile == '3':
				screen.blit(stone_image, (x*8-scroll[0],y*8-scroll[1]))
			if tile == '2':
				screen.blit(dirt_image,(x*8-scroll[0],y*8-scroll[1]))
			if tile == '1':
				screen.blit(grass_image,(x*8-scroll[0],y*8-scroll[1]))
			if tile != '0' and tile != '4' and tile != '5' and tile != '6' and tile != '7' and tile != '8' and tile != '9' and tile != 'b' and tile != 't' and tile != 'f' and tile != 's' and tile != 'd' and tile != 'D' and tile != 'p':
				tile_rects.append(pygame.Rect(x*8,y*8,8,8))
			x += 1
		y += 1

	player_movement = [0, 0]
	if moving_left:
		player_movement[0] -= 50 * dt
	if moving_right:
		player_movement[0] += 100 * dt
	player_movement[1] += player_y_momentum
	player_y_momentum += 10 * dt
	if player_y_momentum > 1.5:
		player_y_momentum = 1.5

	player_rect, collisions = move(player_rect, player_movement, tile_rects)

	if collisions['bottom']:
		player_y_momentum = 0
		air_timer = 0
	else:
		air_timer += 0.05

	screen.blit(player_image,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
	screen.blit(egg, (255-scroll[0], 211-scroll[1]))
	screen.blit(timer, (2, -2))
	screen.blit(talking_text, (2, 4))


	if player_rect.x > 28 and player_rect.x < 37 and showing_dialouge == False and player_rect.y == 65:
		screen.blit(interact_img, (46, 2))
		showing_interact = True
	if player_rect.x > 28 and player_rect.x < 37 and showing_dialouge == True and player_rect.y == 65:
		screen.blit(locked_dialouge, (-128, 1))
	
	if player_rect.x > 194 and player_rect.x < 207 and showing_interact == True:
		screen.blit(interact_img, (46, 2))
		talking = True
	
	draw_hardcoded()

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
					player_y_momentum = -150 * dt
			if event.key == pygame.K_ESCAPE:
				title()
			if event.key == pygame.K_x:
				if showing_interact == True and showing_dialouge == False:
					showing_dialouge = True
				if talking == True and player_rect.y == 457:
					talking_text = font.render("Goal: 18.22", True, (255, 255, 255))
			if event.key == pygame.K_p:
				player_rect.x = 194
				player_rect.y = 457
			if event.key == pygame.K_DOWN:
				if showing_dialouge == True:
					showing_dialouge = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_LEFT:
				moving_left = False

	#print("fps:" + str(clock.get_fps()))
	pygame.display.update()
	dt = min(clock.tick(60)/1000, 0.016)