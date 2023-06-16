from dataclasses import dataclass


@dataclass
class ParametrActivity:
    accessibility: float
    type: str
    participants: int
    price: float
