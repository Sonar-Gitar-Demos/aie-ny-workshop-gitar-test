class BoxofficeError(Exception):
    """A request the box office refuses. The API returns it as {"error": message}."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status
