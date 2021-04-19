def read_file(file):
    '''
    Simple FASTA reader.
        Input: .fasta file [>entry\nATCTGTCGGCTGCTGCTGC...\n>entry2\nATCTGAGTACGATCGT...]
        Output: dictionary mapping entry string to sequence string {'entry':'ATCTGTCGGCTGCTGCTGC...', ...}
                list containing the order of sequences
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




sequences, order = read_file("input.txt")