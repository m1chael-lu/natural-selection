class Sun:
    def __init__(self):
        self.change = 1
        self.max = 1024
        self.inittime = self.max/256
        self.time = 1

    def update(self):
        if self.time == self.max:
            self.change = -1
        elif self.time == self.inittime:
            self.change = 1
        self.time += self.change