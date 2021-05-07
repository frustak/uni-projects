import threading
from random import randrange
from typing import Callable, List
from ship import Ship
from utils import print_centered, wait_for_threads


class Game:
    """Represents a game."""

    def __init__(self, ship_count: int):
        self._ships: List[Ship] = [None] * ship_count

    def start(self):
        """Start the game."""
        print_centered("START WAR")
        self._spawn_ships()
        return self

    def battle(self):
        """Begin the battle with all ships, each in an individual thread."""
        ship_threads = self._command_ships_to_begin()
        wait_for_threads(ship_threads)
        return self

    def end(self):
        """End the game."""
        self._check_has_ended()
        print_centered("END WAR")
        print_centered(f"Winner: {self._get_winner().name}")

    def _command_ships_to_begin(self) -> List[threading.Thread]:
        """Start each ship logic in an individual thread and return the threads."""
        threads: List[threading.Thread] = list()
        for i in range(self._ship_counts()):
            thread = threading.Thread(
                target=self._run_logic, args=(self._ships[i],))
            thread.start()
            threads.append(thread)
        return threads

    def _spawn_ships(self):
        """Spawn all the ships"""
        for i in range(self._ship_counts()):
            self._ships[i] = Ship(f"Ship {i + 1}")

    def _get_random_ship(self, excluded_ship: Ship) -> Ship:
        """Get another random ship different than excluded."""
        self._check_has_not_ended()
        ship_count = self._ship_counts()
        index = randrange(start=0, stop=ship_count)
        if self._ships[index] == excluded_ship:
            if index < ship_count:
                return self._ships[index + 1]
            else:
                return self._ships[index - 1]
        else:
            return self._ships[index]

    def _command_prepare(self, ship: Ship):
        """Prepare a ship to attack."""
        prepare_time = Ship.generate_prepare_time()
        ship.prepare_to_shoot(prepare_time)
        return self

    def _command_fire(self, attacker: Ship):
        """Commands a ship to fire at another ship."""
        try:
            target = self._get_random_ship(excluded_ship=attacker)
            attacker.fire_at(target)
            if target.is_destroyed():
                self._ships.remove(target)
        except:
            if not self._has_winner():
                self._command_fire(attacker=attacker)

    def _run_logic(self, current_ship: Ship):
        """Run game logic for a single ship."""
        while not current_ship.is_destroyed() and not self._has_winner():
            self._command_prepare(ship=current_ship)._command_fire(
                attacker=current_ship)

    def _ship_counts(self) -> int:
        """Return total number of afloat ships."""
        return len(self._ships)

    def _has_winner(self) -> bool:
        """Return true if game has winner (one ship is only left)."""
        return self._ship_counts() == 1

    def _get_winner(self) -> Ship:
        """Get the winner ship if there's a winner yet."""
        if self._has_winner():
            return self._ships[0]

    def _check_has_ended(self):
        """Check if a game has ended."""
        if not self._has_winner():
            raise Exception("Game has no winner yet!")

    def _check_has_not_ended(self):
        """Check if a game has not ended yet."""
        if self._has_winner():
            raise Exception("Game has not ended yet!")
