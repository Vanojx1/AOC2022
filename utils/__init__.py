class Point(complex):
    @property
    def x(self): return int(self.real)
    @property
    def y(self): return int(self.imag)
    def __lt__(self, o):
        return (self.y, self.x) < (o.y, o.x)
    def __add__(self, o) -> 'Point':
        r = super().__add__(o)
        return Point(r.real, r.imag)
    def __sub__(self, o) -> 'Point':
        r = super().__sub__(o)
        return Point(r.real, r.imag)
    
    def mdist(self, o):
        return abs(self.x-o.x) + abs(self.y-o.y)