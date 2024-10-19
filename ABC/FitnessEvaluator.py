import math
from abc import ABC, abstractmethod

class FitnessEvaluator(ABC):
    @abstractmethod
    def evaluateSolutions(self, solutions):
        pass

    @abstractmethod
    def calculateSolutionFitness(self, individual):
        pass


class SphereEvaluator(FitnessEvaluator):
    def evaluateSolutions(self, solutions):
        for solutionIndex in range(len(solutions)):
            solutions[solutionIndex].fitness = self.calculateSolutionFitness(solutions[solutionIndex])
    
    def calculateSolutionFitness(self, solution):
        fitness = 0

        for value in solution.position:
            fitness += value * value

        return fitness

class RastriginEvaluator(FitnessEvaluator):
    
    def calculate_total_fitness(self, population):
        total_fitness = 0
        
        for individual in population:
            total_fitness += self.calculate_individual_fitness(individual)

        return total_fitness
    
    def calculate_individual_fitness(self, individual):
        fitness = 0
        for gene in individual:
            fitness += self.calculate_gene_fitness(gene)
        
        return fitness
    
    def calculate_gene_fitness(self, gene):
        numero = 2*3.1415*gene
        p = (numero/180)*math.pi
        return (gene**2) - (10 * math.cos(p)) + 10
    
class RosenbrockEvaluator(FitnessEvaluator):

    def calculate_total_fitness(self, population):
        total_fitness = 0

        for individual in population:
            total_fitness += self.calculate_individual_fitness(individual)
        
        return total_fitness

    def calculate_individual_fitness(self, individual):
        fitness = 0

        for gene_index in range(len(individual) - 1):
            fitness += self.calculate_gene_fitness(individual,gene_index)
            
        return fitness

    def calculate_gene_fitness(self, individual, index):
        return 100*(individual[index+1] - individual[index]**2)**2 + (individual[index] - 1)**2