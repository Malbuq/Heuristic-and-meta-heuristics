import random
from FitnessEvaluator import SphereEvaluator, RastriginEvaluator, RosenbrockEvaluator
from FitnessSelector import FitnessProportionalSelector, FitnessTournamentSelector
from PopulationCrossover import OnePointCrossover, TwoPointsCrossover

def generate_initial_population(population_size, variable_bound, cromossom_width):
    population = []
    for i in range(population_size):
        population.append([random.randint(-variable_bound, variable_bound) for i in range(cromossom_width)])
    
    return population

def select_better_individuals(evaluator, population, selector):
    mating_probabilties = calculate_mating_probability(evaluator, population)
    return selector.select_population(population, mating_probabilties)

def calculate_mating_probability(FitnessEvaluator, population):
    probabilities = []

    total_fitness_score = FitnessEvaluator.calculate_total_fitness(population)
    
    for individual in population:
        current_probability = FitnessEvaluator.calculate_individual_fitness(individual) / total_fitness_score

        probabilities.append((1-current_probability))

    return probabilities

def mutate_population(population, mutation_prob, variable_bound):
    new_population = []

    for individual in population:
        for gene_index in range(len(individual)):
            if random.random() > mutation_prob:
                continue
            
            individual[gene_index] = random.uniform(-variable_bound, variable_bound)

        new_population.append(individual)

    return new_population

def select_best_individual_and_fitness(population, fitness_evaluator):
    best_individual = None
    best_fitness = 0
    for individual in population:
        curr_individual_fitness = fitness_evaluator.calculate_individual_fitness(individual)
        if best_individual is None or best_fitness > curr_individual_fitness:
            best_fitness = curr_individual_fitness
            best_individual = individual
    
    return best_individual, best_fitness

def GA_algorithm(variable_bound, population_size, generations, cromossom_width, crossover_probability, mutation_probability, evaluator, selector, crossover_type):
    population = generate_initial_population(population_size, variable_bound, cromossom_width)
    iterations = []
    best_fitnesses = []
    for i in range(generations - 1):
        better_individuals = select_better_individuals(evaluator, population, selector)
        new_population = crossover_type.crossover(better_individuals, crossover_probability)
        new_population = mutate_population(new_population, mutation_probability, variable_bound)
        _, best_fitness = select_best_individual_and_fitness(new_population, evaluator)
        population = new_population
        
        iterations.append(i)
        best_fitnesses.append(best_fitness)
    
    return (iterations, best_fitnesses)

def main():
    POPULATION_SIZE = 3
    GENERATIONS = 1000
    CROMOSSOM_WIDTH = 3
    CROSSOVER_PROBABILITY = 0.8
    MUTATION_PROBABILITY = 0.01

    problem_1 = (SphereEvaluator(), 100)
    problem_2 = (RastriginEvaluator(), 30)
    problem_3 = (RosenbrockEvaluator(), 5.12)
    problems = [problem_1, problem_2, problem_3]

    selectors = [FitnessProportionalSelector(), FitnessTournamentSelector()]
    crossovers = [OnePointCrossover(), TwoPointsCrossover()]
    
    for problem in problems:
        evaluator, variable_bound = problem
        for selector in selectors:
            for crossover_type in crossovers:
                print('===============================================================================================================')
                print(f'Best results using the {type(evaluator).__name__}, {type(selector).__name__}, {type(crossover_type).__name__}')
                print(GA_algorithm(variable_bound, POPULATION_SIZE, GENERATIONS, CROMOSSOM_WIDTH, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, evaluator, selector, crossover_type)[1])
