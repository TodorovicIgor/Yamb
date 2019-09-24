from AI.NeuralNetwork import NeuralNetwork
from random import random


class Trainer:

    def __init__(self, hidden_neurons, evolving_iterations, game_iterations, population_size):
        self.iterations = evolving_iterations
        self.hidden_neurons = hidden_neurons
        self.population = [NeuralNetwork(self.hidden_neurons, game_iterations) for _ in range(population_size)]

    def sort_population(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def remove_worst(self, num):
        if num >= len(self.population):
            print("Population size is", len(self.population), ", trying to remove", num, "individuals")
        else:
            for _ in range(num):
                self.population.pop()

    def reproduce_best(self, num):
        if num > len(self.population):
            print("Population size is", len(self.population), ", trying to reproduce", num, "individuals")
        else:
            for i in range(num):
                # TODO reproduce with crossover and mutation
                new_individual = self.population[i].reproduce_with_mutation()
                self.population.append(new_individual)

    def evolve(self):
        """
        Exploring phase:
            population is growing, chance to reproduce with both crossover and mutation is 100%
            number of worst individuals excluded after each iteration depend on number of passed iterations
        Annealing phase:
            TODO WRONG!!!
            population is losing its lower half after each iteration while upper half has 50% chance to
            reproduce with mutation and then die, population size is decreasing while the best ones have chance
            to maintain diversity and explore a little bit more
        """
        # exploring
        print("start", len(self.population))
        for i in range(self.iterations):
            # clear zeroes
            for index in reversed(range(len(self.population[:]))):  # iterating through copy of population
                if self.population[index].fitness == 0 and i != 0:
                    self.population.pop(index)
            # run
            for individual in self.population:
                individual.age += 1
                individual.run()
            # sort
            self.sort_population()
            # remove
            self.remove_worst(i)
            # reproduce
            self.reproduce_best(len(self.population))  # maybe not enough hardware resources
            print(len(self.population))
        # done exploring, population size is large enough

        # printing result
        # self.sort_population()
        # print("*******")
        # for individual in self.population:
        #     print(individual.fitness)
        # print("*******")
        # annealing
        while len(self.population) > 1:
            # clear zeroes
            for index in reversed(range(len(self.population[:]))):  # iterating through copy of population
                if self.population[index].fitness == 0:
                    self.population.pop(index)
            # run
            for individual in self.population:
                individual.age += 1
                individual.run()
            # sort
            self.sort_population()
            # remove
            self.remove_worst(int(len(self.population) / 2))
            if len(self.population) == 1: break
            # reproduce
            for index, individual in enumerate(self.population[:]):  # iterating through copy of population
                if random() > 0.5:
                    new_individual = individual.reproduce_with_mutation()
                    self.population.pop(index)
                    self.population.append(new_individual)
        if len(self.population) == 1:
            return self.population[0]


if __name__ == '__main__':
    # hidden_neurons, evolving_iterations, game_iterations, population_size
    trainer = Trainer(300, 2, 3, 500)
    best = trainer.evolve()
    print("Best score is", best.fitness)
    best.game.print_table()
