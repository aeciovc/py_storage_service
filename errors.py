class InvalidConfigError(Exception):
    
    MESSAGE = "Invalid Config!"

    def __init__(self):
        super().__init__(self.MESSAGE)