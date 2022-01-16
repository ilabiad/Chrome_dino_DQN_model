from GameObject import GameObject
from random import randrange
from pygame import Rect


class Obstacle(GameObject):

    def __init__(self, images=None, heights=None, pos=(0, 0), rot=0, scale=(1, 1)):
        assert len(images) == len(heights), "images and heights should have the same length"
        self.images = images
        self.heights = heights
        index = randrange(len(images))
        self.img = images[index] if images is not None else None
        self.height = heights[index] if heights is not None else None
        self.rect = Rect(pos[0], pos[1], self.img.size[0], self.img.size[1]) if self.img is not None else None
        super(Obstacle, self).__init__((pos[0], self.height), rot, scale)

    def reset(self, x_pos):
        index = randrange(len(self.images))
        self.img = self.images[index] if self.images is not None else None
        self.height = self.heights[index] if self.heights is not None else None
        self.position.x = x_pos
        self.position.y = self.height
        self.rect.update(self.position.x, self.position.y, self.img.size[0],
                         self.img.size[1]) if self.img is not None else None
