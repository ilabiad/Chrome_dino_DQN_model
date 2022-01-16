class Physics:
    gravity = 1500


class Vector2:
    """
    implement here operations on vec2
    """

    def __init__(self, x: object = 0, y: object = 0) -> object:
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y
