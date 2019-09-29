from AI.NeuralNetwork import NeuralNetwork
from threading import Thread
from random import random, randint
from game import Yamb as yamb


class Trainer(Thread):

    def __init__(self, hidden_neurons, evolving_iterations, game_iterations, population_size):
        table = [yamb.Column(i) for i in range(6)]
        self.best_game = yamb.Yamb(table)
        self.game_iterations = game_iterations
        self.population_size = population_size
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
            for i in range(int(num)):
                ind1 = self.population[i]
                random_int = randint(0, int(len(self.population)/2))

                # while random_int == i:
                #     print("rand is ", random_int, "population size is", (len(self.population)))
                #     random_int = randint(0, (len(self.population)))

                # 2 different individuals from upper half
                new_individual = self.population[i].reproduce_with_crossover_and_mutation(ind1, self.population[random_int])
                self.population.append(new_individual)

                new_individual = self.population[i].reproduce_with_crossover_and_mutation(ind1,self.population[random_int])
                self.population.append(new_individual)

    def fill_population(self):
        while len(self.population) < self.population_size:
            self.population.append(NeuralNetwork(self.hidden_neurons, self.game_iterations))

    def evolve(self):
        """
        working out evolving
        """
        # working
        print("starting population size is", len(self.population))
        generation = 0
        for _ in range(self.iterations):
            print("population size is", len(self.population))
            # first run
            if generation == 0:
                for individual in self.population:
                    individual.run()
                    generation += 1
            # sort
            self.sort_population()

            # saving best game
            if self.population[0].game.get_table_sum() > self.best_game.get_table_sum():
                self.best_game = self.population[0].game

            # printing
            for individual in reversed(self.population):
                print("fitness is %.3f, age is %d" % (individual.fitness, individual.age))

            for individual in reversed(self.population):
                if individual.age > 1:
                    individual.game.print_table()
                    break

            # remove
            self.remove_worst(int(2*len(self.population)/3))

            # reproduce
            self.reproduce_best(len(self.population))

            # fill population
            # self.fill_population()

            # run
            for individual in self.population:
                individual.age += 1
                individual.run()

            # if len(self.population) == 1:
        return self.population[0]

    def run(self):
        self.evolve()


if __name__ == '__main__':
    # hidden_neurons, evolving_iterations, game_iterations, population_size
    trainer = Trainer([500, 200, 100], 10, 5, 200)  # kod kuce
    # trainer = Trainer(200, 2, 2, 50)
    best = trainer.evolve()
    print("Best score is", best.fitness, "age is", best.age)
    best.game.print_table()
