import dansplotcore as dpc

class Interpolator:
    def run(self, xi, xf, iterations):
        self.x = xi
        return [self.step(xf) or self.x for i in range(iterations)]

class Linear(Interpolator):
    def __init__(self, m):
        self.m = m

    def step(self, xf):
        if xf >= self.x:
            self.x += min(xf - self.x, self.m)
        else:
            self.x -= max(xf - self.x, -self.m)

class Expo(Interpolator):
    def __init__(self, smooth):
        self.smooth = smooth

    def step(self, xf):
        self.x = self.x * self.smooth + xf * (1 - self.smooth)

class Momentum(Interpolator):
    def __init__(self, drag, mass):
        self.drag = drag
        self.mass = mass
        self.p = 0

    def step(self, xf):
        self.p += xf - self.x
        self.p /= self.drag
        self.x += self.p / self.mass

def combine(*interpolators):
    class Combined(Interpolator):
        def run(self, xi, xf, iterations):
            x = [xf] * iterations
            for i in interpolators:
                i.x = xi
                x = [i.step(j) or i.x for j in x]
            return x
    return Combined()

dpc.plot([
    i.run(0, 1, 4096)
    for i in [
        Linear(0.001),
        Expo(0.99),
        Momentum(10, 10),
        combine(Linear(0.001), Expo(0.99)),
        combine(Expo(0.99), Expo(0.99)),
        combine(Expo(0.99), Expo(0.99), Expo(0.99)),
    ]
])
