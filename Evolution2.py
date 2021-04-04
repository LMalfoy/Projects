import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


class Minchen:

    def __init__(self, label='', strength=1.0):
        self.label = label
        self.age = 0
        self.nutrients = 1
        self.strength = strength
        self.alive = True
        self.child_counter = 0
        self.children = []
        self.cause_of_death = 'alive'

    def __str__(self):
        return str(self.label) + ', age: ' + str(self.age) + ', nutrients: ' + str(self.nutrients) + ', strength: ' \
                + str(self.strength) + ', alive: ' + str(self.alive) + ', children: ' + str(self.child_counter) \
                + ', ' + self.cause_of_death

    def live(self):
        if self.nutrients > 0:
            self.alive = True
            self.nutrients -= 1
        else:
            self.alive = False
            self.cause_of_death = 'starved'

    def do_age(self):
        if self.age >= 10:
            if random.random() > 0.8:
                self.alive = False
                self.cause_of_death = 'old age'
        self.age += 1

    def eat(self):
        if self.nutrients <= 10:
            self.nutrients += 1

    def propagate(self):
        for i in range(5):
            if self.nutrients > 1 and random.random() > 0.3:
                self.nutrients -= 1
                child_name = self.label + '.' + str(self.child_counter)
                child_strength = random.gauss(self.strength, 0.1)
                child = Minchen(label=child_name, strength=child_strength)
                self.children.append(child)
                self.child_counter += 1

    def strength_roll(self):
        return random.random() * 5 + self.strength


class Bear(Minchen):

    def hunt(self):
        return


class Woods:

    def __init__(self, n):
        self.season = 0
        self.minchens = []
        self.grave = []
        self.food = 0
        # stats
        self.alive = n
        self.dead = 0
        self.starved = 0
        self.aged = 0

        for i in range(n):
            minchen = Minchen(str(i))
            self.minchens.append(minchen)
        self.take_stock()

    def grow(self, n):
        self.food += n

    def bury(self):
        for minchen in self.minchens:
            if not minchen.alive:
                self.minchens.remove(minchen)
                self.grave.append(minchen)
                self.dead += 1

    def take_stock(self):
        starve_counter = 0
        aged_counter = 0
        for minchen in self.grave:
            if minchen.cause_of_death == 'starved':
                starve_counter += 1
            if minchen.cause_of_death == 'old age':
                aged_counter += 1
        self.starved = starve_counter
        self.aged = aged_counter
        self.alive = len(self.minchens)

    def distribute_food(self):
        foodfields = []
        mixed_minchens = self.minchens.copy()
        random.shuffle(mixed_minchens)
        for i in range(self.food):
            foodfields.append([])
        while len(mixed_minchens) > 0:
            try:
                for j in range(len(foodfields)):
                    foodfields[j].append(mixed_minchens.pop())
            except:
                break
        for foodfield in foodfields:
            if len(foodfield) == 1:
                foodfield[0].eat()
                self.food -= 1
            elif len(foodfield) > 1:
                strength_rolls = []
                for minchen in foodfield:
                    strength_rolls.append(minchen.strength_roll())
                winner = strength_rolls.index(max(strength_rolls))
                foodfield[winner].eat()
                self.food -= 1

    def forward(self):
        self.bury()
        self.take_stock()
        self.grow(30)
        while self.food > 0:
            self.distribute_food()
        for minchen in self.minchens:
            minchen.live()
            minchen.do_age()
            minchen.propagate()
            for child in minchen.children:
                if child not in self.minchens:
                    self.minchens.append(child)


if __name__ == '__main__':
    wood = Woods(10)
    season = 10000

    seasonal_alive = []
    seasonal_dead = []
    dead_starved = []
    dead_aged = []
    seasonal_food = []
    average_strength = []
    for i in range(season + 1):
        seasonal_alive.append(wood.alive)
        seasonal_dead.append(wood.dead)
        dead_starved.append(wood.starved)
        dead_aged.append(wood.aged)
        seasonal_food.append(wood.food)
        strengths = []
        if len(wood.minchens) > 0:
            for minchen in wood.minchens:
                strengths.append(minchen.strength)
        else:
            strengths.append(0)
        average_strength.append(sum(strengths)/len(strengths))
        wood.forward()

    X = []
    X.extend(range(season+1))
    Y = [seasonal_alive, seasonal_food, average_strength]
    Yn = ['Population', 'Food', 'Avg. Strength']
    fig, ax = plt.subplots()
    for i in range(len(Y)):
        color = 'C' + str(i)
        ax.plot(X, Y[i], color=color, label=Yn[i])
    plt.legend()
    fig.savefig('figure.pdf')




