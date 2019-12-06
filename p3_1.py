import pytest

def parse_paths(input):
    return [
        parse_path(line.strip())
        for line in input.strip().split('\n')
    ]

def parse_path(path):
    return [
        (i[0], int(i[1:]))
        for i in path.strip().split(',')
    ]

MOVES = {
    'R': lambda x, y: (x + 1, y),
    'L': lambda x, y: (x - 1, y),
    'U': lambda x, y: (x, y + 1),
    'D': lambda x, y: (x, y - 1),
}

def render_path(path):
    x = y = 0
    points = set()
    for dir, m in path:
        move = MOVES[dir]
        for i in range(m):
            x, y = move(x, y)
            points.add((x, y))
    return points

def find_closest_intersection(a, b):
    a_pts = render_path(a)
    b_pts = render_path(b)
    points = a_pts.intersection(b_pts)
    return min(
        abs(x) + abs(y)
        for x, y in points
    )

@pytest.mark.parametrize('input,expected', [
    (
        'R75,D30,R83,U83,L12,D49,R71,U7,L72\n'
        'U62,R66,U55,R34,D71,R55,D58,R83',
        159,
    ),
    (
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
        135,
    ),
])
def test(input, expected):
    a, b = parse_paths(input)
    result = find_closest_intersection(a, b)
    assert result == expected

def main():
    with open('p3.input') as fp:
        input = fp.read()

    a, b = parse_paths(input)
    result = find_closest_intersection(a, b)
    print(result)

if __name__ == '__main__':
    main()
