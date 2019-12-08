from dataclasses import dataclass, field
import pytest
import typing

def parse_program(input):
    return [int(x) for x in input.strip().split(',')]

@dataclass
class Runtime:
    memory: typing.List[int]
    input: typing.Iterable[int] = field(default_factory=lambda: iter([]))
    output: typing.List[int] = field(default_factory=list)

    i: int = 0
    halt: bool = False

    def get(self, param):
        x, mode = param
        if mode == 1:
            return x
        return self.memory[x]

    def set(self, param, value):
        x, mode = param
        assert mode == 0, 'cannot write in immediate mode'
        self.memory[x] = value

    def read_input(self):
        return next(self.input)

    def write_output(self, value):
        self.output.append(value)

@dataclass
class Operation:
    code: int
    num_params: int
    impl: typing.Callable[[Runtime], None]

OPS = {}

def register_op(code, num_params):
    def register(fn):
        OPS[code] = Operation(code, num_params, fn)
        return fn
    return register

@register_op(99, 0)
def op_99(ctx):
    ctx.halt = True

@register_op(1, 3)
def op_1(ctx, x, y, z):
    ctx.set(z, ctx.get(x) + ctx.get(y))

@register_op(2, 3)
def op_2(ctx, x, y, z):
    ctx.set(z, ctx.get(x) * ctx.get(y))

@register_op(3, 1)
def op_3(ctx, x):
    ctx.set(x, ctx.read_input())

@register_op(4, 1)
def op_4(ctx, x):
    ctx.write_output(ctx.get(x))

@register_op(5, 2)
def op_5(ctx, x, y):
    if ctx.get(x) != 0:
        return ctx.get(y)

@register_op(6, 2)
def op_6(ctx, x, y):
    if ctx.get(x) == 0:
        return ctx.get(y)

@register_op(7, 3)
def op_7(ctx, x, y, z):
    if ctx.get(x) < ctx.get(y):
        ctx.set(z, 1)
    else:
        ctx.set(z, 0)

@register_op(8, 3)
def op_8(ctx, x, y, z):
    if ctx.get(x) == ctx.get(y):
        ctx.set(z, 1)
    else:
        ctx.set(z, 0)

def parse_instruction(ctx):
    s = str(ctx.memory[ctx.i])
    opcode = int(s[-2:])
    op = OPS.get(opcode)
    if op is None:
        raise RuntimeError(f'unknown instruction={s} at position={ctx.i}')

    modes = [int(x) for x in s[:-2]]
    modes.reverse()
    modes += [0] * (op.num_params - len(modes))
    params = list(zip(
        ctx.memory[ctx.i + 1: ctx.i + 1 + op.num_params],
        modes,
    ))
    return op, params

def join_params(params, modes):
    return list(zip(params, modes))

def run_program(program, input=()):
    ctx = Runtime(program, iter(input))
    while not ctx.halt:
        op, params = parse_instruction(ctx)
        jump = op.impl(ctx, *params)
        if jump is not None:
            ctx.i = jump
        else:
            ctx.i += op.num_params + 1
    return ctx.output

@pytest.mark.parametrize('program,input,output', [
    ('3,9,8,9,10,9,4,9,99,-1,8', [7], [0]),
    ('3,9,8,9,10,9,4,9,99,-1,8', [8], [1]),
    ('3,9,8,9,10,9,4,9,99,-1,8', [9], [0]),
    ('3,9,7,9,10,9,4,9,99,-1,8', [7], [1]),
    ('3,9,7,9,10,9,4,9,99,-1,8', [8], [0]),
    ('3,9,7,9,10,9,4,9,99,-1,8', [9], [0]),
    ('3,3,1108,-1,8,3,4,3,99', [7], [0]),
    ('3,3,1108,-1,8,3,4,3,99', [8], [1]),
    ('3,3,1108,-1,8,3,4,3,99', [9], [0]),
    ('3,3,1107,-1,8,3,4,3,99', [7], [1]),
    ('3,3,1107,-1,8,3,4,3,99', [8], [0]),
    ('3,3,1107,-1,8,3,4,3,99', [9], [0]),
    ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [0], [0]),
    ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [1], [1]),
    ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [-1], [1]),
    ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [0], [0]),
    ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [1], [1]),
    ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [-1], [1]),
    (
        '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
        '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,'
        '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
        [7],
        [999],
    ),
    (
        '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
        '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,'
        '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
        [8],
        [1000],
    ),
    (
        '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
        '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,'
        '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
        [9],
        [1001],
    ),
])
def test(program, input, output):
    program = parse_program(program)
    result = run_program(program, input)
    assert result == output

def main():
    with open('p5.input') as fp:
        input = fp.readline()

    program = parse_program(input)
    output = run_program(program, [5])
    print('\n'.join(str(x) for x in output))

if __name__ == '__main__':
    main()
