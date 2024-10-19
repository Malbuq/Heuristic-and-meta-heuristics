import copy
import random
from FitnessEvaluator import *

class Bee():
    def __init__(self, solution):
        self.solution = solution
    
    def explore(self, solutions, fitnessEvaluator):
        randomSolutionIndex = random.randint(0, len(solutions) - 1)
        neighborSolution = solutions[randomSolutionIndex]

        randomDimensionIndex = random.randint(0, len(neighborSolution.position) - 1)

        currentSolutionDimensionValue = self.solution.position[randomDimensionIndex]
        neighborSolutionDimensionValue = neighborSolution.position[randomDimensionIndex]

        candidateSolution = copy.deepcopy(self.solution)
        candidateSolution.position[randomDimensionIndex] =  currentSolutionDimensionValue + random.uniform(-1, 1)*(currentSolutionDimensionValue - neighborSolutionDimensionValue)

        candidateSolution.fitness = fitnessEvaluator.calculateSolutionFitness(candidateSolution)

        if candidateSolution.fitness < self.solution.fitness:
            self.solution = candidateSolution
            self.solution.improveAttemptCount = 0
            return

        self.solution.improveAttemptCount += 1

class Solution():
    def __init__(self, leftDomainBound, rightDomainBound, dimensionSize):
        self.position = [random.randint(leftDomainBound, rightDomainBound) for _ in range(dimensionSize)]
        self.fitness = 0
        self.improveAttemptCount = 0

def initializeSolutions(leftDomainBound, rightDomainBound, dimensionSize, solutionsLength):
    solutions = []

    solutions = [Solution(leftDomainBound, rightDomainBound, dimensionSize) for _ in range(solutionsLength)]

    return solutions

def initializeEmployeedBees(solutions):
    employeedBees = [Bee(solutions[solutionIndex]) for solutionIndex in range(len(solutions))]

    return employeedBees





def main():
    s1 = Solution(-10, 10, 3)
    s2 = Solution(-10, 10, 3)
    s3 = Solution(-10, 10, 3)

    solutions = [s1,s2,s3]

    SphereEvaluator().evaluateSolutions(solutions)

    empBee = Bee(s1)

    for _ in range(5):
        empBee.explore(solutions, SphereEvaluator())
        

main()