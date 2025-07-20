class NoActiveFileError(Exception):
    """Raised when no active file is connected to the session."""
    def __init__(self, message="No active file connected."):
        super().__init__(message)