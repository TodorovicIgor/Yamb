from AI.NeuralNetwork import NeuralNetwork
from random import random, randint


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
                ind1 = self.population[i]
                random_int = randint(0, int(len(self.population)/2))

                # while random_int == i:
                #     print(random_int)
                #     random_int = randint(0, (len(self.population)))

                # 2 different individuals from upper half
                new_individual = self.population[i].reproduce_with_crossover_and_mutation(ind1, self.population[random_int])
                self.population.append(new_individual)
                # print("inserted new individual with crossover, population size is", len(self.population))

    def evolve(self):
        """
        working out evolving
        """
        # exploring
        print("start", len(self.population))
        generation = 0
        while True:
            print("population size is", len(self.population))
            # first run
            if generation == 0:
                for individual in self.population:
                    individual.age += 1
                    individual.run()
            # sort
            self.sort_population()

            # remove
            self.remove_worst(int(len(self.population)/2))

            # reproduce
            self.reproduce_best(len(self.population))
            # run
            for individual in self.population:
                individual.age += 1
                individual.run()

            if len(self.population) == 1:
                return self.population[0]

        # # printing result
        # self.sort_population()
        # print("*******")
        # for individual in self.population:
        #     print(individual.fitness)
        # print("*******")
        # # annealing
        # while len(self.population) > 1:
        #     # reproduce
        #     for index, individual in enumerate(self.population[:]):  # iterating through copy of population
        #         if random() > 0.5:
        #             new_individual = individual.reproduce_with_mutation()
        #             self.population.pop(index)
        #             self.population.append(new_individual)
        #     # run
        #     for individual in self.population:
        #         individual.age += 1
        #         individual.run()
        #     # sort
        #     self.sort_population()
        #     # remove
        #     self.remove_worst(int(len(self.population) / 2))
        #     if len(self.population) == 1: break
        #     # reproduce
        #     # for index, individual in enumerate(self.population[:]):  # iterating through copy of population
        #     #     if random() > 0.5:
        #     #         new_individual = individual.reproduce_with_mutation()
        #     #         self.population.pop(index)
        #     #         self.population.append(new_individual)
        #


if __name__ == '__main__':
    # hidden_neurons, evolving_iterations, game_iterations, population_size
    trainer = Trainer(200, 2, 2, 3)
    best = trainer.evolve()
    print("Best score is", best.fitness, "age is", best.age)
    best.game.print_table()
