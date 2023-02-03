import math
from src.evaluation_function import evaluation
from src.get_neighbours import neighbourings, get_best_neighbour

def hill_climbing(init_timetable, rooms, teachers):
    
    current_solution = init_timetable
    current_score = evaluation(current_solution, rooms, teachers)
    neighbours = neighbourings(current_solution, rooms)
    best_neighbour, best_neighbour_score = get_best_neighbour(neighbours, rooms, teachers)

    while best_neighbour_score < current_score: 
        current_solution = best_neighbour
        current_score = best_neighbour_score
        new_neighbours = neighbourings(current_solution, rooms)
        best_neighbour, best_neighbour_score = get_best_neighbour(new_neighbours, rooms, teachers)

        print("Current Score: " + str(current_score), end = "\n")

    return current_solution, current_score

cnt = 1
def iterated_hill_climbing(inits, num_of_iterations, classes, rooms, teachers):
    global cnt
    scores = []
    current_best_score = math.inf
    current_best_solution = inits[0]
    for init in inits:
        print(f"Try Init HC #{cnt}")
        solution, score = hill_climbing(init, rooms, teachers)
        scores.append(score)
        current_best_score = min(current_best_score, score)
        if current_best_score == score: current_best_solution = solution
        cnt += 1
    print()
    return current_best_solution, current_best_score, scores

