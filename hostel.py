"""
Everything to do with the physical layout of the hostel: how many blocks
exist, how many rooms each block has, and how much space is left in a
given room.
"""

from typing import Dict
from models import Room

HostelLayout = Dict[str, Dict[str, Room]]


def ask_positive_int(prompt: str) -> int:
    """
    Repeats a prompt until the user enters a whole number greater than zero.
    """
    while True:
        raw_value = input(prompt).strip()

        if not raw_value.isdigit():
            print("Please enter a whole number greater than zero.")
            continue

        value = int(raw_value)

        if value <= 0:
            print("The number must be greater than zero.")
            continue

        return value


def build_hostel_layout() -> HostelLayout:
    """
    Interactively builds the hostel's block/room structure from scratch.
    """
    layout: HostelLayout = {}

    print("\nNo existing hostel layout was found - let's set one up.")

    number_of_blocks = ask_positive_int("How many hostel blocks are there? ")

    for block_index in range(1, number_of_blocks + 1):

        block_name = input(
            f"Name of block {block_index} (e.g. Block A): "
        ).strip()

        while not block_name:
            block_name = input(
                "Block name cannot be empty. Try again: "
            ).strip()

        number_of_rooms = ask_positive_int(
            f"How many rooms does {block_name} have? "
        )

        rooms: Dict[str, Room] = {}

        for room_index in range(1, number_of_rooms + 1):

            room_no = input(
                f"  Room number {room_index} of {block_name}: "
            ).strip()

            while not room_no or room_no in rooms:
                room_no = input(
                    "  Room number is empty or already used. Try again: "
                ).strip()

            capacity = ask_positive_int(
                f"  Capacity of room {room_no}: "
            )

            rooms[room_no] = Room(capacity=capacity)

        layout[block_name] = rooms

    print("\nHostel layout saved for this session.")
    return layout


def room_exists(layout: HostelLayout, block: str, room_no: str) -> bool:
    return block in layout and room_no in layout[block]


def get_room(layout: HostelLayout, block: str, room_no: str) -> Room:
    """
    Direct lookup - callers are expected to check room_exists() first.
    """
    return layout[block][room_no]


def display_occupancy(layout: HostelLayout) -> None:
    """
    Prints every block and every room's current occupancy in one pass.
    """
    print("\n========== HOSTEL OCCUPANCY REPORT ==========")

    for block_name, rooms in layout.items():
        print(f"\n{block_name.upper()}")

        for room_no, room in rooms.items():
            occupied = len(room.occupants)
            print(f"{room_no}: {occupied}/{room.capacity} occupied")


def add_occupant(
    layout: HostelLayout,
    block: str,
    room_no: str,
    reg_no: str
) -> None:
    room = get_room(layout, block, room_no)
    room.occupants.append(reg_no)


def remove_occupant(
    layout: HostelLayout,
    block: str,
    room_no: str,
    reg_no: str
) -> None:
    room = get_room(layout, block, room_no)

    if reg_no in room.occupants:
        room.occupants.remove(reg_no)


def total_capacity(layout: HostelLayout) -> int:
    """
    Total number of beds across every block.
    """
    return sum(
        room.capacity
        for rooms in layout.values()
        for room in rooms.values()
    )


def total_occupied(layout: HostelLayout) -> int:
    return sum(
        len(room.occupants)
        for rooms in layout.values()
        for room in rooms.values()
    )