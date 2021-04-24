'''
Short script for generating a n*m matrix which values are determined by two path matrices 'down' and 'right'.
For the rosalind task 'Find the Length of a Longest Path in a Manhattan-like Grid' (http://rosalind.info/problems/ba5b/)
I had to write a primitive matrix class, because I wrote the script on my iPad without python modules. lel.
'''

class Matrix:

    def __init__(self, n, m, z=0):
        self.matrix = []
        for i in range(n):
            row = []
            for j in range(m):
                row.append(z)
            self.matrix.append(row)

    def __str__(self):
        output = '\n[\n'
        for row in self.matrix:
            output += str(row) + '\n'
        output += ']\n'
        return output

def parse(file):
    '''
    Overly complicated parser for the input file given by Rosalind.info.
    '''
    with open(file) as fin:
        lines = fin.readlines()
        n, m = lines[0].strip().split(' ')
        n, m = int(n), int(m)
        down = Matrix(n, m+1)
        right = Matrix(n+1, m)
        identifier = 'd'
        d_matrix = []
        r_matrix = []
        for line in lines[1:]:
            row = [identifier]
            if line[0] == '-':
                identifier = 'r'
                continue
            for num in line.strip().split(' '):
                row.append(int(num))
            if row[0] == 'd':
                d_matrix.append(row[1:])
            elif row[0] == 'r':
                r_matrix.append(row[1:])
        for i in range(n):
            for j in range(m+1):
                down.matrix[i][j] = d_matrix[i][j]
        for i in range(n+1):
            for j in range(m):
                right.matrix[i][j] = r_matrix[i][j]
        return n, m, down, right


def tourist(n, m, down, right):
    '''
    Generates a n+1, m+1 matrix and evaluates it using the 'down' and 'right' matrix.
    '''
    mx = Matrix(n+1, m+1)
    for i in range(n):
        mx.matrix[i+1][0] = mx.matrix[i][0] + down.matrix[i][0]
    for j in range(m):
        mx.matrix[0][j+1] = mx.matrix[0][j] + right.matrix[0][j]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            mx.matrix[i][j] = max(mx.matrix[i - 1][j] + down.matrix[i - 1][j],
                                  mx.matrix[i][j - 1] + right.matrix[i][j - 1])
    return mx

n, m, down, right = parse('Manhattan_Tourist_input.txt')
print(tourist(n, m, down, right))