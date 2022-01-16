from GameObject import GameObject
from Utils import Physics
import pygame


class Dino(GameObject):

    def __init__(self, img=None, pos=(0, 0), rot=0, scale=(1, 1)):
        self.img = img

        # game logic related
        self.y_speed = 0
        self.jump_height = 80
        self.ground_height = 0
        self.grounded = True
        self.rect = pygame.Rect(pos[0], pos[1], img.size[0], img.size[1]) if img is not None else None
        super(Dino, self).__init__(pos, rot, scale)

    def update(self, deltatime=0.002, events=None):
        self.y_speed += Physics.gravity * deltatime
        self.position.y += self.y_speed * deltatime
        if self.position.y > self.ground_height:
            self.position.y = self.ground_height
            self.y_speed = 1
            self.grounded = True

        if self.rect is not None:
            self.rect.top = self.position.y

        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.grounded and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    self.y_speed = -(self.jump_height * Physics.gravity * 2) ** 0.5
                    self.grounded = False

    def jump(self):
        if self.grounded:
            self.y_speed = -(self.jump_height * Physics.gravity * 2) ** 0.5
            self.grounded = False
