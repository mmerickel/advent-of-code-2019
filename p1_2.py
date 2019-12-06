import pytest

calc_fuel_cost = lambda mass: mass // 3 - 2

def calc_total_fuel_cost(mass):
    total_cost = 0
    while True:
        cost = calc_fuel_cost(mass)
        if cost <= 0:
            break

        total_cost += cost
        mass = cost
    return total_cost

@pytest.mark.parametrize('mass,fuel', [
    (14, 2),
    (1969, 966),
    (100756, 50346),
])
def test_it(mass, fuel):
    assert calc_total_fuel_cost(mass) == fuel

def main():
    with open('p1.input', 'r') as fp:
        lines = fp.readlines()
    values = [int(line.strip()) for line in lines]
    result = sum(calc_total_fuel_cost(x) for x in values)
    print(result)

if __name__ == '__main__':
    main()
