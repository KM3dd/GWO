import numpy as np
import random
from matrice import A_53 as A
from RS100 import tsp_recuit_simule
from AG import GA
class GreyWolfOptimizer:
    def __init__(self, graph, num_wolves, max_iterations):
        self.graph = graph
        self.num_wolves = num_wolves
        self.max_iterations = max_iterations
        self.num_cities = len(graph)
        self.alpha = None
        self.beta = None
        self.delta = None
        self.positions = None

    def initialize_population(self):
        self.positions = np.zeros((self.num_wolves, self.num_cities), dtype=int)
        # initial_pop=GA(self.num_wolves,self.num_wolves/2,0.5,0.1,100)
        # print(initial_pop)
        for i in range(self.num_wolves):
            # self.positions[i] = np.array(initial_pop[i][1])[:-1]
            self.positions[i][0] = 0
            remaining_cities = list(range(1, self.num_cities))
            random.shuffle(remaining_cities)
            self.positions[i][1:] = remaining_cities
        # GA(200,140,0.5,0.1,300)
        # print(self.positions)

    def calculate_fitness(self, position):
        distance = 0
        for i in range(self.num_cities - 1):
            distance += self.graph[position[i]][position[i + 1]]
        distance += self.graph[position[self.num_cities - 1]][position[0]]
        return distance

    def update_alpha_beta_delta(self):
        fitness = [self.calculate_fitness(position) for position in self.positions]
        sorted_fitness_indices = np.argsort(fitness)

        self.alpha = self.positions[sorted_fitness_indices[0]]
        self.beta = self.positions[sorted_fitness_indices[1]]
        self.delta = self.positions[sorted_fitness_indices[2]]
        # print(fitness[sorted_fitness_indices[0]])
    def update_positions(self, iteration):
        a = 1 - (2 * iteration / 10)
        for i in range(1,self.num_wolves):
            self.positions[i][0] = 0
            visited = set()
            visited.add(0)

            for j in range(1, self.num_cities):
                r1 = random.random()
                r2 = random.random()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * self.alpha[j] - self.positions[i][j])
                X1 = self.alpha[j] - A1 * D_alpha

                r1 = random.random()
                r2 = random.random()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * self.beta[j] - self.positions[i][j])
                X2 = self.beta[j] - A2 * D_beta

                r1 = random.random()
                r2 = random.random()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * self.delta[j] - self.positions[i][j])
                X3 = self.delta[j] - A3 * D_delta

                new_position = (X1 + X2 + X3) / 3

                new_position = round(max(0, min(new_position, self.num_cities - 1)))

                if new_position in visited:
                    self.positions[i][j] = -1
                else:
                    self.positions[i][j] = new_position
                    visited.add(new_position)

            missing_cities = set(range(self.num_cities)) - visited
            missing_cities_list = list(missing_cities)

            for j in range(1,self.num_cities):
                if self.positions[i][j] == -1:
                     current_city = self.positions[i][j-1]

                    # Calculate the distances from the current city to all missing cities
                     distances_to_missing_cities = [A[current_city][m_city] for m_city in missing_cities_list]

                    # Find the index of the nearest city
                     nearest_city_index = np.argmin(distances_to_missing_cities)

                    # Get the nearest city from the missing cities list
                     nearest_city = missing_cities_list[nearest_city_index]

                     self.positions[i][j] = nearest_city
                     visited.add(nearest_city)
                     missing_cities_list.pop(nearest_city_index)
    def AgPositions(self):
        intermidPop=[]
        for position in self.positions:
            pos=list(position)
            pos.append(0)
            intermidPop.append([self.calculate_fitness(position),pos])
            
            # np.append(self.positions[i],self.positions[i][0])
        initial_pop=GA(intermidPop,self.num_wolves/2,0.7,0.05,100)
        for i in range(len(initial_pop)):
            self.positions[i] = np.array(initial_pop[i][1])[:-1]                  
    def rsPositions(self):
        for i in range(self.num_wolves):

            solution,cost=tsp_recuit_simule(A,list(self.positions[i]),self.calculate_fitness(self.positions[i]),nb_iter=200 )
            # print(solution)
            # print(self.positions[i])
            if cost<self.calculate_fitness(self.positions[i]):
                self.positions[i]=solution
    def optimize(self):
        best_fitness = float('inf')
        best_position = None 
        self.initialize_population()
        i=0
        for iteration in range(self.max_iterations):
            print('Gwo ',iteration)
            self.update_alpha_beta_delta()
            self.update_positions(iteration)
                
            # self.rsPositions()
            # print(self.positions)
            print('------------------------------------------')
            i=i+1
            for position in self.positions:
                fitness = self.calculate_fitness(position)
                
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_position = position
                    i=0
            if(i==100):
                self.AgPositions()
                i=0
            print(best_fitness)
        self.AgPositions()
        for position in self.positions:
                fitness = self.calculate_fitness(position)
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_position = position
        return list(best_position), best_fitness

graph = A
optimizer = GreyWolfOptimizer(graph, num_wolves=100, max_iterations=1000)
best_position, best_fitness = optimizer.optimize()
# solution,cost=tsp_recuit_simule(A,best_position,best_fitness,nb_iter=12000 )
print("Best path:", best_position)
print("Best fitness:", best_fitness)