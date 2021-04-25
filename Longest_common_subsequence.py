'''
Used to solve "Find a Longest Common Subsequence of Two Strings" on Rosalind.info.
See http://rosalind.info/problems/ba5c/ for more information.
'''

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


def create_diagonal_vectors(seq1, seq2):
    '''
    Calculates whether an alignment of two characters in sequences seq1 and seq2 is a match (= 1) or a mismatch (= 0).
    It uses this information to create a diagonal vector matrix used for the generation of aan alignment map.
    '''
    diagonal = np.zeros((len(seq1), len(seq2)), dtype=int)
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                diagonal[i][j] = 1
            else:
                diagonal[i][j] = 0
    return diagonal


def enumerate_matrix(seq1, seq2):
    '''
    Creates an alignment map of two sequences seq1 and seq2 and creates a backtrack map from it. For this three
    directional vector matrices are created (down, all vectors pointing down; right, all vectors pointing right;
    diagonal, all vectors pointing diagonally down-right). The right vector used for each point in the alignment
    map is the minimum of all corresponding points in the down, right or diagonal vector.

    See Bioinformatic Algorithms (Compeau, Pevzner), Chapter 5. Its too complicated for a short comment like this.
    '''
    m = len(seq1)
    n = len(seq2)
    map = np.zeros((m + 1, n + 1), dtype=int)
    right = np.zeros((m + 1, n), dtype=int)
    down = np.zeros((m, n + 1), dtype=int)
    diagonal = create_diagonal_vectors(seq1, seq2)
    backtrack = np.zeros((m+1, n+1), dtype=int) # right: 0; down: 1; diagonal: 2

    # Enumerate rims
    for i in range(m):
        map[i+1][0] = map[i][0] + down[i][0]
        backtrack [i+1][0] = 1
    for j in range(n):
        map[0][j+1] = map[0][j] + right[0][j]
        backtrack[0][j+1] = 0

    # Enumerate center
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            map[i][j] = max(map[i][j-1] + right[i][j-1], map[i-1][j] + down[i-1][j], map[i-1][j-1] + diagonal[i-1][j-1])
            if map[i][j] == map[i][j-1] + right[i][j-1]:
                backtrack[i][j] = 0
            elif map[i][j] == map[i-1][j] + down[i-1][j]:
                backtrack[i][j] = 1
            elif map[i][j] == map[i-1][j-1] + diagonal[i-1][j-1]:
                backtrack[i][j] = 2
    return map, backtrack


def backtrack(seq1, seq2, backtrack):
    '''
    Uses a backtrack map to align two sequences seq1 and seq2 and return the longest common subsequence of both.
    '''
    copy1 = seq1
    copy2 = seq2
    align1 = ''
    align2 = ''
    i = len(seq1)
    j = len(seq2)
    while i > 0 or j > 0:
        if backtrack[i][j] == 1:
            copy1, char = copy1[:-1], copy1[-1]
            i -= 1
            continue
        elif backtrack[i][j] == 0:
            copy2, char = copy2[:-1], copy2[-1]
            j -= 1
            continue
        elif backtrack[i][j] == 2:
            copy2, char2 = copy2[:-1], copy2[-1]
            copy1, char1 = copy1[:-1], copy1[-1]
            align1 += char2
            i -= 1
            j -= 1
            continue
    return align1[::-1]


def main():
    seq1 = 'CTACGCCTCGAGAGTGAACGGGCTTCAGGACTGAGTAATGGCTCCGAATACATCATCCCGGGAGATAGCCTACGGTTCTACGTCAAAGTGAACGAA' \
           'ATATACGTTCACACAAGCTTTAGTCAAGGCCTATCCGCTCATAAGCGCCTGTTCCGGAGACAGCATACGAGGCCGTTAGTGGTGAAAAACGGAGTA' \
           'ATTATGCTGACCATCGCGGAAGTTATCATCAGTTTAATTTAACCCACAGCAACTGTGATGGGGACTCTTCTGTTGCTCGAATACCTTTATTGTCAT' \
           'GTGCACAATGGAGGGTTGGTCCTTGATCGGACTGTTTGGAGACTGCACAGAGATTCGCCGGCCTATTACATCCTAGTCCTGAGGTAAATTTATATC' \
           'CTGCCAATATCTATGAAGAATTCAGTACTGAAATGAGTCGATCCGGAGACTGGGAAAACTCTAACGGAGTGCTGTCCTCTAGTGCGGTTGAATGGC' \
           'AAGGGTGGGCAATAAGTAATGACATCTTAAATAGTGGAAGACTGTGGTTAGTGGACACATACATTCCCAGATGTTTACTAATTTAGTGGGACTTGG' \
           'GGTGCCCGCATGTTATAACTCTCATCAGAGCTTTCCCCGGAGTAGACCGCCTGTCAGTCTCGGGGCCGAACAGGACGTTGACATGGTGAGGCCACT' \
           'TATGCACACAGCTTAACGAAGTTCAACAAGTGTACACAAAGCGGCTTGTGGAAGCCCCCCTTCATAATATCCTGGTACGTCGAAACCGGGACTCTC' \
           'CAGCATCAGTCATGGCTCGCTCTCCCTACCGAGACATCTATGGGTACACGGGACCGTGGTTCACTGTGGATATGAGTTCCAGATCTCGTCCGCGAC' \
           'TCCCCTTGTAACTGCCGTCTATGTCCAATGGTGCTCTGTAAAAGAGGACAGAATGTTACACCACGTGGGCAACTGTCGCCTGGTGAAAGTCCTTCA' \
           'CTGT '
    seq2 = 'TCCGTATTTACGGCTTAGTAGGTCTGGCCTGGCATTTTACGGGTACTCCGCCAAAGTGTACCCCTTAATGACAATCACTAAGTATGTGCCGGAGTA' \
           'AACAATATGCTGATCTAAGACCGGATACGAAGCCGCTGCCTTAGCTCTCCCTACACAGGCGCCCTGCAACCCTTGGCTATCATCTTGGTTCCGGTG' \
           'ATGGGGTTAAGTGCATCGATGCCAACATACGTTAGGACGCACTATGTCTCGTGCTCACGATGCAAAGATCAGCAGTACATGAGTTCTTGAGGCGGA' \
           'TTCTTCGTTGACAACTACTTATGGGAAAAAGTACTCTACTCTTTTTAATAATTTCACGGTTAAACTCACTTACTCGTGATAGCACGGCTGCCGCTG' \
           'TTATCGCCTGCCATGGAGGACTCGCTACTTCGCAATTGAGTTCTCCAACGAACCGTTTGGGTTGCCTGTCTAATAGCGGAATCGCCAGGCGAAGTG' \
           'TGTCAACTGTGAGGCGGCCCTTGAGCAGTACGCGCTTTTTGAACGAACTCATGCCAACAGACCAAACTAGCTGGATGTGGATTTCACACGCTCGCT' \
           'TTCCGACCAATTGAAGGAATCAATGGATAAGTTTTACTACATCGGGGTGCCGTTGACTCCTATGGACTGCGCCCCGCAGGTTAATACCCCAGGTGA' \
           'TTTTGCGGGAGCAGCCACAATGGACTTGGCCGGATATACGAGTCTAACCGCTGCGGGGCGGGCTCGAGTGTCGGGTGACAAATCCTCCATTAACAC' \
           'CCGCTTAAAATCGCGCCCTGCAGCCGGGCTTGGTCATGCAAGCGCGGA'
    map, tracker = enumerate_matrix(seq1, seq2)
    alignment = backtrack(seq1, seq2, tracker)
    print(alignment)


if __name__ == '__main__':
    main()
