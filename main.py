from game import Game


def receive_ship_count() -> int:
    """Get total number of ships from terminal input."""
    print("Enter the number of ships (N): ")
    ship_count = int(input())
    if ship_count < 1:
        raise Exception("Number of ships cannot be less than 1!")
    return ship_count


if __name__ == "__main__":
    ship_count = receive_ship_count()
    Game(ship_count=ship_count).start().battle().end()
