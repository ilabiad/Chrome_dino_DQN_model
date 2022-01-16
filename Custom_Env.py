import gym
from gym import Env, spaces
from gym.envs.classic_control import rendering
import numpy as np
from random import randrange, random
import pygame
from Utils import Vector2
from PIL import Image
from Dino import Dino
from Obstacle import Obstacle
from itertools import cycle

# <editor-fold desc="Load Images">
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

cloud = Image.open("resources.png").crop((166, 2, 257, 29)).convert("RGBA")
cloud = cloud.resize(list(map(lambda x: x // 2, cloud.size)))

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
# </editor-fold>

# <editor-fold desc="Global Variables">
run_animation = cycle([player_frame_2]*25 + [player_frame_3]*25)
obs_images = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6]
game_dimensions = (600, 200)
height = 110
initial_speed = 400
# </editor-fold>


class ChromeDinoEnv(Env):

    def __init__(self):
        pygame.init()
        self.my_font = pygame.font.SysFont("monospace", 15)
        # <editor-fold desc="game objects">
        # using surface not display bc we don't need pygame to display since it will be handled by gym viewer
        self.gameDisplay = pygame.Surface(game_dimensions)
        self.speed = initial_speed
        self.clouds = []
        self.dino = Dino(pos=(10, height))
        self.dino.img = next(run_animation)
        self.dino.ground_height = height
        self.dino.rect = pygame.Rect(self.dino.position.x, self.dino.position.y, int(self.dino.img.size[0] * 0.9),
                                     int(self.dino.img.size[1] * 0.9))
        self.obstacles = []

        self.bg = Vector2(0, 150)
        self.bg1 = Vector2(ground.size[0], 150)

        self.lastFrame = 0
        self.speed_Vec = Vector2(0, 0)
        self.current_time_to_spawn_obstacles = 1
        self.current_time_to_spawn_clouds = 1
        self.time_step = 1
        # global variables
        self.DEAD = False
        self.REWARD = 0
        self.GLOBAL_MULTIPLIER = 1
        self.CHECK_FOR_COLLISION = True
        # </editor-fold>

        self.action_space = spaces.Discrete(2)
        # The axis were swapped to match expected dimensions
        self.observation_space = spaces.Box(low=0, high=255, shape=(game_dimensions[1], game_dimensions[0], 3),
                                            dtype=np.uint8)
        self.state = None
        self.viewer = None

    def step(self, action):

        t = pygame.time.get_ticks()  # Get current time
        deltaTime = (t - self.lastFrame) * self.GLOBAL_MULTIPLIER / 1000.0  # Find difference in time and then
        # convert it to seconds
        self.lastFrame = t  # set lastFrame as the current time for next frame.
        self.speed_Vec.x = -self.speed * deltaTime
        self.current_time_to_spawn_obstacles -= deltaTime
        self.current_time_to_spawn_clouds -= deltaTime

        # events = pygame.event.get()

        # <editor-fold desc="cloud calculations">
        if self.current_time_to_spawn_clouds <= 0:
            if len(self.clouds) > 0 and self.clouds[0].x <= -50:
                self.clouds[0].x = 700
                self.clouds[0].y = randrange(20, 40)
                self.clouds = self.clouds[1:] + [self.clouds[0]]
            else:
                new_vec = Vector2(700, randrange(20, 40))
                self.clouds.append(new_vec)
            self.current_time_to_spawn_clouds = randrange(20) / 3

        for cloud_vec in self.clouds:
            cloud_vec.x -= self.speed * deltaTime
        # </editor-fold>

        # <editor-fold desc="dino update">
        if action == 1:
            self.dino.jump()
        self.dino.update(deltatime=deltaTime, events=[])
        if self.DEAD:
            self.dino.img = player_frame_4
        else:
            self.dino.img = next(run_animation)
        # </editor-fold>

        # <editor-fold desc="obstacles calculations">
        if self.current_time_to_spawn_obstacles <= 0:
            if len(self.obstacles) > 0 and self.obstacles[0].position.x <= -50:
                self.obstacles[0].reset(600)
                obstacles = self.obstacles[1:] + [self.obstacles[0]]
            else:
                new_obst = Obstacle(pos=(600, 125), images=obs_images, heights=[125, 125, 125, 115, 115, 115])
                self.obstacles.append(new_obst)
            self.current_time_to_spawn_obstacles = (initial_speed + 100 + random() * 200) / (self.speed + 0.0001)

        for obstacle in self.obstacles:
            obstacle.translate(self.speed_Vec)
            obstacle.rect.left = obstacle.position.x
        # </editor-fold>

        # <editor-fold desc="ground calculations">
        self.bg.x -= self.speed * deltaTime
        self.bg1.x -= self.speed * deltaTime
        if self.bg.x <= -ground.size[0]:
            self.bg.x = 0
            self.bg1.x = ground.size[0]
        # </editor-fold>

        self.speed = (self.speed + 3 / self.time_step ** 0.5) * self.GLOBAL_MULTIPLIER
        self.time_step += 1

        done = False
        # check for collision
        if self.CHECK_FOR_COLLISION and self.dino.rect.collidelist([obs.rect for obs in self.obstacles]) >= 0:
            self.GLOBAL_MULTIPLIER = 0
            self.CHECK_FOR_COLLISION = False
            self.DEAD = True
            done = True

        reward = 2.0 * deltaTime * self.GLOBAL_MULTIPLIER
        self.REWARD += reward

        self.redraw()

        return self.get_state(), reward, done, {}

    def render(self, mode='human', close=False):
        img = self.get_state()
        if mode == 'human':
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
        elif mode == 'rgb_array':
            return img

    def reset(self):
        # <editor-fold desc="game objects and variables">
        self.speed = initial_speed
        self.clouds = []
        self.dino = Dino(pos=(10, height))
        self.dino.img = next(run_animation)
        self.dino.ground_height = height
        self.dino.rect = pygame.Rect(self.dino.position.x, self.dino.position.y, int(self.dino.img.size[0] * 0.9),
                                     int(self.dino.img.size[1] * 0.9))
        self.obstacles = []

        self.bg = Vector2(0, 150)
        self.bg1 = Vector2(ground.size[0], 150)

        self.speed_Vec = Vector2(0, 0)
        self.current_time_to_spawn_obstacles = 1
        self.current_time_to_spawn_clouds = 1
        self.time_step = 1
        # global variables
        self.DEAD = False
        self.REWARD = 0
        self.GLOBAL_MULTIPLIER = 1
        self.CHECK_FOR_COLLISION = True
        # </editor-fold>

        self.redraw()
        self.lastFrame = pygame.time.get_ticks()
        return self.get_state()

    def redraw(self):
        self.gameDisplay.fill((255, 255, 255))
        for cloud_vec in self.clouds:
            self.gameDisplay.blit(pygame.image.fromstring(cloud.tobytes(), cloud.size, 'RGBA'), cloud_vec.to_tuple())

        self.gameDisplay.blit(pygame.image.fromstring(self.dino.img.tobytes(), self.dino.img.size, 'RGBA'),
                              (self.dino.position.x, self.dino.position.y))
        for obstacle in self.obstacles:
            self.gameDisplay.blit(pygame.image.fromstring(obstacle.img.tobytes(), obstacle.img.size, 'RGBA'),
                                  (obstacle.position.x, obstacle.position.y))
        self.gameDisplay.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), self.bg.to_tuple())
        self.gameDisplay.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), self.bg1.to_tuple())

        if self.DEAD:
            label2 = self.my_font.render("DEAD :(", True, (50, 0, 0))
            self.gameDisplay.blit(label2, (270, 90))

        label = self.my_font.render(str(int(self.REWARD)), True, (0, 0, 0))
        self.gameDisplay.blit(label, (550, 0))

        # pygame.display.update()

    def get_state(self):
        # maybe change pygame.display.get_surface() to self.gameDisplay
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            self.gameDisplay).astype(np.uint8))))
        return state


env = ChromeDinoEnv()
# test env
"""
episodes = 5
for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode, score))
env.close()
"""
