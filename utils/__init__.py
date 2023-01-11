class Point(complex):
    @property
    def x(self): return int(self.real)
    @property
    def y(self): return int(self.imag)
    def __lt__(self, o):
        return self.real < o.real or self.imag < o.imag
    def __add__(self, o) -> 'Point':
        r = super().__add__(o)
        return Point(r.real, r.imag)
    def __sub__(self, o) -> 'Point':
        r = super().__sub__(o)
        return Point(r.real, r.imag)