from dataclasses import dataclass
from model.chromosone import Chromosone
@dataclass
class Connection:
    Chromosome1:int
    Chromosome2:int
    gene1: int
    gene2: int
    corr:float

