from random import random, randrange

import pygame
from PIL import Image
from itertools import cycle

from Dino import Dino
from Obstacle import Obstacle
from Utils import Vector2

pygame.init()
my_font = pygame.font.SysFont("monospace", 15)

player_frame_1 = Image.open("resources.png").crop((1679, 2, 1765, 95)).convert("RGBA")
player_frame_1 = player_frame_1.resize(list(map(lambda x: x // 2, player_frame_1.size)))

player_frame_2 = Image.open("resources.png").crop((1855, 2, 1941, 95)).convert("RGBA")
player_frame_2 = player_frame_2.resize(list(map(lambda x: x // 2, player_frame_2.size)))

player_frame_3 = Image.open("resources.png").crop((1943, 2, 2029, 95)).convert("RGBA")
player_frame_3 = player_frame_3.resize(list(map(lambda x: x // 2, player_frame_3.size)))

player_frame_4 = Image.open("resources.png").crop((2030, 2, 2117, 95)).convert("RGBA")
player_frame_4 = player_frame_4.resize(list(map(lambda x: x // 2, player_frame_4.size)))

player_frame_5 = Image.open("resources.png").crop((2207, 2, 2323, 95)).convert("RGBA")
player_frame_5 = player_frame_5.resize(list(map(lambda x: x // 2, player_frame_5.size)))

player_frame_6 = Image.open("resources.png").crop((2324, 2, 2441, 95)).convert("RGBA")
player_frame_6 = player_frame_6.resize(list(map(lambda x: x // 2, player_frame_6.size)))

ground = Image.open("resources.png").crop((2, 102, 2401, 127)).convert("RGBA")
ground = ground.resize(list(map(lambda x: x // 2, ground.size)))
bg = Vector2(0, 150)
bg1 = Vector2(ground.size[0], 150)

cloud = Image.open("resources.png").crop((166, 2, 257, 29)).convert("RGBA")
cloud = cloud.resize(list(map(lambda x: x // 2, cloud.size)))
clouds = []

obstacle1 = Image.open("resources.png").crop((446, 2, 479, 71)).convert("RGBA")
obstacle1 = obstacle1.resize(list(map(lambda x: x // 2, obstacle1.size)))

obstacle2 = Image.open("resources.png").crop((446, 2, 547, 71)).convert("RGBA")
obstacle2 = obstacle2.resize(list(map(lambda x: x // 2, obstacle2.size)))

obstacle3 = Image.open("resources.png").crop((446, 2, 581, 71)).convert("RGBA")
obstacle3 = obstacle3.resize(list(map(lambda x: x // 2, obstacle3.size)))

obstacle4 = Image.open("resources.png").crop((653, 2, 701, 101)).convert("RGBA")
obstacle4 = obstacle4.resize(list(map(lambda x: x // 2, obstacle4.size)))

obstacle5 = Image.open("resources.png").crop((653, 2, 701, 101)).convert("RGBA")
obstacle5 = obstacle5.resize(list(map(lambda x: x // 2, obstacle5.size)))

obstacle6 = Image.open("resources.png").crop((851, 2, 950, 101)).convert("RGBA")
obstacle6 = obstacle6.resize(list(map(lambda x: x // 2, obstacle6.size)))

obs_images = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6]

gameDisplay = pygame.display.set_mode((600, 200))
clock = pygame.time.Clock()
pygame.display.set_caption('Chrome-Dino')
run_animation = cycle([player_frame_2]*400 + [player_frame_3]*400)
clock = pygame.time.Clock()
crashed = False
height = 110
speed = 400

# Start
dino = Dino(pos=(10, height))
dino.img = next(run_animation)
dino.ground_height = height
dino.rect = pygame.Rect(dino.position.x, dino.position.y, int(dino.img.size[0]*0.9), int(dino.img.size[1]*0.9))
# obst1 = Obstacle(pos=(randrange(600, 800), 125), images=obs_images, heights=[125, 125, 125, 115, 115, 115])
# obst2 = Obstacle(pos=(900, 1200, 125), images=obs_images, heights=[125, 125, 125, 115, 115, 115])
# obst3 = Obstacle(pos=(1300, 125), images=obs_images, heights=[125, 125, 125, 115, 115, 115])
obstacles = []  # obst1, obst2, obst3]

lastFrame = 0
speed_Vec = Vector2(0, 0)
current_time_to_spawn_obstacles = 1
current_time_to_spawn_clouds = 1
time_step = 1
GLOBAL_MULTIPLIER = 1
CHECK_FOR_COLLISION = True
SCORE = 0  # is float but will be displayed as int
DEAD = False
while not crashed:
    t = pygame.time.get_ticks()  # Get current time
    deltaTime = (t - lastFrame) * GLOBAL_MULTIPLIER / 1000.0  # Find difference in time and then convert it to seconds
    lastFrame = t  # set lastFrame as the current time for next frame.
    speed_Vec.x = -speed * deltaTime
    current_time_to_spawn_obstacles -= deltaTime
    current_time_to_spawn_clouds -= deltaTime

    gameDisplay.fill((255, 255, 255))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            crashed = True
        if not CHECK_FOR_COLLISION and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # reset the game
                pass

    # manage clouds
    if current_time_to_spawn_clouds <= 0:
        if len(clouds) > 0 and clouds[0].x <= -50:
            clouds[0].x = 700
            clouds[0].y = randrange(20, 40)
            clouds = clouds[1:] + [clouds[0]]
        else:
            new_vec = Vector2(700, randrange(20, 40))
            clouds.append(new_vec)
        current_time_to_spawn_clouds = randrange(20) / 3

    for cloud_vec in clouds:
        cloud_vec.x -= speed * deltaTime
        gameDisplay.blit(pygame.image.fromstring(cloud.tobytes(), cloud.size, 'RGBA'), cloud_vec.to_tuple())

    # manage the dino
    dino.update(deltatime=deltaTime, events=events)
    if DEAD:
        dino.img = player_frame_4
    else:
        dino.img = next(run_animation)
    player = gameDisplay.blit(pygame.image.fromstring(dino.img.tobytes(), dino.img.size, 'RGBA'),
                              (dino.position.x, dino.position.y))

    # manage obstacles
    if current_time_to_spawn_obstacles <= 0:
        if len(obstacles) > 0 and obstacles[0].position.x <= -50:
            obstacles[0].reset(700)
            obstacles = obstacles[1:] + [obstacles[0]]
        else:
            new_obst = Obstacle(pos=(700, 125), images=obs_images, heights=[125, 125, 125, 115, 115, 115])
            obstacles.append(new_obst)
        current_time_to_spawn_obstacles = (300 + random() * 100) / (speed + 0.0001)

    for obstacle in obstacles:
        obstacle.translate(speed_Vec)
        obstacle.rect.left = obstacle.position.x
        gameDisplay.blit(pygame.image.fromstring(obstacle.img.tobytes(), obstacle.img.size, 'RGBA'),
                         (obstacle.position.x, obstacle.position.y))

    # manage ground
    gameDisplay.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), bg.to_tuple())
    gameDisplay.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), bg1.to_tuple())
    bg.x -= speed * deltaTime
    bg1.x -= speed * deltaTime
    if bg.x <= -ground.size[0]:
        bg.x = 0
        bg1.x = ground.size[0]

    speed = (speed + 0.3 / time_step ** 0.5) * GLOBAL_MULTIPLIER
    time_step += 1

    # check for collision
    if CHECK_FOR_COLLISION and dino.rect.collidelist([obs.rect for obs in obstacles]) >= 0:
        GLOBAL_MULTIPLIER = 0
        CHECK_FOR_COLLISION = False
        DEAD = True

    if DEAD:
        label2 = my_font.render("DEAD :(", True, (50, 0, 0))
        gameDisplay.blit(label2, (270, 90))

    SCORE += 2.0 * deltaTime * GLOBAL_MULTIPLIER
    label = my_font.render(str(int(SCORE)), True, (0, 0, 0))
    gameDisplay.blit(label, (550, 0))

    pygame.display.update()  # updates the screen

    # clock.tick(60)
