from abc import ABC, abstractmethod
import random

class FitnessSelector(ABC):

    @abstractmethod
    def select_population(self, population, probabilities):
        pass

class FitnessProportionalSelector(FitnessSelector):
    def select_population(self, population, probabilities):
        probabilities = [prob for prob in probabilities]

        new_population_size = len(population)

        new_population = random.choices(population, weights=probabilities, k=new_population_size)

        return new_population 

class FitnessTournamentSelector(FitnessSelector):
    def select_population(self, population, probabilties):
        population_size = len(population)
        new_population = []
        
        for i in range(population_size):
            A_index = random.randint(0, population_size - 1)
            B_index = random.randint(0, population_size - 1)

            if probabilties[A_index] > probabilties[B_index]:
                new_population.append(population[A_index]) 
            elif probabilties[A_index] <= probabilties[B_index]:
                new_population.append(population[B_index])

        return new_population