# sudoku-solver
This project _will_ provide some different ways to solve a sudoku. Nothing is designed to be fast or efficient. The goal is just to make it work.

# Use
Import the `Field` class and the `solve` function from any file other than `base.py` and input the field formatted as shown in the following example. The method will return a copy of the input field with the solved values.

```
from sudoku_solver import Field, solve

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

 Note that, in case the algorithm isn't able to completely or even partially solve the sudoku, it will still return the field, but only with the partial solution. You can use `field.is_solved()` to check if the solution is complete.