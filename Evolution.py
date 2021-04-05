import random


class Minchen:

    def __init__(self, label='', color=0.0, mutation=0.1):
        self.age = 0
        self.label = label
        self.color = random.gauss(color, mutation)
        self.nutrient = 1

    def __str__(self):
        return str(self.label) + ': ' + str(self.color)

    def fuck(self):
        if random.random() > 0.7:
            offspring = int(random.random()*4)
            return 1, offspring
        return 0, 0

    def do_age(self):
        self.age += 1


class Wald:

    def __init__(self, n=0, color=0.0, mutation=0.1):
        self.minchens = list()
        self.n = n
        self.color = color
        self.mutation = mutation
        self.increment = 0.01
        self.season = 1500
        self.counter = 0
        self.eaten = 0
        self.aged = 0
        self.average = 0
        for i in range(n):
            self.minchens.append(Minchen(str(i), self.color, self.mutation))

    def __str__(self):
        output = 'This wood has the color ' + str(self.color) + '.\n'
        output += 'There are currently ' + str(len(self.minchens)) + ' Minchens.\n'
        output += 'This is season ' + str(self.counter) + '.\n'
        output += 'So far ' + str(self.eaten) + ' Minchens have been eaten.\n'
        output += 'So far ' + str(self.aged) + ' Minchens have died of old age.\n'
        output += 'The average color is ' + str(self.average) + '.\n'
        return output

    def change(self):
        return (self.color + self.increment) % self.season

    def bear(self):
        eaten = 0
        for min in self.minchens:
            ratio = min.color / self.color
            if 0.9 <= ratio <= 1.1:
                if random.random() > 0.3:
                    continue
            self.minchens.remove(min)
            eaten += 1
        self.eaten += eaten

    def propagate(self):
        for min in self.minchens:
            min.do_age()
            if min.age > 9:
                if random.random() < 0.7:
                    self.minchens.remove(min)
                    self.aged += 1
            if min.age > 1:
                fuck, offsprings = min.fuck()
                if fuck == 1:
                    for i in range(offsprings):
                        self.n += 1
                        self.minchens.append(Minchen(str(self.n), min.color))

    def evolve(self):
        self.color = self.change()
        self.bear()
        self.propagate()
        self.counter += 1
        sum = 0
        for min in self.minchens:
            sum += min.color
        try:
            self.average = sum / len(self.minchens)
        except:
            print('The world has ended.')

    def run(self, generations):
        for i in range(generations):
            if len(self.minchens) == 0:
                return True
            self.evolve()
            print(self)


Minchenwiese = Wald(100, 1)
Minchenwiese.run(100)