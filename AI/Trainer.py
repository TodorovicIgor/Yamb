from AI.NeuralNetwork import NeuralNetwork
from random import random, randint


class Trainer:

    def __init__(self, hidden_neurons, evolving_iterations, game_iterations, population_size):
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
            for i in range(int(num/2)):
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
        # exploring
        print("start", len(self.population))
        generation = 0
        while True:
            print("population size is", len(self.population))
            # first run
            if generation == 0:
                for individual in self.population:
                    individual.run()
                    generation += 1
            # sort
            self.sort_population()

            # printing
            for individual in reversed(self.population):
                print("fitness is %.3f, age is %d" % (individual.fitness, individual.age))

            # remove
            self.remove_worst(int(2*len(self.population)/3))

            # reproduce
            self.reproduce_best(len(self.population))

            # fill population
            self.fill_population()

            # run
            for individual in self.population:
                individual.age += 1
                individual.run()

            if len(self.population) == 1:
                return self.population[0]

        # exploring
        # print("start", len(self.population))
        # generation = 0
        # for i in range(1, self.population_size):
        #     print("population size is", len(self.population))
        #     # first run
        #     if generation == 0:
        #         for individual in self.population:
        #             individual.run()
        #     # sort
        #     self.sort_population()
        #
        #     # printing
        #     for individual in reversed(self.population):
        #         print("fitness is %.3f, age is %d" % (individual.fitness, individual.age))
        #
        #     # remove
        #     self.remove_worst(len(self.population)-i)
        #
        #     # reproduce
        #     self.reproduce_best(i)
        #
        #     # fill population
        #     self.fill_population()
        #
        #     # run
        #     for individual in self.population:
        #         individual.age += 1
        #         individual.run()
        #
        #     # if len(self.population) == 1:
        # return self.population[0]


if __name__ == '__main__':
    # hidden_neurons, evolving_iterations, game_iterations, population_size
    # trainer = Trainer(200, 2, 3, 300)  # kod kuce
    trainer = Trainer(200, 2, 2, 50)
    best = trainer.evolve()
    print("Best score is", best.fitness, "age is", best.age)
    best.game.print_table()
