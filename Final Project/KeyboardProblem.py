from KeyboardFitnessEvaluator import associateCharsWithKeys, initializeFingers, findingBestFinger, indexToCoordinates, standardKeyboard
from KeyboardPrinter import printKeyboard
import math
import string
from pymoo.core.problem import Problem
from pymoo.problems.single.flowshop_scheduling import create_random_flowshop_problem
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.termination.default import DefaultSingleObjectiveTermination
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

characteres = string.ascii_lowercase + "ç,.´~"

def calculateKeyboardFitness(keyboard, language):
    cost = 0

    input_text_path = f"Final Project\{language}-Preprocessed-file"

    charsToIgnore = [' ', '-', '\n', '?', '!', ':', ';', '"', "’", "'"]

    with open(input_text_path,'r', encoding="utf-8") as text:
        for line in text:
            for char in line:
                if char in charsToIgnore:
                    continue  
                cost += charCost(keyboard, char)

    return cost

def charCost(keyboard, letter):
    cost = 0
    letterToIndex = associateCharsWithKeys()
    fingers = initializeFingers()

    letterIndexInKeyboard = np.where(keyboard == letterToIndex[letter])[0][0]

    choosenFinger = findingBestFinger(fingers, letterIndexInKeyboard)
    
    currLetterPos = indexToCoordinates(letterIndexInKeyboard)
    fingerPos = indexToCoordinates(choosenFinger.currKeyIndex)
    
    choosenFinger.currKeyIndex = letterIndexInKeyboard

    cost += math.dist(currLetterPos, fingerPos)

    return cost

class KeyboardProblem(Problem):
    def __init__(self, language):
        super().__init__(n_var=len(characteres), n_obj=1, xl=0, xu=len(characteres) - 1, type_var=int)
        self.language = language

    def _evaluate(self, X, out, *args, **kwargs):
        results = np.array([calculateKeyboardFitness(x, self.language) for x in X])
        out["F"] = results


def runKeyboardSolver(language, generations, populationSize):
    algorithm = GA(
        pop_size=populationSize,
        eliminate_duplicates=True,
        sampling=PermutationRandomSampling(),
        mutation=InversionMutation(),
        crossover=OrderCrossover()
    )

    res = minimize(
        KeyboardProblem(language),
        algorithm,
        DefaultSingleObjectiveTermination(period=100, n_max_gen=generations),
        seed=1,
        save_history=True
    )

    # fitness_over_gens = [entry.opt[0].F[0] for entry in res.history]

    # plt.plot(range(len(fitness_over_gens)), fitness_over_gens, marker='o')
    # plt.title("Fitness Over Generations")
    # plt.xlabel("Generation")
    # plt.ylabel("Fitness (Cost)")
    # plt.grid()
    # plt.show()

    best_configuration = res.X
    best_fitness = res.F[0]
    first_gen_fitness = res.history[0].opt[0].F[0]

    best_keyboard = [characteres[i] for i in best_configuration]

    printKeyboard(keyboard_layout=best_keyboard, language=language, fitness=best_fitness, initial_fitness=first_gen_fitness)

    print("Best Fitness Value (Cost):", best_fitness)


runKeyboardSolver(language="EN", generations=10, populationSize=10)

