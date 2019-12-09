import itertools
import pytest

from p5_2 import run_program

def run_amplifier(program, phase, input):
    output = run_program(program, [phase, input])
    return output[0]

def run_thrusters(program, sequence):
    signal = 0
    for phase in sequence:
        signal = run_amplifier(program, phase, signal)
    return signal

def find_max_thrust(program):
    best = [0, None]
    for sequence in itertools.permutations(list(range(5))):
        thrust = run_thrusters(program, sequence)
        if thrust > best[0]:
            best = [thrust, sequence]
    return best

@pytest.mark.parametrize('program,sequence,thrust', [
    (
        '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0',
        [4, 3, 2, 1, 0],
        43210,
    ),
    (
        '3,23,3,24,1002,24,10,24,1002,23,-1,23,'
        '101,5,23,23,1,24,23,23,4,23,99,0,0',
        [0, 1, 2, 3, 4],
        54321,
    ),
    (
        '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,'
        '1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0',
        [1, 0, 4, 3, 2],
        65210,
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
