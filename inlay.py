import copy


class Inlay:
    def __init__(self, x=None, y=None, value=None):
        self.x = x
        self.y = y
        self.value = value
        self.options = set([])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return " ".join(["(", str(self.x + 1) if self.x is not None else "x", ", ", str(self.y + 1) if self.y is not None else "y", ") = ",
                         str(self.value) if self.value is not None else "[]",
                         str(self.options) if self.options is not None else "{}"])

    def __str__(self):
        return " ".join(["(", str(self.x + 1) if self.x is not None else "x", " ", str(self.y + 1) if self.y is not None else "y", ") = ",
                         str(self.value) if self.value is not None else "[]",
                         str(self.options) if self.options is not None else "{}"])

    def __deepcopy__(self, memodict={}):
        new = Inlay()
        new.x = self.x
        new.y = self.y
        new.value = self.value
        new.options = set()
        new.options = copy.deepcopy(self.options)
        return new

    def is_empty(self):
        return self.value is None

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def unset(self):
        self.value = None

    def set_options(self, pv):
        self.options = pv

    def set_options_empty(self):
        self.options = set([])

    def get_options(self):
        return self.options

    def remove_option(self, v):
        try:
            self.options.remove(v)
        except KeyError:
            pass

    def add_option(self, v):
        self.options.add(v)
