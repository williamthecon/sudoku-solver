from base import Field

def _loop(field: Field) -> Field | None:
    """Recursively solves the given field using the bruteforce method.

    Args:
        field (Field): The field to solve.

    Returns:
        Field | None: The solved field or None if the field is not solvable.
    """
    if not field.is_valid():
        return None

    empty = field.get_empty_cell()
    if empty is None:
        return field

    for number in field.get_possible_values(empty):
        field.set(empty, number) # type: ignore [int != FieldValue]
        result = _loop(field)
        if result is not None:
            return result

    return None

def solve(field: Field) -> Field:
    """Solves the given field using the bruteforce method.

    Args:
        field (Field): The field to solve.

    Returns:
        Field: The solved field.

    Raises:
        ValueError: If the field is not valid or not solvable.
    """

    if not field.is_valid():
        raise ValueError("Field is not valid")

    if field.is_solved():
        return field

    result = _loop(field)
    if result is None:
        raise ValueError("Field is not solvable")
    return result