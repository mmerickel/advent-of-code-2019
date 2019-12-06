import pytest

calc_fuel_cost = lambda mass: mass // 3 - 2

@pytest.mark.parametrize('mass,fuel', [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583),
])
def test_it(mass, fuel):
    assert calc_fuel_cost(mass) == fuel

def main():
    with open('p1.input', 'r') as fp:
        lines = fp.readlines()
    values = [int(line.strip()) for line in lines]
    result = sum(calc_fuel_cost(x) for x in values)
    print(result)

if __name__ == '__main__':
    main()
