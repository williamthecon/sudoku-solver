from base import Field

def _loop(field: Field, possibles: dict[tuple[int, int], list[int]]) -> Field | None:
    """Recursively solves the given field using the bruteforce method.

    Args:
        field (Field): The field to solve.
        possibles (dict[tuple[int, int], list[int]]): The possible values for all empty cells.

    Returns:
        Field | None: The solved field or None if the field is not solvable.
    """
    if not field.is_valid():
        return None

    empty = field.get_empty_cell()
    if empty is None:
        return field

    for number in possibles[empty.tuple()]:
        field.set(empty, number) # type: ignore [int != FieldValue]
        result = _loop(field, possibles)
        if result is not None:
            return result

        field.set(empty, 0)

    return None

def solve(field: Field) -> Field:
    """Solves the given field using the bruteforce method.

    Args:
        field (Field): The field to solve.

    Returns:
        Field: The solved field.

    Raises:
        ValueError: If the field is not valid.
    """
    if not field.is_valid():
        raise ValueError("Field is not valid")

    nfield = field.copy()

    if nfield.is_solved():
        return nfield

    possibles = {coord.tuple(): list(field.get_possible_values(coord)) for coord, value in nfield.enumerate() if value == 0}

    result = _loop(nfield, possibles) # type: ignore
    if result is None:
        return nfield

    return result
