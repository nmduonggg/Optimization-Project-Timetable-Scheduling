from copy import deepcopy
from src.evaluation_function import evaluation



def neighbourings(current_timetable, rooms):
    
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
        if timetable[i][6] + timetable[i][1] < 6: timetable[i][6] += 1
        if mixed_timetable[i][6] + timetable[i][1] < 6: mixed_timetable[i][6] += 1
        new_timetables.append(timetable)
        new_timetables.append(mixed_timetable)
    for i in range(1, len(current_timetable)):
        timetable = list(deepcopy(current_timetable))
        if timetable[i][6] > 1: timetable[i][6] -= 1
        if mixed_timetable[i][6] > 1: mixed_timetable[i][6] -= 1
        new_timetables.append(timetable)
        new_timetables.append(mixed_timetable)
    
    return new_timetables

def get_best_neighbour(neighbours, rooms, teachers):
    best_neighbour = neighbours[0]
    current_best = evaluation(best_neighbour, rooms, teachers)

    for n in neighbours:
        score = evaluation(n, rooms, teachers)
        current_best = min(current_best, score)
        if current_best == score: best_neighbour = n

    return best_neighbour, current_best
       