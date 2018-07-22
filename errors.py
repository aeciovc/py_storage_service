class InvalidConfigError(Exception):
    
    MESSAGE = "Invalid Config!"

    def __init__(self):
        super().__init__(self.MESSAGE)

class InvalidParamError(Exception):
    
    DEFAULT_MESSAGE = "Invalid Param: "

    def __init__(self, message):
        super().__init__(self.DEFAULT_MESSAGE + message)