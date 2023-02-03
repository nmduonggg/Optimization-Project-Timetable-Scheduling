
def read_data(inputFile):
    classes = {}
    rooms = {}
    teachers = []
    with open(inputFile, "r") as f:
        lines = f.readlines()
        N, M = [int(x) for x in lines[0].split()]
        for i in range(1, N+1):
            t, g, s = lines[i].split()
            classes[i] = [int(t), g, int(s)]
            if g not in teachers: teachers.append(g)
        for j in range(N+1, N+M+1):
            rooms[j - N] = int(lines[j].rstrip())

    return classes, rooms, teachers