import numpy as np


class Digit:
    def __init__(self, value: int):
        self.value = value
        self.is_default = (value != 0)

    def __str__(self) -> str:
        return f"{self.value}"


class Grid:
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.first_non_default_index = self.get_index_of_first_non_default()

    def __str__(self):
        string = ''
        for i in range(0, 3):
            string = string + "+-------+-------+-------+\n"
            for j in range(0, 3):
                for k in range(0, 3):
                    string = string + '|'
                    for m in range(0, 3):
                        string = string + ' ' + str(self.grid[27 * i + 9 * j + 3 * k + m].value)
                    string = string + ' '
                string = string + '|\n'
        string = string + "+-------+-------+-------+"
        return string

    def get_row_from_index(self, index: int) -> list:
        """
        Gives the row of the grid at an index
        :param index: index in the row
        :return: the row as a list
        """
        return [self.grid[(index // 9) * 9 + i].value for i in range(0, 9)]

    def get_col_from_index(self, index: int) -> list:
        """
        Gives the column of the grid at an index
        :param index: index in the column
        :return: the column as a list
        """
        return [self.grid[(index % 9) + i * 9].value for i in range(0, 9)]

    def get_box_from_index(self, index: int) -> list:
        """
        Gives the box of the grid in which the index is, a sudoku grid being separated into 9 boxes
        :param index: index in the box
        :return: the box as a list
        """
        box = [[self.grid[(index // 27) * 27 + ((index % 9) // 3) * 3 + j * 9 + k].value for k in range(0, 3)] for j in
               range(0, 3)]
        box = box[0] + box[1] + box[2]
        return box

    def get_digit(self, index: int) -> Digit:
        """
        Gives the digit corresponding at a given index
        :param index: index of the digit
        :return: the digit
        """
        return self.grid[index]

    def get_index_of_first_non_default(self) -> int:
        i = 0
        for i in range(0, len(self.grid)):
            if not self.grid[i].is_default:
                break
        return i


class Sudoku:
    def __init__(self, file_path: str):
        self.grid = Grid(self.open_sudoku(file_path))

    def __str__(self):
        return f"{self.grid}"

    def open_sudoku(self, path: str) -> np.ndarray:
        """
        Opens an inline sudoku (00209310..01) from a file
        :param path: path of the file
        :return: a 2d numpy array representing the sudoku grid
        """
        opened_sudoku = np.array([])
        with open(path) as f:
            for n in f.readline()[:-2]:  # [:-2] to remove the ',' and '\n'
                opened_sudoku = np.append(opened_sudoku, Digit(int(n)))
        return opened_sudoku

    def accept(self) -> bool:
        """
        Checks if the completed grid is correct
        :return: True if the grid is correct, False otherwise
        """
        if 0 in [cell.value for cell in self.grid.grid]:
            return False
        # checking the rows and columns
        for i in range(0, 9):
            row = self.grid.get_row_from_index(i * 9)
            col = self.grid.get_col_from_index(i)
            if len(row) > len(set(row)) or len(col) > len(set(col)):
                return False

        # checking the boxes
        for i in range(0, 3):
            for j in range(0, 3):
                box = self.grid.get_box_from_index(i * 27 + j * 3)
                if len(box) > len(set(box)):
                    return False
        return True

    def reject(self, number: int, index: int) -> bool:
        """
        Check if the number placement is correct, i.e. it is not already in its row, column or box.
        :param grid: 2d array representing the sudoku grid
        :param number: number to insert
        :param index: index of the number in the grid
        :return: True if the number placement in not correct, False otherwise
        """
        if number == 0 or number > 9:
            return True
        # checking if the number is already in the row / column
        if self.grid.get_row_from_index(index).count(number) + self.grid.get_col_from_index(index).count(number) > 2:
            return True
        # checking if the number is in the box
        if self.grid.get_box_from_index(index).count(number) > 1:
            return True
        return False

    def solve(self) -> bool:
        """
        Solves the sudoku using backtracking
        ----
        Algorithm:
        while the grid is not accepted:
         |  current (index in the grid) is 0
         |  while current index is less than 9 * 9
         |   |  if the digit is a default one:
         |   |   |  current is current + 1
         |   |  else:
         |   |   |  if the current state is rejected:
         |   |   |   |  if the current digit is less than 9:
         |   |   |   |   |  add one to the current digit
         |   |   |   |  else
         |   |   |   |   |  set the current digit to zero
         |   |   |   |   |  current goes back to the last non-default digit
         |   |   |   |   |  add one to the current digit
         |   |   |   |  end if
         |   |   |  else:
         |   |   |   |  current is current + 1
         |   |   |  end if
         |   |  end if
         |  end while
        end while
        ----
        :return: True if the sudoku has been solved, False otherwise
        """
        while not self.accept():
            current = 0
            while current < 9 * 9:
                current_digit = self.grid.get_digit(current)
                if current_digit.is_default:
                    current = current + 1
                else:
                    if self.reject(current_digit.value, current):
                        if current_digit.value < 9:
                            current_digit.value = current_digit.value + 1
                        else:
                            current_digit.value = 0
                            current = current - 1
                            while self.grid.get_digit(current).is_default:
                                if current < self.grid.first_non_default_index:
                                    return False
                                current = current - 1
                            self.grid.get_digit(current).value = self.grid.get_digit(current).value + 1
                    else:
                        current = current + 1
        return True


if __name__ == "__main__":
    sudoku = Sudoku("data.csv")

    print('Unsolved :')
    print(sudoku.grid)

    sudoku.solve()

    print('Solved :')
    print(sudoku.grid)
