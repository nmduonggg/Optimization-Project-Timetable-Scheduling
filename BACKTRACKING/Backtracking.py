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
        classes[i] = (int(t), g, int(s))
        if g not in teachers: teachers.append(g)
    for j in range(N+1, N+M+1):
        rooms[j - N] = int(lines[j].rstrip())


# Decision variable
X = {}
N = len(classes)
M = len(rooms)
MaxBlock = 10
MaxPeriods = 6

for i in range(1, N + 1):
    for m in range(1, M + 1):
        for k in range(1, MaxBlock + 1):
            for b in range(1, MaxPeriods + 1):
                X[(i, m, k, b)] = 0

# Constraint: The chosen room has enough seats for students
def enough_seats(i, m, k, b):
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    t, g, s = classes[i]
    return s <= rooms[m]

# Constraint: Class cannot be assigned in 2 separated blocks
def separated_blocks():
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    check = True
    for k in range(1, MaxBlock + 1):
        for i in classes:
            t, g, s = classes[i]
            PeriodInBlock = 0
            
            for m in rooms:
                for b in range(1, MaxPeriods + 1):
                    PeriodInBlock += X[(i, m, k, b)]
            check = (PeriodInBlock == t) | (PeriodInBlock == 0)
            if check == False: break
        if check == False: break

    return check

    
# Constraint: Each teacher can only teach one class in each period
def teacher_class():
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    check = True
    for teacher in teachers:
        for k in range(1, MaxBlock + 1):
            for b in range(1, MaxPeriods + 1):
                duplicate_tc = 0
                for m in rooms:
                    for i in classes:
                        t, g, s = classes[i]
                        if g == teacher:
                            duplicate_tc += X[(i, m, k, b)]
                check =  (duplicate_tc <= 1)
                if check == False: break
            if check == False: break
        if check == False: break

    return check
               
# Constraint: Total periods taught by 1 teacher <= 6

def total_periods_teacher():
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    check = True
    for k in range(1, MaxBlock + 1):
        for teacher in teachers:
            PeriodInBlock = 0
            for m in rooms:
                for i in classes:
                    t, g, s = classes[i]
                    if g == teacher:
                        for b in range(1, MaxPeriods + 1):
                            PeriodInBlock += X[(i, m, k, b)]
            check = (PeriodInBlock <= MaxPeriods)
            if check == False: break
        if check == False: break
    return check                

# Constraint: Class cannot change room during its section
def class_not_change():
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    check = True
    for i in classes:
        t, g, s = classes[i]
        for m in rooms:
            RoomPeriodInWeek = 0
            for k in range(1, MaxPeriods + 1):
                for b in range(1, MaxPeriods + 1):
                    RoomPeriodInWeek += X[(i, m, k, b)]
            check = (RoomPeriodInWeek == t) | (RoomPeriodInWeek == 0)
            if check == False: break
        if check == False: break

    return check
            
# Constraint: Each class has to be assigned in whole week
def assigned_once():
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    check = True
    for i in classes:
        t, g, s = classes[i]
        CPeriodInWeek = 0
        for k in range(1, MaxBlock + 1):
            for b in range(1, MaxPeriods + 1):
                for m in rooms:
                    CPeriodInWeek += X[(i, m, k, b)]
        check = (CPeriodInWeek == t)
        if check == False: break

    return check

# Constraint: At every period, there must be less than 1 class assigned to the given room
def class_room():
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    check = True
    for k in range(1, MaxBlock + 1):
        for m in rooms:
            for b in range(1, MaxPeriods + 1):
                class_dup = 0
                for i in classes:
                    class_dup += X[(i, m, k, b)]
                check = (class_dup <= 1)
                if check == False: break
            if check == False: break
        if check == False: break
    return check

# Constraint: When assign class i in the given room, the next t-1 periods blocked
def next_blocked():
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    check = True
    for k in range(1, MaxPeriods + 1):
        if check:
            for b in range(1, MaxPeriods + 1):
                Blocked = 0
                if check:
                    for m in rooms:
                        if check:
                            for i in classes:
                                if check:
                                    t, g, s = classes[i]
                                    if X[(i, m, k, b)] == 1:
                                        for b_ in range(b, b + t-1):
                                            Blocked += X[(i, m, k, b_)]
                                        check = (Blocked == t)
        
    return check

def condition():
    return separated_blocks() & teacher_class() & total_periods_teacher() & class_not_change() & assigned_once() & next_blocked()

cnt = 1
outputFile = "output_backtrack.txt"
with open(outputFile, "w") as f:
    f.write(" ")

def WriteSolution(outputFile):
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers
    global cnt
    with open(outputFile, "a") as f:
        f.write("Solution " + str(cnt) + "\n")
        cnt += 1
        for assign in X.keys():
            i, m, k, b = assign
            f.write("Block " + str(k) + "\n")
            t, g, s = classes[i]
            if X[assign] == 1:
                f.write("**", end = " ")
                f.write(f"Class{i} by {g} takes {t} in room {m} assigned to period {b} ")
        f.write(" ")

try_cnt = 1
visited = []


# Backtrack
# start at block 1, period 1

def Find(b_run: int):
    global classes, rooms, MaxBlock, MaxPeriods, X, teachers, try_cnt

    for i in classes:
        t,g,s = classes[i]
        
        for m in rooms:

            if b_run > MaxBlock*MaxPeriods: 
                    if X not in visited:
                        visited.append(X)
                        print(f"Try {try_cnt}")

            else:
                if (s <= rooms[m]):

                    if b_run % 6 == 0: k = b_run // 6
                    else: k = (b_run // 6) + 1
                    b = b_run - 6*(k-1)

                    X[(i, m, k, b)] = 1
                
                    for b_ in range(b, b+t):
                        X[(i, m, k, b_)] = 1
                   
                    Find(b_run + 1)
                    X[(i, m, k, b)] = 0
                    
                    for b_ in range(b, b+t):
                        X[(i, m, k, b_)] = 0
          
        

            # if condition(): WriteSolution()


Find(1)
                        
print("Done")