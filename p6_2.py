from collections import defaultdict, deque
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

def traverse(nodes, source, target):
    history = {source: None}
    q = deque()
    q.appendleft(source)
    while q:
        id = q.pop()
        if id == target:
            break
        node = nodes[id]
        edges = set(node.orbits)
        if node.source:
            edges.add(node.source)
        for o in edges:
            if o not in history:
                q.appendleft(o)
                history[o] = id

    path = []
    id = history[target]
    while id != source:
        path.append(nodes[id])
        id = history[id]
    path.reverse()
    return path

def count_hops(nodes, source, target):
    path = traverse(nodes, source, target)
    return len(path) - 1

@pytest.mark.parametrize('input,source,target,output', [
    (
        'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN',
        'YOU',
        'SAN',
        4,
    ),
])
def test(input, source, target, output):
    orbits = parse_input(input)
    nodes = build_nodes(orbits)
    result = count_hops(nodes, source, target)
    assert result == output

def main():
    with open('p6.input') as fp:
        input = fp.read()

    orbits = parse_input(input)
    nodes = build_nodes(orbits)
    output = count_hops(nodes, 'YOU', 'SAN')
    print(output)

if __name__ == '__main__':
    main()
