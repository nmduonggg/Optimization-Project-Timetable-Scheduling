

# Read input
classes = {}   #(t, g, s)
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

X = {} #assigned = integer(period)
# -----------------------Initialization-------------------------#
for i in classes:
    for m in rooms:
        X[(i, m)] = []

def find_block(b: int):
    if (b%6 == 0): return b//6
    else: return (b//6) + 1

# --------------------------Constraints------------------------#

#Enough seats
def enough_seat(i: int, m: int):
    global classes, rooms
    return classes[i][2] <= rooms[m]

#Class not in 2 separated blocks
def not_separated_blocks(i: int):
    global X, classes, rooms
    t,g,s = classes[i]

    # How many periods in a whole week
    periods = []
    tmp_periods = [X[x] for x in X.keys() if (x[0] == i) & (X[x] > 0)]
    for p in tmp_periods:
        periods += p
    cnt = len(periods)
    minPeriod = min(periods)
    maxPeriod = max(periods)
    return (find_block(minPeriod) == find_block(maxPeriod)) & (cnt == t)
    
# Teacher cannot be at the different rooms or classes simultaneously
def duplicated_teacher(teacher: str):
    global X, classes, rooms
    
    def compare(l1: list, l2: list):
        s1 = set(l1)
        s2 = set(l2)
        return ((s1 & s2) == None) # Kiểm tra set difference ra null hay set rỗng



    def different_rooms(teacher: str):
        for i in classes:
            if classes[i][1] == teacher:
                for m in rooms:
                    if X[(i, m)] != 0:


    

#Backtracking
def Try(period_b: int):
    pass