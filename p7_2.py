import itertools
import pytest

from p5_2 import run_program

def make_input(phase, signal):
    yield phase
    yield from signal

def run_thrusters(program, sequence):
    last_output = None
    def feedback():
        nonlocal last_output
        while True:
            assert last_output is not None
            value, last_output = last_output, None
            yield value
    signal = itertools.chain([0], feedback())
    for phase in sequence:
        input = make_input(phase, signal)
        signal = run_program(program, input, stream=True)

    for value in signal:
        last_output = value
    return last_output

def find_max_thrust(program):
    best = [0, None]
    for sequence in itertools.permutations(list(range(5, 10))):
        thrust = run_thrusters(program, sequence)
        if thrust > best[0]:
            best = [thrust, sequence]
    return best

@pytest.mark.parametrize('program,sequence,thrust', [
    (
        '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,'
        '27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5',
        [9, 8, 7, 6, 5],
        139629729,
    ),
    (
        '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,'
        '-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,'
        '53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10',
        [9, 7, 8, 5, 6],
        18216,
    ),
])
def test(program, sequence, thrust):
    result = run_thrusters(program, sequence)
    assert result == thrust

def main():
    with open('p7.input') as fp:
        program = fp.read()

    best = find_max_thrust(program)
    print(best[1])
    print(best[0])

if __name__ == '__main__':
    main()
