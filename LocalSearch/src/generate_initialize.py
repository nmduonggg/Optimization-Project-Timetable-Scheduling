import math
import random
from copy import deepcopy

# Read input

# def read_data(inputFile):
#     classes = {}
#     rooms = {}
#     teachers = []
#     with open(inputFile, "r") as f:
#         lines = f.readlines()
#         N, M = [int(x) for x in lines[0].split()]
#         for i in range(1, N+1):
#             t, g, s = lines[i].split()
#             classes[i] = [int(t), g, int(s)]
#             if g not in teachers: teachers.append(g)
#         for j in range(N+1, N+M+1):
#             rooms[j - N] = int(lines[j].rstrip())

#     return classes, rooms, teachers

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
            max_start = 7 - t
            start = random.randint(1,max_start)
            block = random.randint(1,10)
            for m in rooms:
                seat = rooms[m]
                
                if s <= seat:                                                 # Starting,Block   
                    assign = assign + [i] + classes[i] + [m] + [rooms[m]] + [start,block]
                    temp_timetable.append(assign)
                    break

        all_timetables.append(temp_timetable)
    return all_timetables
