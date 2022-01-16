from Utils import Vector2


class GameObject:

    def __init__(self, pos=(0, 0), rot=0, scale=(1, 1), children=list()):
        if children is None:
            children = []
        self.position = Vector2(*pos)
        self.rotation = rot
        self.scale = Vector2(*scale)
        self.children = children

    def update(self, deltatime=0.002):
        pass

    def translate(self, vec):
        self.position.x = self.position.x + vec.x
        self.position.y = self.position.y + vec.y
        for child in self.children:
            child.translate(vec)

    def rotate(self, ang):
        self.rotation += ang
        for child in self.children:
            child.rotate(ang)

    def add_child(self, child_object):
        if child_object not in self.children:
            self.children.append(child_object)
