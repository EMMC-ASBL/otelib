class Pipe(object):
    """ Pipe object in a pipe-and-filter pattern """
    def __init__(self, i):
        self.input = i

    def get(self, sessionid):
        return self.input.get(sessionid)
