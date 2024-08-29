from base import Field, Coord, FieldValue

# Strategies:
# 1. Only one possible value here
# 2. This value only possible here (row/column/block)
# (3. Two cells (in a row/column/block) with only two possible values)
# Two cells align with at least one possible value other appearances in block can be eliminated
# " and they are in the same block, other appearances in block can be eliminated

class Item:
    exists: bool

    def __init__(self, value):
        self.value = value
        self.exists = True

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

class Collection:
    def __init__(self, items: list[Item]):
        self.items = items

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return repr(self.items)

    def __iter__(self):
        for item in self.items:
            if item.exists:
                yield item

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

def solve(field: Field) -> Field:
    """Solves the given field using the logical method.

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

    def remove_possibility(item):
        item.exists = False
        coord = item.value[0]
        block = coord.to_block_coord()
        value = nfield.get(coord)

        print()
        print(f"{coord}: {value}")
        print(nfield)

        possibles.remove(item)
        possibles_rows[coord.y].remove(item)
        possibles_columns[coord.x].remove(item)
        possibles_blocks[block.n].remove(item)

        for item2 in possibles_rows[coord.y]:
            if value in item2.value[1]:
                # print(f"Removing {value} from row {item2}")
                item2.value[1].remove(value)

        for item2 in possibles_columns[coord.x]:
            if value in item2.value[1]:
                # print(f"Removing {value} from column {item2}")
                item2.value[1].remove(value)

        for item2 in possibles_blocks[block.n]:
            if value in item2.value[1]:
                # print(f"Removing {value} from block {item2}")
                item2.value[1].remove(value)

    possibles = Collection([])
    possibles_rows = [Collection([]) for _ in range(9)]
    possibles_columns = [Collection([]) for _ in range(9)]
    possibles_blocks = [Collection([]) for _ in range(9)]

    for coord in nfield.get_empty_cells():
        item = Item((coord, list(nfield.get_possible_values(coord))))
        possibles.add(item) # type: ignore
        possibles_rows[coord.y].add(item)
        possibles_columns[coord.x].add(item)
        possibles_blocks[coord.to_block_coord().n].add(item)

    while not nfield.is_solved():
        print(nfield.is_valid())
        success = False

        if len(possibles) == 1:
            coord, values = possibles[0].value
            nfield.set(coord, values[0]) # type: ignore [int != FieldValue]
            break

        # Only one possible value here
        for item in possibles:
            coord, values = item.value
            if len(values) == 1:
                nfield.set(coord, values[0]) # type: ignore [int != FieldValue]
                remove_possibility(item)
                success = True
                break

        if success:
            continue

        # This value only possible here
        for n, item in enumerate(possibles):
            coord, values = item.value
            coord_block = coord.to_block_coord()
            for value in values:
                double = False
                for item2 in possibles[n + 1:]:
                    coord2, values2 = item2.value
                    if value in values2:
                        if coord.x == coord2.x or coord.y == coord2.y or coord_block.n == coord2.to_block_coord().n:
                            double = True
                            break

                if not double:
                    nfield.set(coord, value) # type: ignore [int != FieldValue]
                    remove_possibility(item)
                    success = True
                    break

            if success:
                break

        if success:
            continue

        break

    # for _ in range(len(emptys)):
    #     next_coord, next_value = get_next_move(nfield, emptys)
    #     if next_coord is None:
    #         return nfield

    #     nfield.set(next_coord, next_value)

    return nfield
