import numpy as np


def read_file(file):
    '''
    Simple FASTA reader.
        Input: .fasta file ">entry\nATCTGTCGGCTGCTGCTGC...\n...\n>entry2\nATCTGAGTACGATCGT..."
        Output: - dictionary mapping entry string to sequence string {'entry':'ATCTGTCGGCTGCTGCTGC...', ...}
                - list containing the order of sequences ['entry', 'entry2', ...]
    '''
    entries = dict()
    order = list()
    with open(file) as fin:
        entry = ''
        for line in fin:
            if line.strip() == '':
                continue
            if line[0] == '>':
                entry = line[1:].strip()
                entries[entry] = ''
                order.append(entry)
                continue
            if entry != '':
                entries[entry] += line.strip()
    return entries, order


def create_matrix(seq1, seq2):
    '''
    Creates an m * n alignment matrix filled with zeroes. With m = length(seq1) + 1 and n = length(seq2) + 1.
    '''
    return np.zeros((len(seq1) + 1, len(seq2) + 1), dtype=int)


def initialize_matrix(matrix):
    '''
    Initializes the alignment matrix (first row and file of the matrix filled with correct numbers).
    '''
    n, m = matrix.shape
    for i in range(n):
        matrix[i][0] = i
    for j in range(m):
        matrix[0][j] = j


def enumerate_matrix(seq1, seq2):
    '''
    Creates and initializes an alignment matrix based on the two provided sequences.Calculates the values in the
    alignment matrix. Each value is calculated as the minimum of three possible values:
        1) Upper neighboring vertical value + 1
        2) Horizontal value to the left + 1
        3) Diagonal value to the upper left + 1 (if characters in the sequences do not match; represents substitution)
            or diagonal value to the upper left + 0 (if characters in the sequences match; represents not editing)
    See "Bioinformatic Algorithms: An Active Learning Approach" (Compeau & Pevzner, 2014), Chapter 5 for more
    information on dynamic programming.
    '''
    matrix = create_matrix(seq1, seq2)
    initialize_matrix(matrix)
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            vertical = matrix[i-1][j] + 1
            horizontal = matrix[i][j-1] + 1
            if seq1[i-1] == seq2[j-1]:
                diagonal = matrix[i-1][j-1]
            else:
                diagonal = matrix[i-1][j-1] + 1
            matrix[i][j] = min(vertical, horizontal, diagonal)
    return matrix


def backtrack(seq1, seq2, matrix):
    copy1 = seq1
    copy2 = seq2
    align1 = ''
    align2 = ''
    i, j = matrix.shape
    i -= 1
    j -= 1
    while i > 0 or j > 0:
        '''
        General workflow and changing of variables is right. But the matrix right now is enumerated in a way,
        that encourages wrong paths with equal value through it. Path information is lost in flat landscapes.
        Every node has its point derived from neighboring nodes, but when all nodes have same value in neighborhood
        origin of individual node points is obscured!
        
        Must find a way to retain directional information even in flat value landscapes!
        '''
        vertical = matrix[i-1][j]
        horizontal = matrix[i][j-1]
        diagonal = matrix[i-1][j-1]
        choice = min(vertical, horizontal, diagonal)
        if choice == vertical:
            copy1, char = copy1[:-1], copy1[-1]
            align1 += '-'
            align2 += char
            i -= 1
            continue
        elif choice == horizontal:
            copy2, char = copy2[:-1], copy2[-1]
            align1 += char
            align2 += '-'
            j -= 1
            continue
        elif choice == diagonal:
            copy2, char2 = copy2[:-1], copy2[-1]
            copy1, char1 = copy1[:-1], copy1[-1]
            align1 += char2
            align2 += char1
            i -= 1
            j -= 1
            continue
    return align1[::-1], align2[::-1]



def main():
    # Read .fasta file and get sequences
    sequences, order = read_file("Manhattan_Tourist_input.txt")
    seq1, seq2 = sequences[order[0]], sequences[order[1]]
    # Create and enumerate the edit / alignment matrix
    matrix = enumerate_matrix(seq1, seq2)
    # Print out the last value in the matrix which represents the minimal edit distance
    print(matrix[len(seq1)][len(seq2)])
    print(backtrack(seq1, seq2, matrix))


if __name__ == '__main__':
    main()
