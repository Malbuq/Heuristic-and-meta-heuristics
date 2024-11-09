import math
from abc import ABC, abstractmethod

class FitnessEvaluator(ABC):
    def evaluateSolutions(self, solutions):
            for solutionIndex in range(len(solutions)):
                solutions[solutionIndex].fitness = self.calculateSolutionFitness(solutions[solutionIndex])

    @abstractmethod
    def calculateSolutionFitness(self, individual):
        pass


class SphereEvaluator(FitnessEvaluator):
    
    def calculateSolutionFitness(self, solution):
        fitness = 0

        for value in solution.position:
            fitness += value * value

        return fitness

class RastriginEvaluator(FitnessEvaluator):
        
    def calculateSolutionFitness(self, solution):
        fitness = 0
        for gene in solution.position:
            numero = 2*3.1415*gene
            p = (numero/180)*math.pi
            fitness += (gene**2) - (10 * math.cos(p)) + 10

        return fitness
    
class RosenbrockEvaluator(FitnessEvaluator):

    def calculateSolutionFitness(self, solution):
        fitness = 0

        for index in range(len(solution.position) - 1):
            fitness += 100*(solution.position[index+1] - solution.position[index]**2)**2 + (solution.position[index] - 1)**2

        return fitness 