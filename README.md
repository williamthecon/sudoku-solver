# sudoku-solver
Solves any sudoku automatically, but hasn't any implemented error handling.

# Use
Import the solve function and input the field formatted as shown in the following example. To print out a field you can use the `fprint` function.

```
from sudoku_solver import solve, fprint

field = [
    [' ', '9', '7', '2', ' ', '6', ' ', '3', '1'],
    [' ', ' ', ' ', '1', ' ', '5', '4', ' ', '6'],
    [' ', ' ', ' ', ' ', '9', ' ', ' ', '5', ' '],
    ['7', ' ', ' ', ' ', ' ', ' ', '9', ' ', '3'],
    ['9', ' ', '3', ' ', '8', ' ', ' ', '6', ' '],
    [' ', '5', '2', ' ', '6', '3', ' ', '7', ' '],
    [' ', '6', '9', ' ', ' ', '1', '5', '2', ' '],
    ['1', ' ', '5', '6', ' ', ' ', '3', ' ', ' '],
    ['3', ' ', '4', '8', ' ', ' ', '6', '1', '7']
]
fprint(field)
solution = solve(field)
fprint(solution)
```
