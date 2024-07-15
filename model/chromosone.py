from dataclasses import dataclass
@dataclass
class Chromosone:
    id:int

    def __hash__(self):
        return self.id
