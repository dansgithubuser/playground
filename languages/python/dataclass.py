from dataclasses import dataclass

@dataclass
class C:
    i: int
    l: list

def test(expr):
    print(expr)
    try:
        exec(f'print({expr})')
    except Exception as e:
        print(e)
    print()

test('C()')
test('C(1, 2)')
C(1, 2)
