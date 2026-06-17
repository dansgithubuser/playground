from dataclasses import dataclass, field

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


try:
    @dataclass
    class C:
        l: list = []
except Exception as e:
    print(e)


@dataclass
class C:
    l: list = field(default_factory=list)
