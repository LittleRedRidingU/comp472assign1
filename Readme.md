Instruction to use program:
1. Enter row and column number to create the grid you desired.
2. Enter a list of numbers for place arrangement:
    # 1 for quarantine, 2 for vaccine, 3 for playground, 0 for empty
    # Here is an example for 3*4 grid: 1 2 3 0 2 0 1 0 3 1 2 2
3. Enter the role you want to pick: "c", "v", or "p"
4. Enter the Index of start place staring from 1 to row*column, such as "1", "7"
5. A* method is starting now:
   # our heuristic function will consider any point around destination as end point
6. Return the output.

Libraries:
    matplotlib.pyplot
    math