class StringBuilder:
    def __init__(self, s=""):
        self.s = s

    def __iadd__(self, other):
        if type(other) is StringBuilder:
            self.s = "".join([self.s, other.s])
        elif type(other) is str:
            self.s = "".join([self.s, other])

        return self

    def __str__(self):
        return self.s
