from p2_1 import parse_program, run_program

def find_program_inputs(program, output):
    for x in range(100):
        for y in range(100):
            test_prog = list(program)
            test_prog[1] = x
            test_prog[2] = y
            run_program(test_prog)
            if test_prog[0] == output:
                return x, y
    raise RuntimeError('could not find a valid combination')

def main():
    with open('p2.input') as fp:
        input = fp.readline()

    program = parse_program(input)
    x, y = find_program_inputs(program, 19690720)
    print(100 * x + y)

if __name__ == '__main__':
    main()
