class Test:

    def __init__(self):
        self.x = [5]
        self.y = self.x


t = Test()

print(t.x, t.y)

t.x[0] += 1

print(t.x, t.y)
