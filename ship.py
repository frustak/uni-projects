import time
from random import randrange


class Ship:
    """Represents a ship."""

    MAX_HIT_POINTS = 2
    FIRE_DAMAGE = 1
    MIN_PREPARE_TIME = 1
    MAX_PREPARE_TIME = 3

    def __init__(self, name: str):
        self.name = name
        self._hit_points = Ship.MAX_HIT_POINTS

    @staticmethod
    def generate_prepare_time() -> int:
        """Generate a random number between `MIN_PREPARE_TIME` and `MAX_PREPARE_TIME`."""
        return randrange(
            start=Ship.MIN_PREPARE_TIME, stop=Ship.MAX_PREPARE_TIME)

    def prepare_to_shoot(self, prepare_time: float):
        """Prepare the ship to shoot, takes some amount of time."""
        print(f"{self.name} takes {prepare_time} seconds to prepare.")
        time.sleep(prepare_time)

    def fire_at(self, target: "Ship"):
        """Commands current ship to fire at another one."""
        if self == target:
            raise Exception("Cannot attack itself!")
        target._take_damage(Ship.FIRE_DAMAGE)
        print(f"{self.name} fired at the {target.name}.")
        self._print_if_drowned(target)

    def is_destroyed(self) -> bool:
        """Check if a ship is destroyed."""
        return self._hit_points == 0

    def _take_damage(self, amount: int):
        """Cause a ship to take an amount of damage, if it's not already destroyed."""
        if self._hit_points > 0:
            self._hit_points -= amount
        else:
            raise Exception(
                f"Cannot damage a destroyed ship! ship name:{self.name}")

    def _print_if_drowned(self, target: "Ship"):
        """Print a message if target is drowned."""
        if target.is_destroyed():
            print(f"{target.name} was drowned by {self.name}")
