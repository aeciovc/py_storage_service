class InvalidConfigError(Exception):
    
    msg = "Invalid Config!"

    def __init__(self):
        super().__init__(self.msg)

class InvalidParamError(Exception):
    
    msg = "Invalid Param: "

    def __init__(self, message):
        super().__init__(self.msg + message)

class FileNotFoundError(Exception):
    
    msg = "File Not Found: "

    def __init__(self, message):
        super().__init__(self.msg + message)