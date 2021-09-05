class InvalidShortUrlError(Exception):
    def __init__(self, short_url):
        self.short_url = short_url
        self.message = f"{self.short_url} is taken!"
        super().__init__(self.message)

    def __str__(self):
        return self.message
