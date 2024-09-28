import random
from FitnessEvaluators import SphereEvaluator
from InertiaStrategys import ConstantIntertia, LinearDescentInertia

class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.fitness = 0
        self.best_position = position
        self.best_position_fitness = float('inf')

def generate_initial_particles(position_left_bound, position_right_bound, dimension, population_size):
    population = []
    for i in range(population_size):
        for j in range(dimension):
            #Mudança que o senhor pediu sobre velocidade
            particle = Particle([random.uniform(position_left_bound, position_right_bound) for i in range(dimension)], [random.uniform(position_left_bound, position_right_bound) for i in range(dimension)])
        population.append(particle)
    
    return population

def update_particles_position(population, left_bound, right_bound, general_best_position, intertiaStrategy):
    c1 = 1.5
    c2 = 1.5

    for index in range(len(population)):
        particle = population[index]


        for axis_index in range(len(particle.position)):
            w = intertiaStrategy.calculate_intertia(axis_index)

            new_axis_velocity = w*particle.velocity[axis_index] + \
                           c1*random.random()*(particle.best_position[axis_index] - particle.position[axis_index]) + \
                           c2*random.random()*(general_best_position[axis_index] - particle.position[axis_index])

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
    
    return best_particle

def main():
    
    NUMBER_ITERATIONS = 1000
    LEFT_BOUND = -100
    RIGHT_BOUND = 100

    initial_population = generate_initial_particles(-100, 100, 30, 1000)
    evaluator = SphereEvaluator()
    intertiaStrategy = LinearDescentInertia(0.2, 1, NUMBER_ITERATIONS)
    best_particle = initial_population[0]
    best_particle.fitness = float('inf')

    for iteration in range(NUMBER_ITERATIONS):
        best_particle_from_iteration = find_best_particle_from_iteration(initial_population, evaluator)

        if best_particle_from_iteration.fitness < best_particle.fitness: #Mudança que o senhor pediu sobre a melhor particula
            best_particle = best_particle_from_iteration

        update_particles_position(initial_population, LEFT_BOUND, RIGHT_BOUND, best_particle.position, intertiaStrategy)

        print("================================================================")
        print(f'Iteration: {iteration + 1}# Best score: {best_particle_from_iteration.fitness}.')
        
main()



