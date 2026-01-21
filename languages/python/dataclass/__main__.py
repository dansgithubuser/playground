from dataclasses import asdict, dataclass
import json

@dataclass
class C:
    x: int
    y: int

print(C(0, 1))
print(C(x=0, y=1))
print(json.dumps(asdict(C(0, 1))))
