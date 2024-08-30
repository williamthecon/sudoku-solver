from typing import Iterator, Literal

FieldType = Literal[0, 1, 2]
FieldValue = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class Field:
    """
    Representing a Sudoku field.
    """
    def __init__(self, rows: list[list[int]] | None = None, columns: list[list[int]] | None = None):
        """Initializes a new field with the given rows or columns.

        Args:
            rows (list[list[int]], optional): The rows of the field. Defaults to an empty field.
            columns (list[list[int]], optional): The columns of the field. Defaults to an empty field.

        Raises:
            AssertionError: If the field is not 9x9 or if the field contains invalid values.
        """
        if columns is not None:
            rows = list(map(list, zip(*columns)))
        elif rows is not None:
            columns = list(map(list, zip(*rows)))
        else:
            rows = [[0] * 9 for _ in range(9)]
            columns = [[0] * 9 for _ in range(9)]

        assert len(rows) == 9 and all(len(row) == 9 for row in rows), "Field must be 9x9"
        assert all(0 <= v <= 9 for row in rows for v in row), "Field must only contain numbers between 0 and 9, or 0 for empty cells"

        self.rows: list[list[int]] = rows
        self.columns: list[list[int]] = columns
        self.blocks: list[list[int]] = [[] for _ in range(9)]

        # Precompute the blocks
        for y, row in enumerate(self.rows):
            for x, value in enumerate(row):
                self.blocks[x // 3 + y // 3 * 3].append(value)

    def __str__(self) -> str:
        """Returns a string representation of the field.

        Returns:
            str: A string representation of the field.
        """
        rows = []
        for y, row in enumerate(self.rows):
            if y % 3 == 0 and y != 0:
                rows.append("------+-------+------")

            rs = ""
            for x, value in enumerate(row):
                if x % 3 == 0 and x != 0:
                    rs += "| "
                rs += str(value) + " "
            rows.append(rs)
        return "\n".join(rows)

    def __repr__(self) -> str:
        """Returns a string representation of the field.

        Returns:
            str: A string representation of the field.
        """
        return str(self)

    def _get_by_type(self, type: FieldType) -> list[list[int]]:
        """Returns the rows, columns or blocks of the field based on the given type (0, 1 or 2).

        Args:
            type (FieldType): The type of list to return (0: rows; 1: columns; 2: blocks).

        Returns:
            list[list[int]]: The rows, columns or blocks of the field.
        """
        return [self.rows, self.columns, self.blocks][type]

    def get(self, coord: "Coord | BlockCoord") -> int:
        """Returns the value at the given coordinates.

        Args:
            coord (Coord | BlockCoord): The coordinates of the value to get.

        Returns:
            int: The value at the given coordinates.

        Raises:
            ValueError: If the coordinates are not valid.
        """
        if isinstance(coord, Coord):
            return self.rows[coord.y][coord.x]
        elif isinstance(coord, BlockCoord):
            return self.blocks[coord.n][coord.i]

        raise ValueError("Invalid coordinates. Only Coords and BlockCoords are allowed")

    def get_rows(self, y: int | slice) -> list[list[int]] | list[int]:
        """Returns one or more rows of the field.

        Args:
            y (int | slice): The row(s) to return.

        Returns:
            list[list[int]] | list[int]: The rows of the field.
        """
        return self.rows[y]

    def get_columns(self, x: int | slice) -> list[list[int]] | list[int]:
        """Returns one or more columns of the field.

        Args:
            x (int | slice): The column(s) to return.

        Returns:
            list[list[int]] | list[int]: The columns of the field.
        """
        return self.columns[x]

    def get_blocks(self, x: int | slice) -> list[list[int]] | list[int]:
        """Returns one or more blocks of the field.

        Args:
            x (int | slice): The block(s) to return.

        Returns:
            list[list[int]] | list[int]: The blocks of the field.
        """
        return self.blocks[x]

    def __getitem__(self, key) -> list[list[int]] | list[int] | int:
        """Returns one or more row(s), column(s) or block(s) of the field, or the value at the given coordinates.

        Args:
            key (int | slice | Coord | BlockCoord): The row(s), column(s) or block(s) to return, or the coordinates of the value to get.

        Returns:
            list[list[int]] | list[int] | int: The row(s), column(s) or block(s) of the field, or the value at the given coordinates.

        Raises:
            TypeError: If the key is not of a valid type.
        """
        if isinstance(key, (int, slice)):
            return self.get_rows(key)
        elif isinstance(key, (Coord, BlockCoord)):
            return self.get(key)

        raise TypeError("Invalid index. Only integers, slices, Coords and BlockCoords are allowed.")

    def set(self, coord: "Coord | BlockCoord", value: FieldValue):
        """Sets the value at the given coordinates.

        Args:
            coord (Coord | BlockCoord): The coordinates of the value to set.

        Raises:
            ValueError: If the value is not between 0 and 9.
        """
        if not 0 <= value <= 9:
            raise ValueError("Field must only contain numbers between 0 and 9, or 0 for empty cells")

        if isinstance(coord, Coord):
            x, y = coord.x, coord.y
            n, i = BlockCoord.from_coord(coord).tuple()
        else: # BlockCoord
            x, y = coord.to_coord().tuple()
            n, i = coord.n, coord.i

        self.rows[y][x] = value
        self.columns[x][y] = value
        self.blocks[n][i] = value

    def __setitem__(self, key, value: FieldValue):
        """Sets the value at the given coordinates.

        Args:
            key (Coord | BlockCoord): The coordinates of the value to set.

        Raises:
            ValueError: If the value is not between 0 and 9.
        """
        self.set(key, value)

    def __iter__(self) -> Iterator[list[int]]:
        """Returns an iterator over the rows of the field.

        Returns:
            Iterator[list[int]]: An iterator over the rows of the field.
        """
        return iter(self.rows)

    def __len__(self) -> int:
        """Returns the number of rows in the field.

        Returns:
            int: The number of rows in the field.
        """
        return len(self.rows)

    def enumerate(self, type: FieldType = 0) -> Iterator[tuple["Coord | BlockCoord", int]]:
        """Returns an iterator over the cells of the field.

        Args:
            type (FieldType, optional): The order to return the cells (0: by rows; 1: by columns; 2: by blocks). Defaults to 0 (by rows).

        Returns:
            Iterator[tuple[Coord | BlockCoord, int]]: An iterator over the cells of the field.

        Raises:
            ValueError: If the type is invalid.
        """
        if type == 0:
            for y, row in enumerate(self.rows):
                for x, value in enumerate(row):
                    yield Coord(x, y), value
        elif type == 1:
            for x, column in enumerate(self.columns):
                for y, value in enumerate(column):
                    yield Coord(x, y), value
        elif type == 2:
            for n, block in enumerate(self.blocks):
                for i, value in enumerate(block):
                    yield BlockCoord(n, i), value
        else:
            raise ValueError("Invalid type. Only 0 (rows), 1 (columns) and 2 (blocks) are allowed")

    def enumerate_rows(self) -> Iterator[tuple[int, list[int]]]:
        """Returns an iterator over the rows of the field as tuples of the row number and the row.

        Returns:
            Iterator[tuple[int, list[int]]]: An iterator over the rows of the field as tuples of the row number and the row.
        """
        return enumerate(self.rows)

    def enumerate_columns(self) -> Iterator[tuple[int, list[int]]]:
        """Returns an iterator over the columns of the field as tuples of the column number and the column.

        Returns:
            Iterator[tuple[int, list[int]]]: An iterator over the columns of the field as tuples of the column number and the column.
        """
        return enumerate(self.columns)

    def enumerate_blocks(self) -> Iterator[tuple[int, list[int]]]:
        """Returns an iterator over the blocks of the field as tuples of the block number and the block.

        Returns:
            Iterator[tuple[int, list[int]]]: An iterator over the blocks of the field as tuples of the block number and the block.
        """
        return enumerate(self.blocks)

    def is_valid(self) -> bool:
        """Returns True if the field is valid, False otherwise.

        Returns:
            bool: True if the field is valid, False otherwise.
        """
        for row in self.rows:
            for value in set(row):
                if value != 0 and row.count(value) > 1:
                    return False

        for column in self.columns:
            for value in set(column):
                if value != 0 and column.count(value) > 1:
                    return False

        for block in self.blocks:
            for value in set(block):
                if value != 0 and block.count(value) > 1:
                    return False

        return True

    def is_valid_for(self, coord: "Coord | BlockCoord", value: FieldValue) -> bool:
        """Returns True if the field is valid for the given value at the given coordinates, False otherwise.

        Args:
            coord (Coord | BlockCoord): The coordinates of the value to check.
            value (FieldValue): The value to check.

        Returns:
            bool: True if the field is valid for the given value at the given coordinates, False otherwise.
        """
        if not self.is_valid():
            return False

        self.set(coord, value)
        valid = self.is_valid()
        self.set(coord, 0)

        return valid

    def is_solved(self) -> bool:
        """Returns True if the field is solved, False otherwise.

        Returns:
            bool: True if the field is solved, False otherwise.
        """
        return self.is_valid() and all(value != 0 for _, value in self.enumerate())

    def get_empty_cell(self) -> "Coord | None":
        """Returns the coordinates of the first empty cell in the field, or None if there are no empty cells.

        Returns:
            Coord | None: The coordinates of the first empty cell in the field, or None if there are no empty cells.
        """
        for coord, value in self.enumerate():
            if value == 0:
                return coord # type: ignore [will be Coord]

        return None

    def get_empty_cells(self) -> list["Coord"]:
        """Returns a list of the coordinates of the empty cells in the field.

        Returns:
            list[Coord]: A list of the coordinates of the empty cells in the field.
        """
        return [coord for coord, value in self.enumerate() if value == 0] # type: ignore [will be Coord]

    def get_possible_values(self, coord: "Coord | BlockCoord") -> Iterator[int]:
        """Returns a list of the possible values for the given coordinate.

        Args:
            coord (Coord | BlockCoord): The coordinate.

        Returns:
            Iterator[int]: A list of the possible values for the given coordinate.
        """
        for value in range(1, 10):
            if self.is_valid_for(coord, value): # type: ignore
                yield value

    def copy(self) -> "Field":
        """Returns a copy of the field.

        Returns:
            Field: A copy of the field.
        """
        return Field([row.copy() for row in self.rows])

    def copy_with(self, coord: "Coord | BlockCoord", value: FieldValue) -> "Field":
        """Returns a copy of the field with the given value at the given coordinates.

        Args:
            coord (Coord | BlockCoord): The coordinates of the value to set.
            value (FieldValue): The value to set.

        Returns:
            Field: A copy of the field with the given value at the given coordinates.
        """
        field = self.copy()
        field.set(coord, value)
        return field

    def format(self, marked: list["Coord"] = []) -> str:
        """Returns a string representation of the field. The given coordinates are marked with two asterisks.

        Args:
            marked (list[Coord], optional): The coordinates to mark. Defaults to [].

        Returns:
            str: A string representation of the field.
        """
        rows = []
        for y, row in enumerate(self.rows):
            if y % 3 == 0 and y != 0:
                rows.append("------+-------+------")

            rs = ""
            for x, value in enumerate(row):
                if x % 3 == 0 and x != 0:
                    rs += "| "
                if Coord(x, y) in marked:
                    rs = rs[:-1] + "*" + str(value) + "*"
                else:
                    rs += str(value) + " "
            rows.append(rs)
        return "\n".join(rows)

class Coord:
    """
    Represents a coordinate in the field.
    """
    def __init__(self, x: int, y: int):
        """Initializes a new coordinate.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Raises:
            AssertionError: If the coordinates are not between [0 and 8].
        """
        assert 0 <= x < 9 and 0 <= y < 9, "Coordinates must be between 0 and 8"

        self.x = x
        self.y = y

    @classmethod
    def from_block_coord(cls, coord: "BlockCoord") -> "Coord":
        """Creates a new coordinate from a block coordinate.

        Args:
            coord (BlockCoord): The block coordinate.

        Returns:
            Coord: The new coordinate.
        """
        return coord.to_coord()

    def to_block_coord(self) -> "BlockCoord":
        """Converts the coordinate to a block coordinate.

        Returns:
            BlockCoord: The block coordinate.
        """
        return BlockCoord.from_coord(self)

    def __str__(self) -> str:
        """Returns a string representation of the coordinate.

        Returns:
            str: The string representation of the coordinate.
        """
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Returns a string representation of the coordinate.

        Returns:
            str: The string representation of the coordinate.
        """
        return str(self)

    def __eq__(self, other) -> bool:
        """Checks if the coordinates are equal.

        Args:
            other (Coord | BlockCoord): The other coordinate.

        Returns:
            bool: True if the coordinates are equal, False otherwise.
        """
        if isinstance(other, Coord):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, BlockCoord):
            oc = other.to_coord()
            return self.x == oc.x and self.y == oc.y

        raise TypeError("Invalid comparison. Only Coords and BlockCoords are allowed.")

    def __ne__(self, other) -> bool:
        """Checks if the coordinates are not equal.

        Args:
            other (Coord | BlockCoord): The other coordinate.

        Returns:
            bool: True if the coordinates are not equal, False otherwise.
        """
        return not self == other

    def __getitem__(self, key) -> int:
        """Returns the value at the given index.

        Args:
            key (int | str): The index.

        Returns:
            int: The value at the given index.

        Raises:
            ValueError: If the index is invalid.
            TypeError: If the index is not an integer or a string.
        """
        if isinstance(key, int):
            if key in [0, 1]:
                return [self.x, self.y][key]

            raise ValueError("Invalid index. Only 0 (x) and 1 (y) are allowed")
        elif isinstance(key, str):
            if key in ["x", "y"]:
                return {"x": self.x, "y": self.y}[key]

            raise ValueError("Invalid index. Only 'x' and 'y' are allowed")

        raise TypeError("Invalid index. Only integers and strings are allowed.")

    def copy(self) -> "Coord":
        """Returns a copy of the coordinate.

        Returns:
            Coord: A copy of the coordinate.
        """
        return Coord(self.x, self.y)

    def tuple(self) -> tuple[int, int]:
        """Returns the coordinate as a tuple.

        Returns:
            tuple[int, int]: The coordinate as a tuple.
        """
        return self.x, self.y

class BlockCoord:
    """
    Represents a block coordinate in the field.
    """
    def __init__(self, n: int, i: int):
        """Initializes a new block coordinate.

        Args:
            n (int): The block number.
            i (int): The block index.

        Raises:
            AssertionError: If the block number or index are not between [0 and 8].
        """
        assert 0 <= n < 9 and 0 <= i < 9, "Block number and index must be between 0 and 8"

        self.n = n
        self.i = i

    @classmethod
    def from_coord(cls, coord: Coord) -> "BlockCoord":
        """Creates a new block coordinate from a coordinate.

        Args:
            coord (Coord): The coordinate.

        Returns:
            BlockCoord: The new block coordinate.
        """

        x, y = coord.x, coord.y
        n, i = x // 3 + y // 3 * 3, x % 3 + y % 3 * 3

        return cls(n, i)

    def to_coord(self) -> Coord:
        """Converts the block coordinate to a coordinate.

        Returns:
            Coord: The converted coordinate.
        """
        i, n = self.i, self.n
        x, y = n % 3 * 3 + i % 3, n // 3 * 3 + i // 3

        return Coord(x, y)

    def __str__(self) -> str:
        """Returns a string representation of the block coordinate.

        Returns:
            str: The string representation of the block coordinate.
        """
        return f"({self.n}, {self.i})"

    def __repr__(self) -> str:
        """Returns a string representation of the block coordinate.

        Returns:
            str: The string representation of the block coordinate.
        """
        return str(self)

    def __getitem__(self, key) -> int:
        """Returns the value at the given index.

        Args:
            key (int | str): The index.

        Returns:
            int: The value at the given index.

        Raises:
            ValueError: If the index is invalid.
            TypeError: If the index is not an integer or a string.
        """
        if isinstance(key, int):
            if key in [0, 1]:
                return [self.n, self.i][key]

            raise ValueError("Invalid index. Only 0 (n) and 1 (i) are allowed")
        elif isinstance(key, str):
            if key in ["n", "i"]:
                return {"n": self.n, "i": self.i}[key]

            raise ValueError("Invalid index. Only 'n' and 'i' are allowed")

        raise TypeError("Invalid index. Only integers are allowed")

    def __eq__(self, other) -> bool:
        """Checks if the coordinates are equal.

        Args:
            other (Coord | BlockCoord): The other coordinate.

        Returns:
            bool: True if the coordinates are equal, False otherwise.
        """
        if isinstance(other, BlockCoord):
            return self.n == other.n and self.i == other.i
        elif isinstance(other, Coord):
            oc = other.to_block_coord()
            return self.n == oc.n and self.i == oc.i

        raise TypeError("Invalid comparison. Only Coords and BlockCoords are allowed")

    def copy(self) -> "BlockCoord":
        """Returns a copy of the block coordinate.

        Returns:
            BlockCoord: A copy of the block coordinate.
        """
        return BlockCoord(self.n, self.i)

    def tuple(self) -> tuple[int, int]:
        """Returns the block coordinate as a tuple.

        Returns:
            tuple[int, int]: The block coordinate as a tuple.
        """
        return self.n, self.i
