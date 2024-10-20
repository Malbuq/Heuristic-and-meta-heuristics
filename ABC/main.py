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
        newValue = currentSolutionDimensionValue + random.uniform(-1, 1)*(currentSolutionDimensionValue - neighborSolutionDimensionValue)
        candidateSolution.position[randomDimensionIndex] =  newValue

        candidateSolution.fitness = fitnessEvaluator.calculateSolutionFitness(candidateSolution)

        if candidateSolution.fitness < self.solution.fitness:
            self.solution.position[randomDimensionIndex] = newValue
            self.solution.improvAttemptCount = 0
            return

        self.solution.improvAttemptCount += 1

class Solution():
    def __init__(self, leftDomainBound, rightDomainBound, dimensionSize):
        self.position = [random.randint(leftDomainBound, rightDomainBound) for _ in range(dimensionSize)]
        self.leftDomainBound = leftDomainBound
        self.rightDomainBound = rightDomainBound
        self.dimensionSize = dimensionSize
        self.fitness = 0
        self.improvAttemptCount = 0

def initializeSolutions(leftDomainBound, rightDomainBound, dimensionSize, solutionsLength):
    solutions = []

    solutions = [Solution(leftDomainBound, rightDomainBound, dimensionSize) for _ in range(solutionsLength)]

    return solutions

def initializeEmployeedBees(solutions):
    employeedBees = [Bee(solutions[solutionIndex]) for solutionIndex in range(len(solutions))]

    return employeedBees

def initializeOnlookerBees(solutions):
    onlookerBees = [Bee(None) for _ in range(len(solutions))]

    for index in range(len(onlookerBees)):
        onlookerBee = onlookerBees[index]

        populationFitness = sum([solution.fitness for solution in solutions])
        
        solutionsWeights = [1 - (solution.fitness/populationFitness) for solution in solutions]

        onlookerBee.solution = random.choices(solutions, solutionsWeights, k=1)[0]

    return onlookerBees

def employeedBeesExploration(employeedBees, solutions, fitnessEvaluator):
    for beeIndex in range(len(employeedBees)):
        employeedBees[beeIndex].explore(solutions, fitnessEvaluator)

def onlookerBeesExploration(onlookerBees, solutions, fitnessEvaluator):
    for beeIndex in range(len(onlookerBees)):
        onlookerBees[beeIndex].explore(solutions, fitnessEvaluator)

def scoutBeesExploration(bees, maxImprovTries):
    for index in range(len(bees)):
        currentPossibleScout = bees[index]

        if currentPossibleScout.solution.improvAttemptCount >= maxImprovTries:
            newRandomSolution = Solution(currentPossibleScout.solution.leftDomainBound, currentPossibleScout.solution.rightDomainBound, currentPossibleScout.solution.dimensionSize)
            currentPossibleScout.solution = newRandomSolution

def ABC_algorithm(colonySize, leftDomainBound, rightDomainBound, searchSpaceDimension, fitnessEvaluator, numberIterations, maxImprovTries):
    solutions = initializeSolutions(leftDomainBound, rightDomainBound, searchSpaceDimension, colonySize)
    fitnessEvaluator.evaluateSolutions(solutions)

    employeedBees = initializeEmployeedBees(solutions)
    onlookerBees = initializeOnlookerBees(solutions)

    result = {}

    for iteration in range(numberIterations):
        fitnessEvaluator.evaluateSolutions(solutions)

        result[iteration] = sum([solution.fitness for solution in solutions])

        employeedBeesExploration(employeedBees, solutions, fitnessEvaluator)
        onlookerBeesExploration(onlookerBees, solutions, fitnessEvaluator)

        scoutBees = employeedBees + onlookerBees
        scoutBeesExploration(scoutBees, maxImprovTries)

    return result

def selectBestSolutionFromIteration(solutions):
    bestSolution = None
    
    for solution in solutions:
        if bestSolution is None or solution.fitness < bestSolution.fitness:
            bestSolution = solution
    
    return bestSolution

def main():
    COLONY_SIZE = 100
    NUMBER_ITERATIONS = 1000
    LEFT_BOUND = -100
    RIGHT_BOUND = 100
    SEARCH_SPACE_DIMENSIONS = 30
    MAX_IMPROV_TRIES = COLONY_SIZE*SEARCH_SPACE_DIMENSIONS #Isso aqui é MUITO importante pro quao rapido o algoritimo converge

    fitnessEvaluator = SphereEvaluator()

    result = ABC_algorithm(COLONY_SIZE, LEFT_BOUND, RIGHT_BOUND, SEARCH_SPACE_DIMENSIONS, fitnessEvaluator, NUMBER_ITERATIONS, MAX_IMPROV_TRIES)
