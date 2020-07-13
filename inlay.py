import copy


class Inlay:
    def __init__(self, x=None, y=None, value=None):
        self.x = x
        self.y = y
        self.value = value
        self.options = set([])

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
