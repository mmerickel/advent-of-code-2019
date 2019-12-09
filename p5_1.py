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

def run_program(program, input=()):
    ctx = Runtime(program, iter(input))
    while not ctx.halt:
        op, params = parse_instruction(ctx)
        op.impl(ctx, *params)
        ctx.i += op.num_params + 1
    return ctx.output

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
    with open('p5.input') as fp:
        input = fp.readline()

    program = parse_program(input)
    output = run_program(program, [1])
    print('\n'.join(str(x) for x in output))

if __name__ == '__main__':
    main()
