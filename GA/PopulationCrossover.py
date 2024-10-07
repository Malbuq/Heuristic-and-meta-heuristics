from abc import ABC, abstractmethod
import random

class PopulationCrossover(ABC):
    
    @abstractmethod
    def crossover(self, population, crossover_prob):
        pass


class OnePointCrossover(PopulationCrossover):

    def crossover(self, population, crossover_prob):
        population_size = len(population)
        cromossom_width = len(population[0])

        new_population = []

        population_is_odd = population_size % 2 != 0

        if population_is_odd:
            random_index = random.randint(0, population_size - 1)
            random_individual = population[random_index]
            new_population.append(random_individual)

        while len(new_population) < population_size:
            
            individual_A_index, individual_B_index = random.randint(0, population_size - 1), random.randint(0, population_size - 1)

            individual_A = population[individual_A_index]
            individual_B = population[individual_B_index]

            dont_crossover = random.random() > crossover_prob 

            if dont_crossover:
                new_population.extend([individual_A, individual_B])
                continue

            crossover_point = random.randint(0, cromossom_width - 1)

            A_B_child = individual_A[:crossover_point] + individual_B[crossover_point:]
            B_A_child = individual_B[:crossover_point] + individual_A[crossover_point:]

            new_population.extend([A_B_child, B_A_child])
        
        return new_population
    
class TwoPointsCrossover(PopulationCrossover):

    def crossover(self, population, crossover_prob):
        population_size = len(population)
        cromossom_width = len(population[0])

        new_population = []

        population_is_odd = population_size % 2 != 0

        if population_is_odd:
            random_index = random.randint(0, population_size - 1)
            random_individual = population[random_index]
            new_population.append(random_individual)

        while len(new_population) < population_size:
            
            individual_A_index, individual_B_index = random.randint(0, population_size - 1), random.randint(0, population_size - 1)

            individual_A = population[individual_A_index]
            individual_B = population[individual_B_index]

            dont_crossover = random.random() > crossover_prob 

            if dont_crossover:
                new_population.extend([individual_A, individual_B])
                continue

            crossover_start_point = random.randint(0, cromossom_width - 2)
            crossover_end_point = random.randint(crossover_start_point, cromossom_width - 1)

            A_B_child = individual_A[:crossover_start_point] + individual_B[crossover_start_point:crossover_end_point] + individual_A[crossover_end_point:]
            B_A_child = individual_B[:crossover_start_point] + individual_A[crossover_start_point:crossover_end_point] + individual_B[crossover_end_point:]

            new_population.extend([A_B_child, B_A_child])
        
        return new_population