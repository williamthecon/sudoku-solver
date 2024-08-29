from base import Field, Coord, FieldValue

def get_best_move(field: Field) -> tuple[Coord | None, FieldValue]:

    return None, 0

def solve(field: Field) -> Field:
    emptys = field.get_empty_cells()
    for _ in range(len(emptys)):
        best_coord, best_value = get_best_move(field)
        if best_coord is None:
            return field

        field.set(best_coord, best_value)

    return field