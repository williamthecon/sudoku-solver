# sudoku-solver
A sudoku solver with minimal code

# Use
Just import the solve function and input the field as a list with nine lists containing nine strings containing either numbers or spaces. To print out a field you can use the `fprint` function

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
