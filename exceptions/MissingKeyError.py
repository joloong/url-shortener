class MissingKeyError(Exception):
    def __init__(self, key):
        self.key = key
        self.message = f"{self.key} is missing!"
        super().__init__(self.message)

    def __str__(self):
        return self.message
