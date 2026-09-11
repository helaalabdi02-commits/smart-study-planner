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
    occupants: list = field(default_factory=list) #new room fresh list  

    def is_full(self):
        return len(self.occupants) >= self.capacity #True

    def has_space(self):
        return len(self.occupants) < self.capacity #False


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

    def get_balance(self):
        return self.total_fee - self.amount_paid

    def is_allocated(self):
        return self.block is not None and self.room is not None #if they have both have room and block it returns true if not false 
    
