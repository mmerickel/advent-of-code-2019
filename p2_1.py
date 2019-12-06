import pytest

def parse_program(input):
    return [int(x) for x in input.strip().split(',')]

def run_program(program):
    i = 0
    while True:
        op = program[i]
        if op == 99:
            break

        elif op == 1:
            x, y, z = program[i + 1: i + 4]
            program[z] = program[x] + program[y]
            i += 4

        elif op == 2:
            x, y, z = program[i + 1: i + 4]
            program[z] = program[x] * program[y]
            i += 4

        else:
            raise RuntimeError(f'invalid opcode={op}')

@pytest.mark.parametrize('input,expected', [
    ('1,0,0,0,99', '2,0,0,0,99'),
    ('2,3,0,3,99', '2,3,0,6,99'),
    ('2,4,4,5,99,0', '2,4,4,5,99,9801'),
    ('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99'),
])
def test(input, expected):
    program = parse_program(input)
    run_program(program)
    result = ','.join(str(x) for x in program)
    assert result == expected

def main():
    with open('p2.input') as fp:
        input = fp.readline()

    program = parse_program(input)
    program[1] = 12
    program[2] = 2
    run_program(program)
    print(program[0])

if __name__ == '__main__':
    main()
