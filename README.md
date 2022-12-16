## OPTIMIZATION_TimeScheduling

### Problems
N classes: 1, 2, ..., N need to be assigned.
- Each class i has t(i): number of periods needed, g(i): teacher, s(i): number of students
M rooms: 1, 2, ..., M 
- Each room i has c(i) number of seats
There are 5 scholar days a week, from Monday to Friday, each day is divided into 12 periods
(Morning: 6 periods/ Afternoon: 6 periods)

Create a timetable for those classes satisfying the following constraints:
1. Classes with the same teacher can not be on the same period
2. Number of students need to be smaller than number of seats

### Solution
**I will divide 5 days - 60 periods into 10 blocks, each block contains 6 periods.**
- All of classes can not be assigned in 2 separated blocks
- I define a boolean variable Assign(i, m, k, b) for whether "assign class i in room b in period b of block k" or not
- Teacher can not be at the different rooms or classes simultaneously, so sum of Assign() for that him/her <= 1 at each period.
  Also, the total period taught by him cannot exceed maxperiod (6)
- A class i cannot change room during its section, then the total periods taken by it can only be 0 (not assigned) or t(i) (is assigned)
- A class i has to be assigned once in a whole week then total periods taken by it for whole week = t(i)
- One room cannot contain 2 class at the same period, then when a class i in assigned to a room j, the next t(i) periods of room j need to be blocked.

**With supports of Google OR-Tools, we can solve this problem !!!** 




![image](https://user-images.githubusercontent.com/87572445/208050998-5bb2fd17-6153-4970-a6e8-9d32532a0e98.png)

