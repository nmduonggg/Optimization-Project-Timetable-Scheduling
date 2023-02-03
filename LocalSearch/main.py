from src.generate_initialize import random_initialize
from src.hill_climbing import iterated_hill_climbing
from src.simulated_annealing import iterated_simulated_annealing
from read_data import read_data


def write_output(line: str, outputFile):
    with open(outputFile, "a") as f:
        f.write(line)
        f.write("\n")

if __name__ == "__main__":

    input_file = r'LocalSearch\special_data.txt'
    output_file = r'LocalSearch\result.txt'
    
    classes, rooms, teachers = read_data(inputFile= input_file)
    num_of_inits = 15
    inits = random_initialize(classes, rooms, num_of_inits)
    num_of_iterations = 200

    hill = 1

    if hill: 
        with open(output_file, "w") as f:
            f.write("HILL CLIMBING \n")
        solution, score, candidate_scores = iterated_hill_climbing(inits, num_of_iterations, 
        classes, rooms, teachers)
    
    else: 
        with open(output_file, "w") as f:
            f.write("SIMULATED ANNEALING \n")
        solution, score, candidate_scores = iterated_simulated_annealing(inits, num_of_iterations, 
        classes, rooms, teachers)
    
    print(*candidate_scores)
    print("Best Score: " + str(score))

    solution.sort(key = lambda x: x[7])
    for n in solution:
        write_output("{} - {}:{} - {} - {} - {} - {} - {}".format(
            n[7], n[6], n[6]+n[1]-1, n[0], n[2], n[3], n[4], n[5] 
        ), output_file)

    print("DONE")