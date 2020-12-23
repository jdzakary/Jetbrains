import math
import copy


class Matrix:
    rows = None
    columns = None
    contents_string = []
    contents_numeric = []

    def __init__(self, manual, contents, rows, columns):
        if manual is True:
            self.rows = int(rows)
            self.columns = int(columns)
            self.contents_numeric = []
            y = 0
            while y < self.rows:
                this_row = input().split()
                this_row = [float(x) for x in this_row]
                if len(this_row) != self.columns:
                    print("ERROR")
                    self.contents_numeric = []
                    break
                else:
                    self.contents_numeric.append(this_row)
                y += 1
        else:
            self.contents_numeric = contents
            self.rows = rows
            self.columns = columns

    def convert_contents(self):
        this_row = []
        self.contents_string = []
        for row in self.contents_numeric:
            for number in row:
                new = str(number)
                this_row.append(new)
            self.contents_string.append(this_row)
            this_row = []

    def structured_form(self):
        self.convert_contents()
        for row in self.contents_string:
            print(' '.join(row))

    def addition(self, target):
        if self.rows == target.rows and self. columns == target.columns:
            new_contents = []
            this_row = []
            x = 0
            y = 0
            for row in self.contents_numeric:
                for number in row:
                    new = number + target.contents_numeric[y][x]
                    this_row.append(new)
                    x += 1
                new_contents.append(this_row)
                this_row = []
                x = 0
                y += 1
            return new_contents
        else:
            return False

    def multiplication_integer(self, multiple):
        new_contents = []
        this_row = []
        x = 0
        y = 0
        for row in self.contents_numeric:
            for number in row:
                new = number * float(multiple)
                this_row.append(new)
                x += 1
            new_contents.append(this_row)
            this_row = []
            x = 0
            y += 1
        return new_contents

    def multiplication_matrix(self, target):
        if self.columns == target.rows:
            new_contents = []
            this_row = []
            running_total = 0
            x = 0  # Macroscopic column counter
            y = 0  # Macroscopic row counter
            z = 0  # Internal counter
            while y < self.rows:
                while x < target.columns:
                    while z < self.columns:
                        running_total += (self.contents_numeric[y][z] * target.contents_numeric[z][x])
                        z += 1
                    this_row.append(running_total)
                    z = 0
                    running_total = 0
                    x += 1
                new_contents.append(this_row)
                this_row = []
                x = 0
                y += 1
            return new_contents
        else:
            return False

    def transpose_horizontal(self):
        new_contents = self.contents_numeric[::-1]
        return new_contents

    def transpose_vertical(self):
        new_contents = []
        for row in self.contents_numeric:
            new_row = row[::-1]
            new_contents.append(new_row)
        return new_contents

    def transpose_main(self):
        new_contents = []
        this_row = []
        x = 0
        y = 0
        while x < self.columns:
            while y < self.rows:
                this_row.append(self.contents_numeric[y][x])
                y += 1
            new_contents.append(this_row)
            this_row = []
            y = 0
            x += 1
        return new_contents

    def transpose_side(self):
        new_contents = []
        this_row = []
        x = self.columns - 1
        y = self.rows - 1
        while x >= 0:
            while y >= 0:
                this_row.append(self.contents_numeric[y][x])
                y -= 1
            new_contents.append(this_row)
            this_row = []
            y = self.rows - 1
            x -= 1
        return new_contents


def determinant(coefficient, contents):
    if len(contents) == 2:
        return coefficient * (contents[0][0]*contents[1][1] - contents[1][0]*contents[0][1])
    else:
        answer = 0
        for y in range(0, len(contents)):
            new_coefficient = contents[y][0] * math.pow(-1, y+2) * coefficient
            new_contents = copy.deepcopy(contents)
            del new_contents[y]
            for x in range(0, len(new_contents)):
                del new_contents[x][0]
            answer += determinant(new_coefficient, new_contents)
        return answer


def element_cofactor(coefficient, contents, first=False, row=None, column=None):
    if len(contents) == 2:
        return coefficient * (contents[0][0]*contents[1][1] - contents[1][0]*contents[0][1])
    elif first is True:
        answer = 0
        column2 = int(row) - 1
        row2 = int(column) - 1
        new_coefficient = math.pow(-1, row2 + column2 + 2)
        new_contents = copy.deepcopy(contents)
        del new_contents[row2]
        for x in range(0, len(new_contents)):
            del new_contents[x][column2]
        answer += element_cofactor(new_coefficient, new_contents)
        return answer
    else:
        answer = 0
        for y in range(0, len(contents)):
            new_coefficient = contents[y][0] * math.pow(-1, y+2) * coefficient
            new_contents = copy.deepcopy(contents)
            del new_contents[y]
            for x in range(0, len(new_contents)):
                del new_contents[x][0]
            answer += element_cofactor(new_coefficient, new_contents)
        return answer


