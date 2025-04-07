class MiniMaxNode:
    def __init__(self) -> None:
        self.is_max_player = False 
        self.move = None
        self.score = 0
        self.children = []
        self.choices = []
