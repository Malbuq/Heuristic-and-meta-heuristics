import random
from FitnessEvaluators import SphereEvaluator, RastriginEvaluator, RosenbrockEvaluator
from InertiaStrategys import ConstantIntertia, LinearDescentInertia
import copy

class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.fitness = 0
        self.best_position = position
        self.best_position_fitness = float('inf')
        self.left_friend = None
        self.right_friend = None

def generate_initial_particles(position_left_bound, position_right_bound, dimension, population_size):
    population = []
    for i in range(population_size):
        for j in range(dimension):
            particle = Particle([random.uniform(position_left_bound, position_right_bound) for i in range(dimension)], [random.uniform(position_left_bound, position_right_bound) for i in range(dimension)])
        population.append(particle)
    
    return population

def link_friends(population):
    population_size = len(population)

    for i in range(population_size):
        curr_particle = population[i]
        
        if i == 0:
            curr_particle.right_friend = population[i+1]
            curr_particle.left_friend = population[population_size - 1]
        elif i == population_size - 1:
            curr_particle.left_friend = population[i - 1]
            curr_particle.right_friend = population[0]
        else:
            curr_particle.left_friend = population[i-1]
            curr_particle.right_friend = population[i+1]

def select_friends_best_position(particle):
    best_particle = None
    for p in [particle.left_friend, particle, particle.right_friend]:
        if best_particle is None or p.best_position_fitness < best_particle.best_position_fitness:
            best_particle = p
    
    return best_particle.best_position

def update_particles_position(population, left_bound, right_bound, general_best_position, intertiaStrategy, iteration):
    c1 = 1.5
    c2 = 1.5
    social_bias = 0

    for index in range(len(population)):
        particle = population[index]

        for axis_index in range(len(particle.position)):
            w = intertiaStrategy.calculate_intertia(iteration)

            social_bias = c2*random.random()*(general_best_position[axis_index] - particle.position[axis_index])


            new_axis_velocity = w*particle.velocity[axis_index] + \
                           c1*random.random()*(particle.best_position[axis_index] - particle.position[axis_index]) + \
                           social_bias

            curr_new_axis_position = particle.position[axis_index] + new_axis_velocity 
            curr_new_axis_position = ensure_axis_position_is_inbounds(left_bound, right_bound, curr_new_axis_position) #Mudança que o senhor pediu sobre manter as posições nos limites

            particle.position[axis_index] = curr_new_axis_position
            particle.velocity[axis_index] = new_axis_velocity

def ensure_axis_position_is_inbounds(left_bound, right_bound, position):
    if position > 0:
        return min(right_bound, position)
    
    return max(left_bound, position)

def find_best_particle_from_iteration(population, evaluator):
    best_particle = None
    best_fitness = float('inf')
    
    for index in range(len(population)):
        particle = population[index]

        particle.fitness = evaluator.calculate_individual_fitness(particle.position)

        if particle.fitness < best_fitness:
            best_particle = particle
            best_fitness = particle.fitness
        
        if particle.fitness < particle.best_position_fitness:
            particle.best_position = particle.position
            particle.best_position_fitness = particle.fitness
    
    return copy.deepcopy(best_particle)

def PSO_algorithm(number_iterations, left_bound, right_bound, dimension, population_size, evaluator, inertiaStrategy):

    initial_population = generate_initial_particles(left_bound, right_bound, dimension, population_size)

    best_particle = initial_population[0]
    best_particle.fitness = float('inf')

    for iteration in range(number_iterations):
        best_particle_from_iteration = find_best_particle_from_iteration(initial_population, evaluator)

        if best_particle_from_iteration.fitness < best_particle.fitness:
            best_particle = (best_particle_from_iteration)

        update_particles_position(initial_population, left_bound, right_bound, best_particle.position, inertiaStrategy, iteration)

        print("================================================================")
        print(f'Iteration: {iteration + 1}# Best score: {best_particle_from_iteration.fitness}.')


def main():
    
    NUMBER_ITERATIONS = 500
    LEFT_BOUND = -100
    RIGHT_BOUND = 100
    DIMENSION = 30
    POPULATION_SIZE = 100

    evaluator = SphereEvaluator()
    inertiaStrategy = LinearDescentInertia(0.4, 0.9, NUMBER_ITERATIONS)

    PSO_algorithm(NUMBER_ITERATIONS, LEFT_BOUND, RIGHT_BOUND, DIMENSION, POPULATION_SIZE, evaluator, inertiaStrategy)
        
main()



