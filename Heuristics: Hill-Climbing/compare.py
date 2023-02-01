from hill_climbing import *
from simulated_annealing import *

import math
import random
from copy import deepcopy

# Read input
classes = {}
rooms = {}
teachers = []
inputFile = 'data.txt'
with open(inputFile, "r") as f:
    lines = f.readlines()
    N, M = [int(x) for x in lines[0].split()]
    for i in range(1, N+1):
        t, g, s = lines[i].split()
        classes[i] = [int(t), g, int(s)]
        if g not in teachers: teachers.append(g)
    for j in range(N+1, N+M+1):
        rooms[j - N] = int(lines[j].rstrip())

def test_random_initialize(classes, rooms, num_of_inits):
    
    all_timetables = []
    for _ in range(num_of_inits):
        temp_timetable = []
        for i in classes:
            assign = []
            t,g,s = classes[i]
            start = random.randint(1,6)
            block = random.randint(1,10)
            for m in rooms:
                seat = rooms[m]
                
                if s <= seat:                                                 # Starting,Block   
                    assign = assign + [i] + classes[i] + [m] + [rooms[m]] + [start,block]
                    temp_timetable.append(assign)
                    break

        all_timetables.append(temp_timetable)
    return all_timetables


num_of_inits = 80
inits = test_random_initialize(classes, rooms, num_of_inits)
def iterated_SA(inits):
    global rooms, classes, cnt
    scores = []
    current_best_score = math.inf
    current_best_solution = inits[0]
    for init in inits:
        print(f"Try {cnt}")
        solution, score = simulated_annealing(init, 100, 10)
        scores.append(score)
        current_best_score = min(current_best_score, score)
        if current_best_score == score: current_best_solution = solution
        cnt += 1
    print()
    return current_best_solution, current_best_score, scores

def iterated_HC(inits):
    global rooms, classes, cnt
    scores = []
    current_best_score = math.inf
    current_best_solution = inits[0]
    for init in inits:
        print(f"Try {cnt}")
        solution, score = hill_climbing(init)
        scores.append(score)
        current_best_score = min(current_best_score, score)
        if current_best_score == score: current_best_solution = solution
        cnt += 1
    print()
    return current_best_solution, current_best_score, scores


def test(inits):
    HC_scores = iterated_HC(inits)[2]
    SA_scores = iterated_SA(inits)[2]
    max_HC = min(HC_scores)
    max_SA = min(SA_scores)

    print("Hill Climbing: ", HC_scores)
    print("Hill Climbing Best: ", max_HC)
    print("Simulated Annealing: ", SA_scores)
    print("Simulated Annealing Best: ", max_SA)

test(inits)