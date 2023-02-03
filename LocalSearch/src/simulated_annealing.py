import math
from src.evaluation_function import evaluation
from src.get_neighbours import neighbourings, get_best_neighbour
       
def simulated_annealing(init_timetable, num_of_iterations, initial_temp, rooms, teachers):
    
    current_solution = init_timetable
    current_score = evaluation(current_solution, rooms, teachers)
    
    prob_bound = 1e-50

    for i in range(num_of_iterations):

        current_temp = initial_temp / float(i+1)
        neighbours = neighbourings(current_solution, rooms)
        best_neighbour, best_neighbour_score = get_best_neighbour(neighbours, rooms, teachers)

        if best_neighbour_score < current_score: 
            current_solution, current_score = best_neighbour, best_neighbour_score
        else: 
            diff = best_neighbour_score - current_score
            prob = math.exp(-(diff/current_temp))

            if (prob >= prob_bound): current_solution, current_score = best_neighbour, best_neighbour_score

    return current_solution, current_score

cnt = 1
def iterated_simulated_annealing(inits, num_of_iterations, classes, rooms, teachers):
    global cnt
    scores = []
    current_best_score = math.inf
    current_best_solution = inits[0]
    for init in inits:
        print(f"Try Init SA #{cnt}")
        solution, score = simulated_annealing(init, num_of_iterations, 10, rooms, teachers)
        scores.append(score)
        current_best_score = min(current_best_score, score)
        if current_best_score == score: current_best_solution = solution
        cnt += 1
    print()
    return current_best_solution, current_best_score, scores


