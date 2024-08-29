# sudoku-solver
This project _will_ provide some different ways to solve a sudoku. Nothing is designed to be fast or efficient. The goal is just to make it work.

# Use
Import the `Field` class from `base`, the `solve` function from any other file and input the field formatted as shown in the following example.

```
from base import Field
from sudoku_solver import solve

field = Field([
    [0, 9, 7, 2, 0, 6, 0, 3, 1],
    [0, 0, 0, 1, 0, 5, 4, 0, 6],
    [0, 0, 0, 0, 9, 0, 0, 5, 0],
    [7, 0, 0, 0, 0, 0, 9, 0, 3],
    [9, 0, 3, 0, 8, 0, 0, 6, 0],
    [0, 5, 2, 0, 6, 3, 0, 7, 0],
    [0, 6, 9, 0, 0, 1, 5, 2, 0],
    [1, 0, 5, 6, 0, 0, 3, 0, 0],
    [3, 0, 4, 8, 0, 0, 6, 1, 7]
])
print(field)
solution = solve(field)
print(solution)
```