def cofactor_matrix(contents):
    new_contents = []
    for y in range(0, len(contents)):
        this_row = []
        for x in range(0, len(contents[y])):
            this_row.append(element_cofactor(1, contents, True, y+1, x+1))
        new_contents.append(this_row)
    return new_contents


def action_1():
    rows, columns = input('Enter size of first matrix: ').split()
    print('Enter first matrix:')
    matrix_1 = Matrix(True, None, rows, columns)
    rows2, columns2 = input('Enter size of second matrix: ').split()
    print('Enter second matrix:')
    matrix_2 = Matrix(True, None, rows2, columns2)
    if rows == rows2 and columns == columns2:
        new_contents = matrix_1.addition(matrix_2)
        matrix_3 = Matrix(False, new_contents, matrix_1.rows, matrix_2.columns)
        print('The result is:')
        matrix_3.structured_form()
    else:
        print('The operation cannot be performed.')


def action_2():
    rows, columns = input('Enter size of matrix: ').split()
    print('Enter matrix:')
    matrix_1 = Matrix(True, None, rows, columns)
    constant = input('Enter constant: ')
    new_contents = matrix_1.multiplication_integer(constant)
    matrix_3 = Matrix(False, new_contents, matrix_1.rows, matrix_1.columns)
    print('The result is:')
    matrix_3.structured_form()


def action_3():
    rows, columns = input('Enter size of first matrix: ').split()
    print('Enter first matrix:')
    matrix_1 = Matrix(True, None, rows, columns)
    rows2, columns2 = input('Enter size of second matrix: ').split()
    print('Enter second matrix:')
    matrix_2 = Matrix(True, None, rows2, columns2)
    if columns == rows2:
        new_contents = matrix_1.multiplication_matrix(matrix_2)
        matrix_3 = Matrix(False, new_contents, columns2, rows)
        print('The result is:')
        matrix_3.structured_form()
    else:
        print('The operation cannot be preformed.')


def action_4():
    print()
    print('1. Main diagonal')
    print('2. Side diagonal')
    print('3. Vertical line')
    print('4. Horizontal line')
    action = input('Your choice: ')
    rows, columns = input('Enter matrix size: ').split()
    print('Enter matrix:')
    matrix_1 = Matrix(True, None, rows, columns)
    if action == '1':
        matrix_2 = Matrix(False, matrix_1.transpose_main(), rows, columns)
        print('The result is: ')
        matrix_2.structured_form()
    elif action == '2':
        matrix_2 = Matrix(False, matrix_1.transpose_side(), rows, columns)
        print('The result is: ')
        matrix_2.structured_form()
    elif action == '3':
        matrix_2 = Matrix(False, matrix_1.transpose_vertical(), rows, columns)
        print('The result is: ')
        matrix_2.structured_form()
    elif action == '4':
        matrix_2 = Matrix(False, matrix_1.transpose_horizontal(), rows, columns)
        print('The result is: ')
        matrix_2.structured_form()
    else:
        print('That is not a valid option!')
        print()
        action_4()


def action_5():
    rows, columns = input('Enter matrix size: ').split()
    if rows == columns:
        if rows == '1':
            print('Enter matrix:')
            number = input()
            print('The result is:')
            print(number)
        else:
            print('Enter matrix:')
            matrix_1 = Matrix(True, None, rows, columns)
            print('The result is:')
            print(determinant(1, matrix_1.contents_numeric))
    else:
        print('Matrix must be square!')


def action_6():
    rows, columns = input('Enter matrix size: ').split()
    rows = int(rows)
    columns = int(columns)
    print('Enter matrix:')
    matrix_1 = Matrix(True, None, rows, columns)
    det = determinant(1, matrix_1.contents_numeric)
    if det == 0:
        print('This matrix does not have an inverse.')
    else:
        print('The result is:')
        matrix_2 = Matrix(False, cofactor_matrix(matrix_1.contents_numeric), rows, columns)
        matrix_3 = Matrix(False, matrix_2.multiplication_integer(1/det), rows, columns)
        matrix_3.structured_form()


def home():
    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate a determinant")
    print("6. Inverse matrix")
    print("0. Exit")
    action = input('Your choice: ')
    if action == '1':
        action_1()
        print()
        home()
    elif action == '2':
        action_2()
        print()
        home()
    elif action == '3':
        action_3()
        print()
        home()
    elif action == '4':
        action_4()
        print()
        home()
    elif action == '5':
        action_5()
        print()
        home()
    elif action == '6':
        action_6()
        print()
        home()
    elif action == '0':
        exit()
    else:
        print("That is not a valid option!")
        home()


home()
