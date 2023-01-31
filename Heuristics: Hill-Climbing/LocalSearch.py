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

# INPUT:
## classes: {"Class ID": [NumPeriods, Teacher, NumStudents]}
## rooms: {"Room ID": NumSeats
# OUTPUT:
## [[ClassID, NumPeriods, Teacher, NumStudents, RoomID, NumSeats, StartingPeriod, Block]]
## ==> There is not any conflict in room duplication, numseats, only teacher and duplicated period

def random_initialize(classes, rooms, num_of_inits):
    
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

        

def evaluation(timetable):
    global rooms, teachers
    TheScore = 0

    # HARD CONSTRAINTS
    for i in range(len(timetable)):
        for j in range(i+1, len(timetable)):
            # for simplicity, assign temp1 first and reassign temp2 following the constraints after temp1
            temp1 = timetable[i]
            temp2 = timetable[j]

            # check whether 2 classes are assigned at 1 period of a block
            
            ## same block
            if temp1[7] == temp2[7]:

                period_diff = temp2[6] - (temp1[6]+temp1[1]-1) # (start period 2 - end period 1) 
                if period_diff <= 1: 
                    if period_diff == 0: TheScore += 8
                    else: TheScore += abs(period_diff) + 1

                ## 1 room cannot be assigned for 2 classed in 1 period
                if temp1[4] == temp2[4] :
                    period_diff = temp2[6] - (temp1[6]+temp1[1]-1) # (start period 2 - end period 1) 
                    if period_diff <= 1: 
                        if period_diff == 0: TheScore += 8
                        else: TheScore += abs(period_diff) + 1


                ## 1 teacher 1 class 1 period
                if temp1[2] == temp2[2]:
                    period_diff = temp2[6] - (temp1[6]+temp1[1]-1) # (start period 2 - end period 1) 
                    if period_diff <= 1: 
                        if period_diff == 0: TheScore += 8
                        else: TheScore += abs(period_diff) + 1

            ## class is only at 1 block
            end_period = temp2[6] + temp2[1] - 1
            if end_period > 6: TheScore += 1
            

    # Total periods of a room in one block
    over_periods = 0
    for m in rooms:
        total_periods = sum([temp[1] for temp in timetable if temp[4] == m])
        if total_periods > 6: over_periods += 1
    TheScore += over_periods

    # Total periods of teacher in one block
    over_teachers = 0
    for t in teachers:
        total_periods = sum([temp[1] for temp in timetable if temp[2] == t])
        if total_periods > 6: over_teachers += 1
    TheScore += over_teachers
    # SOFT CONSTRAINTS
    ## usally teachers want to work in beginning of weeks and go out at the rest of week
    ## it could be obtained by make the classes assigned as close as possible

    return TheScore

def neighbourings(current_timetable):
    global rooms
    new_timetables = []
    mixed_timetable = list(deepcopy(current_timetable))
    # change room
    for i in range(len(current_timetable)):
        timetable = list(deepcopy(current_timetable))
        assign = current_timetable[i]
        current_room_id = assign[4]
        current_num_students = assign[3]

        for m in rooms:
            seat = rooms[m]
            if seat >= current_num_students and current_room_id != m:
                timetable[i][4] = m
                mixed_timetable[i][4] = m
                new_timetables.append(timetable)
                new_timetables.append(mixed_timetable)
                break
        

    # change block
    for i in range(1, len(current_timetable)):
        timetable = list(deepcopy(current_timetable))
        if timetable[i][7] < 10: timetable[i][7] += 1
        if mixed_timetable[i][7] < 10: mixed_timetable[i][7] += 1
        new_timetables.append(timetable)
        new_timetables.append(mixed_timetable)
    for i in range(1, len(current_timetable)):
        timetable = list(deepcopy(current_timetable))
        if timetable[i][7] > 1: timetable[i][7] -= 1
        if mixed_timetable[i][7] > 1: mixed_timetable[i][7] -= 1
        new_timetables.append(timetable)
        new_timetables.append(mixed_timetable)
    
    # change starting period
    for i in range(1, len(current_timetable)):
        timetable = list(deepcopy(current_timetable))
        if timetable[i][6] < 6: timetable[i][6] += 1
        if mixed_timetable[i][6] < 6: mixed_timetable[i][6] += 1
        new_timetables.append(timetable)
        new_timetables.append(mixed_timetable)
    for i in range(1, len(current_timetable)):
        timetable = list(deepcopy(current_timetable))
        if timetable[i][6] > 1: timetable[i][6] -= 1
        if mixed_timetable[i][6] > 1: mixed_timetable[i][6] -= 1
        new_timetables.append(timetable)
        new_timetables.append(mixed_timetable)
    
    return new_timetables

def get_best_neighbour(neighbours):
    best_neighbour = neighbours[0]
    current_best = evaluation(best_neighbour)

    for n in neighbours:
        score = evaluation(n)
        current_best = min(current_best, score)
        if current_best == score: best_neighbour = n

    return best_neighbour, current_best
       

def local_search(init_timetable):
    
    current_solution = init_timetable
    current_score = evaluation(current_solution)
    neighbours = neighbourings(current_solution)
    best_neighbour, best_neighbour_score = get_best_neighbour(neighbours)

    while best_neighbour_score < current_score: 
        current_solution = best_neighbour
        current_score = best_neighbour_score
        new_neighbours = neighbourings(current_solution)
        best_neighbour, best_neighbour_score = get_best_neighbour(new_neighbours)

        print("Current Score: " + str(current_score), end = "\n")

    return current_solution, current_score

cnt = 1
def iterated_local_search(num_of_inits):
    global rooms, classes, cnt
    inits = random_initialize(classes, rooms, num_of_inits)
    scores = []
    current_best_score = math.inf
    current_best_solution = inits[0]
    for init in inits:
        print(f"Try {cnt}")
        solution, score = local_search(init)
        scores.append(score)
        current_best_score = min(current_best_score, score)
        if current_best_score == score: current_best_solution = solution
        cnt += 1
    print()
    return current_best_solution, current_best_score, scores


if __name__ == "__main__":

    solution, score, candidate_scores = iterated_local_search(200)
    print(*candidate_scores)
    print("Best Score: " + str(score))
    
    for n in solution:
        print(n)
