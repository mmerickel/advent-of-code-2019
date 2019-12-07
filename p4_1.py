def parse_input(input):
    return [int(x) for x in input.strip().split('-', 1)]

def is_valid(x):
    digits = [int(x) for x in str(x)]
    has_same = False
    for i in range(len(digits) - 1):
        if digits[i + 1] < digits[i]:
            return False

        if digits[i] == digits[i + 1]:
            has_same = True

    if not has_same:
        return False

    return True

def iter_passwords(lo, hi):
    for x in range(lo, hi):
        if is_valid(x):
            yield x

def main():
    input = '168630-718098'
    lo, hi = parse_input(input)
    passwords = list(iter_passwords(lo, hi))
    print(len(passwords))

if __name__ == '__main__':
    main()
