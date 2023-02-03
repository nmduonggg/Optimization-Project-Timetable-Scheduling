def evaluation(timetable, rooms, teachers):
    TheScore = 0

    # HARD CONSTRAINTS
    for i in range(len(timetable)):
        for j in range(len(timetable)):

            if i != j:
                # for simplicity, assign temp1 first and reassign temp2 following the constraints after temp1
                temp1 = timetable[i]
                temp2 = timetable[j]

                # check whether 2 classes are assigned at 1 period of a block
                
                ## same block
                if temp1[7] == temp2[7]:

                    # end_temp1 = temp1[6] + temp1[1] - 1
                    # if temp2[6] <= end_temp1 <= temp2[6] + temp2[1] - 1: TheScore += 8
                    # else: TheScore -= 5

                    ## 1 room cannot be assigned for 2 classed in 1 period
                    if temp1[4] == temp2[4] :
                        end_temp1 = temp1[6] + temp1[1] - 1
                        if temp2[6] <= end_temp1 <= temp2[6] + temp2[1] - 1: TheScore += 15
                        else: TheScore -= 5
                    else: TheScore -= 7


                    ## 1 teacher 1 class 1 period
                    if temp1[2] == temp2[2]:
                        end_temp1 = temp1[6] + temp1[1] - 1
                        if temp2[6] <= end_temp1 <= temp2[6] + temp2[1] - 1: TheScore += 15
                        else: TheScore -= 5
                    else: TheScore -= 7
                else: TheScore -= 10

                ## class is only at 1 block
                end_period = temp2[6] + temp2[1] - 1
                if end_period > 6: TheScore += 1

                

        # Total periods of a room in one block
    #     over_periods = 0
    #     for m in rooms:
    #         total_periods = sum([temp[1] for temp in timetable if temp[4] == m])
    #         if total_periods > 6: over_periods += 5
    #     TheScore += over_periods

    # # Total periods of teacher in one block
    # over_teachers = 0
    # for t in teachers:
    #     total_periods = sum([temp[1] for temp in timetable if temp[2] == t])
    #     if total_periods > 6: over_teachers += 5
    # TheScore += over_teachers
    # SOFT CONSTRAINTS
    ## usally teachers want to work in beginning of weeks and go out at the rest of week
    ## it could be obtained by make the classes assigned as close as possible

    return TheScore