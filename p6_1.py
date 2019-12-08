from collections import defaultdict
from dataclasses import dataclass, field
import pytest
import typing

def parse_input(input):
    return [
        line.split(')', 1)
        for line in input.strip().split('\n')
    ]

@dataclass
class Node:
    id: str
    source: typing.Optional[str] = None
    orbits: typing.Set[str] = field(default_factory=set)

def build_nodes(orbits):
    nodes = defaultdict(list)

    def get_node(id):
        node = nodes.get(id)
        if node is None:
            node = nodes[id] = Node(id)
        return node

    for a, b in orbits:
        a = get_node(a)
        b = get_node(b)
        b.source = a.id
        a.orbits.add(b.id)

    return nodes

def sorted_nodes(nodes):
    result = []
    visited = set()

    def visit(node):
        if node.id in visited:
            return
        for orbit in node.orbits:
            visit(nodes[orbit])
        visited.add(node.id)
        result.insert(0, node)

    for node in nodes.values():
        visit(node)

    return result

def count_orbits(nodes):
    total_per_node = {}
    for node in sorted_nodes(nodes):
        if node.source is None:
            total_per_node[node.id] = 0
        else:
            total_per_node[node.id] = 1 + total_per_node[node.source]
    return sum(x for x in total_per_node.values())

@pytest.mark.parametrize('input,output', [
    ('COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L', 42),
])
def test(input, output):
    orbits = parse_input(input)
    nodes = build_nodes(orbits)
    result = count_orbits(nodes)
    assert result == output

def main():
    with open('p6.input') as fp:
        input = fp.read()

    orbits = parse_input(input)
    nodes = build_nodes(orbits)
    output = count_orbits(nodes)
    print(output)

if __name__ == '__main__':
    main()
