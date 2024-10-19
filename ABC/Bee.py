from abc import ABC, abstractmethod
import copy
import random


class Bee(ABC):
    def __init__(self, solution):
        self.solution = solution
    
    @abstractmethod
    def explore(self):
        pass

class EmployeedBee(Bee):
    def explore(self, solutions, fitnessEvaluator):
        randomSolutionIndex = random.randint(0, len(solutions) - 1)
        neighborSolution = solutions[randomSolutionIndex]

        randomDimensionIndex = random.randint(0, len(neighborSolution.position) - 1)

        currentSolutionDimensionValue = self.solution.position[randomDimensionIndex]
        neighborSolutionDimensionValue = neighborSolution.position[randomDimensionIndex]

        candidateSolution = copy.deepcopy(self.solution)
        candidateSolution[randomDimensionIndex] =  currentSolutionDimensionValue + random.uniform(-1, 1)*(currentSolutionDimensionValue - neighborSolutionDimensionValue)

        fitnessEvaluator.calculateSolutionFitness(candidateSolution)

        if candidateSolution.fitness < self.solution.fitness:
            self.solution = candidateSolution
            self.solution.improveAttemptCount = 0
            return

        self.solution.improveAttemptCount += 1