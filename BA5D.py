# Find longest path in weighted directed acyclic graph - iPad script

def reader(file):
    seqs = list()
    with open(file) as fin:
        for line in fin:
            seqs.append(line.strip())
    return seqs


input = reader('input.txt')
start = int(input[0])
end = int(input[1])
edges = input[2:]
numeric_edges = []

for edge in edges:
    edge_start, edge_remainder = int(edge.split('-')[0]), edge.split('-')[1][1:]
    edge_end, edge_weight = int(edge_remainder.split(':')[0]), int(edge_remainder.split(':')[1])
    numeric_edges.append((edge_start, edge_end, edge_weight))

print(numeric_edges)