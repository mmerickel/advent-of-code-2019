import pytest

from p3_1 import parse_paths, render_path, find_intersection_points

def count_steps_to_point(path, target):
    # position in list does not include starting point (0, 0) so add one step
    return path.index(target) + 1

def process_input(input):
    paths = parse_paths(input)
    points = [render_path(path) for path in paths]
    intersecting_points = find_intersection_points(*points)
    return min(
        count_steps_to_point(points[0], t) + count_steps_to_point(points[1], t)
        for t in intersecting_points
    )

@pytest.mark.parametrize('input,expected', [
    (
        'R75,D30,R83,U83,L12,D49,R71,U7,L72\n'
        'U62,R66,U55,R34,D71,R55,D58,R83',
        610,
    ),
    (
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
        410,
    ),
])
def test(input, expected):
    result = process_input(input)
    assert result == expected

def main():
    with open('p3.input') as fp:
        input = fp.read()

    result = process_input(input)
    print(result)

if __name__ == '__main__':
    main()
