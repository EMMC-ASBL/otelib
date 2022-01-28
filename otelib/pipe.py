class Pipe:
    """Pipe object in a pipe-and-filter pattern."""
    def __init__(self, i):
        self.input = i

    def get(self, session_id):
        return self.input.get(session_id)
