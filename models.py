# MODEL.PY

from dataclasses import dataclass, field


# Stores information about one payment
@dataclass
class Payment:
    amount: float
    date: str


# Stores information about one hostel room
@dataclass
class Room:
    capacity: int
    occupants: list = field(default_factory=list)

    def is_full(self):
        return len(self.occupants) >= self.capacity

    def has_space(self):
        return len(self.occupants) < self.capacity


# Stores information about one student
@dataclass
class Student:
    name: str
    reg_no: str
    gender: str
    course: str
    year: str
    total_fee: float
    block: str = None
    room: str = None
    amount_paid: float = 0
    payments: list = field(default_factory=list)

    @property
    def balance(self):
        return self.total_fee - self.amount_paid

    def get_balance(self):
        return self.total_fee - self.amount_paid

    @property
    def is_allocated(self):
        return self.block is not None and self.room is not None