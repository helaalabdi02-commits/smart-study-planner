"""
Handles the physical hostel layout, including blocks, rooms,
room capacities, and occupancy.
"""

from typing import Dict
from models import Room

# Block name -> room number -> Room
HostelLayout = Dict[str, Dict[str, Room]]


# Validate numbers used during hostel setup
def ask_positive_int(prompt: str) -> int:
    while True:
        raw_value = input(prompt).strip()

        # Make sure the input is a whole number
        if not raw_value.isdigit():
            print("Please enter a whole number greater than zero.")
            continue

        value = int(raw_value)

        # Do not allow zero or negative values
        if value <= 0:
            print("The number must be greater than zero.")
            continue

        return value


# Build the hostel layout from the user's input
def build_hostel_layout() -> HostelLayout:
    layout: HostelLayout = {}

    print("\nNo existing hostel layout was found - let's set one up.")

    # First ask how many blocks the hostel has
    number_of_blocks = ask_positive_int("How many hostel blocks are there? ")

    # Create each block one at a time
    for block_index in range(1, number_of_blocks + 1):
        block_name = input(
            f"Name of block {block_index} (e.g. Block A): "
        ).strip()

        # Block names cannot be left empty
        while not block_name:
            block_name = input(
                "Block name cannot be empty. Try again: "
            ).strip()

        number_of_rooms = ask_positive_int(
            f"How many rooms does {block_name} have? "
        )

        rooms: Dict[str, Room] = {}

        # Add each room and its capacity
        for room_index in range(1, number_of_rooms + 1):
            room_no = input(
                f"  Room number {room_index} of {block_name}: "
            ).strip()

            # Prevent empty or duplicate room numbers
            while not room_no or room_no in rooms:
                room_no = input(
                    "  Room number is empty or already used. Try again: "
                ).strip()

            capacity = ask_positive_int(
                f"  Capacity of room {room_no}: "
            )

            rooms[room_no] = Room(capacity=capacity)

        # Store all rooms under this block
        layout[block_name] = rooms

    print("\nHostel layout saved for this session.")
    return layout


# Check whether a requested room exists
def room_exists(
    layout: HostelLayout, block: str, room_no: str
) -> bool:
    return block in layout and room_no in layout[block]


# Find and return a specific room
def get_room(
    layout: HostelLayout, block: str, room_no: str
) -> Room:
    """Direct lookup - callers are expected to check room_exists() first."""
    return layout[block][room_no]


# Display the current occupancy of all rooms
def display_occupancy(layout: HostelLayout) -> None:
    print("\n========== HOSTEL OCCUPANCY REPORT ==========")

    for block_name, rooms in layout.items():
        print(f"\n{block_name.upper()}")

        for room_no, room in rooms.items():
            # Use the Room method to show its current status
            print(f"{room_no}: {room.occupancy_label()}")


# Add a student's registration number to a room
def add_occupant(
    layout: HostelLayout, block: str, room_no: str, reg_no: str
) -> None:
    room = get_room(layout, block, room_no)
    room.occupants.append(reg_no)


# Remove a student from their room
def remove_occupant(
    layout: HostelLayout, block: str, room_no: str, reg_no: str
) -> None:
    room = get_room(layout, block, room_no)

    if reg_no in room.occupants:
        room.occupants.remove(reg_no)


# Calculate the total number of beds
def total_capacity(layout: HostelLayout) -> int:
    return sum(
        room.capacity
        for rooms in layout.values()
        for room in rooms.values()
    )


# Calculate how many beds are currently occupied
def total_occupied(layout: HostelLayout) -> int:
    return sum(
        len(room.occupants)
        for rooms in layout.values()
        for room in rooms.values()
    )