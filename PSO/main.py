import random
from FitnessEvaluators import SphereEvaluator
from InertiaStrategys import ConstantIntertia, LinearDescentInertia

class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = [0.2*element for element in position]
        self.best_position = position
        self.best_position_fitness = float('inf')

def generate_initial_particles(position_left_bound, position_right_bound, dimension, population_size):
    population = []
    for i in range(population_size):
        for j in range(dimension):
            particle = Particle([random.uniform(position_left_bound, position_right_bound) for i in range(dimension)])
        population.append(particle)
    
    return population

def update_particles_position(population, general_best_position, intertiaStrategy):
    c1 = 1.5
    c2 = 1.5

    for index in range(len(population)):
        particle = population[index]


        for axis_index in range(len(particle.position)):
            w = intertiaStrategy.calculate_intertia(axis_index)

            new_axis_velocity = w*particle.velocity[axis_index] + \
                           c1*random.random()*(particle.best_position[axis_index] - particle.position[axis_index]) + \
                           c2*random.random()*(general_best_position[axis_index] - particle.position[axis_index])

            particle.position[axis_index] = particle.position[axis_index] + new_axis_velocity 
            particle.velocity[axis_index] = new_axis_velocity

def find_best_general_position(population, evaluator):
    best_particle = None
    best_fitness = float('inf')
    
    for index in range(len(population)):
        particle = population[index]

        curr_particle_fitness = evaluator.calculate_individual_fitness(particle.position)

        if curr_particle_fitness < best_fitness:
            best_particle = particle
            best_fitness = curr_particle_fitness
        
        if curr_particle_fitness < particle.best_position_fitness:
            particle.best_position = particle.position
            particle.best_position_fitness = curr_particle_fitness
    
    return best_particle

def main():
    
    NUMBER_ITERATIONS = 100

    initial_population = generate_initial_particles(-100, 100, 100, 1000)
    evaluator = SphereEvaluator()
    intertiaStrategy = LinearDescentInertia(0.2, 1, NUMBER_ITERATIONS)

    for iteration in range(NUMBER_ITERATIONS):
        general_best_particle = find_best_general_position(initial_population, evaluator)
        update_particles_position(initial_population, general_best_particle.position, intertiaStrategy)

        print("================================================================")
        print(f'Iteration: {iteration + 1}# Best score: {evaluator.calculate_individual_fitness(general_best_particle.position)}.')
        
main()



