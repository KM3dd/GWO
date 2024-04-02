import random
import numpy as np
import copy
import time
from matrice import A_53 as A
import matplotlib.pyplot as plt

def cost(indiv):
    f = 0
    for i in range(len(indiv) - 1):
        if A[indiv[i]][indiv[i + 1]] == 0:
            return 0
        f += A[indiv[i]][indiv[i + 1]]
    return f

def generatePopulation(N):
    population = []
    cities = np.arange(1,len(A)).tolist()
    while(len(population) < N):
        c = cities.copy()
        random.shuffle(c)
        fullPath = [0] +  c + [0]
        pathCost = cost(fullPath)
        if pathCost != 0:
            population.append([pathCost,fullPath])
    return population

def rw_selection(population,Nprime):  # Selection a la roulette
    cost = [max(population)[0] - x[0] for x in population]
    sum_score = sum(cost)
    indexes = np.random.choice(len(population),size=Nprime,replace=False, p=[x / sum_score for x in cost]).tolist()
    return [population[i] for i in indexes]

def tnm_selection(population, Nprime):  # tournament selection
    selectedIndexes = []
    selectedPopulation = []
    while len(selectedPopulation) < Nprime:
        ind1 = np.random.randint(len(population))
        # check if ind1 has already been selected
        while ind1 in selectedIndexes:
            ind1 = np.random.randint(len(population))
        ind2 = np.random.randint(len(population))
        # check if ind2 has already been selected
        while ind2 in selectedIndexes:
            ind2 = np.random.randint(len(population))
        if population[ind2][0] < population[ind1][0]:
            ind1 = ind2
        prob = random.random()
        if (prob > 0.5 ):
            selectedIndexes.append(ind1)
            selectedPopulation.append(population[ind1])
    return selectedPopulation

def rank_selection(population,Nprime):
    def rank_list(population):
        sorted_list = sorted(population,reverse=True)
        ranks = [sorted_list.index(x) + 1 for x in population]
        return ranks
    ranks = rank_list(population)
    sum_ranks = sum(ranks)
    indexes = np.random.choice(len(population),size=Nprime,replace=False, p=[x / sum_ranks for x in ranks]).tolist()
    return [population[i] for i in indexes]

def elt_selection(population,Nprime):  # elitism
    return sorted(population,reverse=True)[0:Nprime]

def crossover(p1,p2):
    # we get the array and eliminate the last 0
    pp1, pp2 = p1[1].copy()[:-1], p2[1].copy()[:-1]
    Possible = False
    while not Possible:
        c1, c2 = pp1.copy(), pp2.copy()
        pt1 = random.randint(1, len(pp1)-1)
        pt2 = random.randint(1, len(pp2)-1)
        while pt1 == pt2:
            pt2 = random.randint(0, len(pp2)-1)
        pt1, pt2 = (pt1, pt2) if pt1 < pt2 else (pt2, pt1)
        # we do the cross over
        c1[pt1:pt2+1] = pp2[pt1:pt2+1]
        c2[pt1:pt2+1] = pp1[pt1:pt2+1]
        # we look for missing values
        c1_missing_values = [i for i in range(len(A)) if i not in c1]
        c2_missing_values = [i for i in range(len(A)) if i not in c2]
        # we look for redandent values and replace them
        for j in range(pt1):
            if c1[j] in pp2[pt1:pt2+1]:
                c1[j] = c1_missing_values.pop()
            if c2[j] in pp1[pt1:pt2+1]:
                c2[j] = c2_missing_values.pop()
        for j in range(pt2+1,len(A)):
            if c1[j] in pp2[pt1:pt2+1]:
                c1[j] = c1_missing_values.pop()
            if c2[j] in pp1[pt1:pt2+1]:
                c2[j] = c2_missing_values.pop()
        if cost(c1 + [0]) != 0 and cost(c2 + [0]) != 0:
            Possible = True
    c1, c2 = c1 + [0], c2 + [0]
    return [cost(c1),c1], [cost(c2),c2]

def mutation(population,Pm):
    mutatedPopulation = []
    for indiv in population:
        if random.random() < Pm:
            validPath = False
            while not validPath:
                indivc = copy.deepcopy(indiv)
                point1 = random.randint(1, len(indiv[1]) - 2)
                point2 = random.randint(1, len(indiv[1]) - 2)
                indivc[1][point1], indivc[1][point2] = indivc[1][point2] ,indivc[1][point1]
                pathCost = cost(indivc[1])
                if( pathCost > 0 ):
                    indivc[0] = pathCost
                    validPath = True
                    mutatedPopulation.append(indivc)
        else:
            mutatedPopulation.append(indiv)
    return mutatedPopulation

def remplacement(newPopulation,N):
    return sorted(newPopulation)[:N]

def GA(pop,Nprime,Pc,Pm,MAX_ITER):
    population = pop.copy()
    for _ in range(MAX_ITER):
        population = tnm_selection(population,Nprime)
        pair = []
        for indiv in population:
            prob = random.random()
            if (prob < Pc ):
                pair.append(indiv)
                if(len(pair) == 2):
                    child1, child2 = crossover(pair[0],pair[1])
                    population.append(child1)
                    population.append(child2)
                    pair = []
        population = mutation(population,Pm)
        population = remplacement(population,len(pop))
    print(population)
    return population

# GA(200,140,0.5,0.1,300)