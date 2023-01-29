classes = {}
rooms = {}
teachers = []
inputFile = 'backtracking\data.txt'
with open(inputFile, "r") as f:
    lines = f.readlines()
    N, M = [int(x) for x in lines[0].split()]
    for i in range(1, N+1):
        t, g, s = lines[i].split()
        classes[i] = (int(t), g, int(s))
        if g not in teachers: teachers.append(g)
    for j in range(N+1, N+M+1):
        rooms[j - N] = int(lines[j].rstrip())

max_k = 10  # number of blocks in a week

timetable = {x: [] for x in range(1, 11)}
available_room = {}
for r in rooms.keys():
    available_room[r] = [1]*60

available_teacher = {}
for c_id in classes.keys():
    t, g, s = classes[c_id]
    available_teacher[g] = [1]*60

available_class = {}
for c in classes.keys():
    available_class[c] = 1

cnt = 1
try_cnt = 1
def PrintSolution():
    global try_cnt
    print(f"Try {try_cnt}")
    try_cnt += 1

outputFile = 'backtracking\output_backtracking.txt'
with open(outputFile, 'w') as f:
        f.write(" ")

def write(outputFile):
    global cnt, timetable
    with open(outputFile, 'a') as f:
        f.write(f"# {cnt} \n")
        for block, c in timetable.items():
            f.write(f"{block}: {c} \n")
        f.write("\n")
    cnt += 1

left_class = len(available_class.keys())
assigned = []

def Try(b):
    global left_class, cnt, assigned, timetable, outputFile, teachers
    
    if b % 6 == 0: block_k = b//6
    else: block_k = b//6 + 1
    start_b = b - 6*(block_k-1)

    if (b > 60):
        PrintSolution()
        if (timetable not in assigned): 
            assigned.append(timetable)
            write(outputFile)
    else:
        tmp_class = 0
        tmp_teacher = 0
        tmp_room = 0
        for c_id in classes.keys():
            change = False
            t, g, s = classes[c_id]
            start = start_b - 1 + (block_k - 1)*6
            end = start_b - 1 + t + (block_k - 1)*6

            if (available_class[c_id] == 1) & (available_teacher[g][start: end] == [1]*t) & (start_b + t - 1 <= 6):
                tmp_class = c_id
                tmp_teacher = g
            
                for r_id in rooms.keys():
                    if (s <= rooms[r_id]) & (available_room[r_id][start: end] == [1]*t):
                        tmp_room = r_id
                        timetable[block_k] = timetable[block_k] + [[c_id, classes[c_id], r_id, rooms[r_id], start_b]]
                        available_class[c_id] = 0
                        available_teacher[g][start: end] = [0]*t
                        available_room[r_id][start: end] = [0]*t
                        left_class -= 1
                        change = True
                        
                    else:
                        timetable[block_k].append([])

                    Try(b+1)
                    timetable[block_k].pop()

                    if change:
                        available_class[tmp_class] = 1
                        available_teacher[tmp_teacher][start: end] = [1]*t
                        available_room[tmp_room][start: end] = [1]*t
                        left_class += 1

Try(1)
print("DONE !!!!")
