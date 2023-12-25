# Group Members: 
# Laurent Lorquet (Architect)
# Sebastian Rojas (Developer)
# Cedric Winter (Reporter)
# Professor: Dr. Oge Marques 
import random
import math

# This here defines the City and Population classes
class City:
    def __init__(self, city_id, x, y):
        self.city_id = city_id
        self.x = x
        self.y = y

class Population:
    def __init__(self, city_list, pop_size, routes=None):
        self.city_list = city_list
        self.pop_size = pop_size
        if routes is None:
            self.routes = self.initialize_population()
        else:
            self.routes = routes

    def initialize_population(self):
        # Here its creating a list of random routes
        routes = []
        for _ in range(self.pop_size):
            route = random.sample(self.city_list, len(self.city_list))
            routes.append(route)
        return routes

# Here its calculating the distance between two cities
def calculate_distance(city1, city2):
    return math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

# Here its calculating the total distance of a route
def calculate_route_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        distance += calculate_distance(route[i], route[i + 1])
    # (Something Cool imo) Here it adds distance from the last city to the starting city
    distance += calculate_distance(route[-1], route[0])
    return distance

# Here its selecting parents for crossover (a roulette wheel selection)
def select_parents(population):
    fitness_scores = [1 / calculate_route_distance(route) for route in population.routes]
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    return random.choices(population.routes, probabilities, k=2)

# Here it performs a mixed two-point crossover
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child1 = [None] * len(parent1)
    child2 = [None] * len(parent1)

    # Here its copying the selected segment from parent1 to child1 and parent2 to child2
    child1[start:end+1] = parent1[start:end+1]
    child2[start:end+1] = parent2[start:end+1]

    # Here its filling in the remaining cities from parent2 to child1 and from parent1 to child2
    remaining_cities1 = [city for city in parent2 if city not in child1]
    remaining_cities2 = [city for city in parent1 if city not in child2]
    index1, index2 = 0, 0
    for i in range(len(parent1)):
        if child1[i] is None:
            child1[i] = remaining_cities1[index1]
            index1 += 1
        if child2[i] is None:
            child2[i] = remaining_cities2[index2]
            index2 += 1

    return child1, child2

# Here it mutates a route by swapping two cities with a certain probability
def mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        index1, index2 = random.sample(range(len(route)), 2)
        route[index1], route[index2] = route[index2], route[index1]

# Here its creating a new generation of routes
def create_new_generation(population, mutation_rate):
    new_population = []

    # Here its keeping the best route from the previous generation (elitism)
    best_route = min(population.routes, key=calculate_route_distance)
    new_population.append(best_route)

    while len(new_population) < population.pop_size:
        parent1, parent2 = select_parents(population)
        child1, child2 = crossover(parent1, parent2)

        # Here its applying mutation with a certain probability
        mutate(child1, mutation_rate)
        mutate(child2, mutation_rate)

        new_population.extend([child1, child2])

    return Population(population.city_list, population.pop_size, routes=new_population)

# This is where we run the Genetic Algorithm
def run_genetic_algorithm(city_list, pop_size, max_generations, stagnation_limit, initial_mutation_rate):
    population = Population(city_list, pop_size)
    best_distance = float('inf')
    stagnation_count = 0

    for generation in range(max_generations):
        population = create_new_generation(population, initial_mutation_rate)
        best_route = min(population.routes, key=calculate_route_distance)
        current_distance = calculate_route_distance(best_route)

        if current_distance < best_distance:
            best_distance = current_distance
            stagnation_count = 0
        else:
            stagnation_count += 1

        if stagnation_count >= stagnation_limit:
            break

    best_route = min(population.routes, key=calculate_route_distance)
    return best_route, best_distance

# This is it in use
if __name__ == "__main__":
    # Here it defines a list of cities
    city_list = [City(city_id, random.randint(0, 200), random.randint(0, 200)) for city_id in range(10)]

    # Setting the GA parameters
    pop_size = 100
    max_generations = 200
    stagnation_limit = 25
    initial_mutation_rate = 0.1

    # Runing the GA
    best_route, best_distance = run_genetic_algorithm(city_list, pop_size, max_generations, stagnation_limit, initial_mutation_rate)

    print("Best Route:", [city.city_id for city in best_route])
    print("Best Distance:", best_distance)