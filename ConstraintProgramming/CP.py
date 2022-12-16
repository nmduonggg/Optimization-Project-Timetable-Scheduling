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


# Modelling
from ortools.sat.python import cp_model
model = cp_model.CpModel()

AssignOptions = {}
MaxBlock = 10
MaxStartPeriod = 6

for i in classes:
    t, g, s = classes[i]
    for m in rooms:
        for k in range(1, MaxBlock + 1):
            for b in range(1, MaxStartPeriod + 1):
                AssignOptions[(i, m, k, b)] = model.NewBoolVar(f"Assign class {i} in room {m} at period {b} of block {k}")

# Constraint: A class is assinged once on a week and all have been assigned
# for i in classes:
#     assigned = 0
#     for k in range(1, MaxBlock + 1):
#         for b in range(1, MaxStartPeriod + 1):
#             for m in rooms:
#                 assigned += AssignOptions[(i, m, k, b)]
#     model.Add(assigned == 1)
            
# Constraint: There are enough seats for students
for k in range(1, MaxBlock + 1):
    for b in range(1, MaxStartPeriod + 1):
        for i in classes:
            t, g, s = classes[i]
            for m in rooms:
                model.Add(s <= rooms[m]).OnlyEnforceIf(AssignOptions[(i, m, k, b)])

# Constraint: Sum of periods by teacher of each block <= max period
for teacher in teachers:
    for k in range(1, MaxBlock + 1):
        TeachPeriod = 0
        for m in rooms:
            for i in classes:
                t, g, s = classes[i]
                if g == teacher:
                    for b in range(1, MaxStartPeriod + 1):
                        TeachPeriod += AssignOptions[(i, m, k, b)]
        model.Add(TeachPeriod <= MaxStartPeriod)

# Constraint: Each teacher at each period teaches one class only
for teacher in teachers:
    for k in range(1, MaxBlock + 1):
        for b in range(1, MaxStartPeriod + 1):
            not_duplicate = 0
            for m in rooms:
                for i in classes:
                    t, g, s = classes[i]
                    if g == teacher:
                        not_duplicate += AssignOptions[(i, m, k, b)]

            model.Add(not_duplicate <= 1)
                

# Constraint: One room contains one class at each block
for k in range(1, MaxBlock + 1):
    for b in range(1, MaxStartPeriod + 1):
        for m in rooms:
            model.Add(sum(AssignOptions[(i, m, k, b)] for i in classes) <= 1)

# Constraint: One class can not change room during section
for i in classes:
    t, g, s = classes[i]
    for m in rooms:
        period_in_room = 0
        x = model.NewBoolVar("")
        for k in range(1, MaxBlock + 1):
            for b in range(1, MaxStartPeriod + 1):
                period_in_room += AssignOptions[(i, m, k, b)]

        model.Add(period_in_room == t).OnlyEnforceIf(x)
        model.Add(period_in_room == 0).OnlyEnforceIf(x.Not())

# Constraint: One class assigned once a week and has to be assigned
for i in classes:
    PeriodInWeek = 0
    t, g, s = classes[i]
    for k in range(1, MaxBlock + 1):
        for b in range(1, MaxStartPeriod + 1):
            for m in rooms:
                PeriodInWeek += AssignOptions[(i, m, k, b)]

    model.Add(PeriodInWeek == t)

# Constraint: Class can not be assigned in 2 separated blocks
for i in classes:
    t, g, s = classes[i]
    for k in range(1, MaxBlock + 1):
        x = model.NewBoolVar("")
        class_period_block = 0
        for m in rooms:
            for b in range(1, MaxStartPeriod + 1):
                class_period_block += AssignOptions[(i, m, k, b)]
        
        model.Add(class_period_block == t).OnlyEnforceIf(x)
        model.Add(class_period_block == 0).OnlyEnforceIf(x.Not())

# Constraint: When assign class to a start period, t next periods of that room are blocked
for k in range(1, MaxBlock + 1):
    for m in rooms:
        for i in classes:
            t, g, s = classes[i]
            for b in range(1, MaxStartPeriod + 1 - t):
                model.Add(sum(AssignOptions[(i, m, k, b_)] for b_ in range(b, b+t)) == AssignOptions[(i, m, k, b)]*t).OnlyEnforceIf(AssignOptions[(i, m, k, b)])

# Solution Printer Class
class SolutionPrinterClass(cp_model.CpSolverSolutionCallback):
    def __init__(self, AssignOptions, classes, rooms, blocks, maxperiods, sols):
        val = cp_model.CpSolverSolutionCallback.__init__(self)
        self._AssignOptions = AssignOptions
        self._classes = len(classes)
        self._rooms = len(rooms)
        self._blocks = blocks
        self._maxperiods = maxperiods
        self._solutions = set(sols)
        self._solution_count = 0
    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print("solution " + str(self._solution_count))
            for k in range(1, self._blocks+1):
                print("Block " + str(k))
                for i in range(1, self._classes+1):
                    t, g, s = classes[i]
                    is_teaching = False
               
                    for m in range(1, self._rooms+1):
                        for b in range(1, self._maxperiods + 1):
                            
                            # print(f"Class {i} room {m} block {k} period {b}: {self.Value(self._AssignOptions[(i, m, k, b)])}")
                    
                            if self.Value(self._AssignOptions[(i, m, k, b)]):
                                is_teaching = True
                                print("** Class " +str(i) + " takes " + str(t) + " by " + g + " in room " + str(m) + " at period " + str(b))
                              
                    if not is_teaching:
                        print('-- Class {} does not assigned in this block'.format(i))
            print()
        self._solution_count += 1
    def solution_count(self):
        return self._solution_count


# Solver
solver = cp_model.CpSolver()
# Solve it and check if solution was feasible
solutionrange = range(1) # we want to display 1 feasible results (the first one in the feasible set)
solution_printer = SolutionPrinterClass(AssignOptions, classes, rooms,
                                        MaxBlock, MaxStartPeriod, solutionrange)
solver.SearchForAllSolutions(model, solution_printer)