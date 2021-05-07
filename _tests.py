import threading
import pytest
from ship import Ship
from game import Game

SHIP_COUNT = 10


# --------------------------------------- Ship Tests ---------------------------------------


def test_ship_init():
    ship = Ship("Some ship")
    assert ship.name == "Some ship"
    assert ship._hit_points == Ship.MAX_HIT_POINTS


def test_ship_generate_prepare_time():
    prepare_time = Ship.generate_prepare_time()
    assert prepare_time >= Ship.MIN_PREPARE_TIME and prepare_time <= Ship.MAX_PREPARE_TIME


def test_ship_fire_at():
    ship1 = Ship("Ship 1")
    ship2 = Ship("Ship 2")
    ship1.fire_at(ship2)
    ship1._hit_points == Ship.MAX_HIT_POINTS
    ship2._hit_points == Ship.MAX_HIT_POINTS - Ship.FIRE_DAMAGE
    ship1.fire_at(ship2)
    ship1._hit_points == Ship.MAX_HIT_POINTS
    ship2._hit_points == Ship.MAX_HIT_POINTS - Ship.FIRE_DAMAGE * 2


def test_ship_is_destroyed():
    ship = Ship("Ship")
    ship._hit_points = 0
    assert ship.is_destroyed()


def test_ship_take_damage():
    ship = Ship("Ship")
    ship._take_damage(2)
    assert ship._hit_points == 0
    with pytest.raises(Exception):
        ship._take_damage(1)


# --------------------------------------- Game Tests ---------------------------------------


def init_new_game() -> Game:
    game = Game(ship_count=SHIP_COUNT)
    return game


def test_game_init():
    game = init_new_game()
    assert game._ship_counts() == SHIP_COUNT
    assert all([ship is None for ship in game._ships])


def test_game_start():
    game = init_new_game().start()
    assert game._ship_counts() == SHIP_COUNT
    for ship in game._ships:
        assert type(ship) is Ship


def test_game_battle_end():
    game = init_new_game()
    game.start().battle().end()
    assert game._has_winner() or game._ship_counts() == 0


def test_game_get_random_ship():
    game = init_new_game().start()
    random_ship = game._get_random_ship(excluded_ship=game._ships[0])
    assert any(ship == random_ship for ship in game._ships)
    game.battle().end()
    with pytest.raises(Exception):
        game._get_random_ship()


def test_game_command_ships_to_begin():
    game = init_new_game().start()
    threads = game._command_ships_to_begin()
    assert len(threads) == game._ship_counts()


def test_game_spawn_ships():
    game = init_new_game()
    game._spawn_ships()
    assert all([type(ship) is Ship for ship in game._ships])


def test_game_command_fire():
    game = init_new_game().start()
    game._command_fire(game._ships[0])
    assert any(ship._hit_points == 1 for ship in game._ships)


def test_game_run_logic():
    game = init_new_game().start()
    game._run_logic(game._ships[0])
    assert game._get_winner() == game._ships[0]


def test_game_ship_counts():
    game = init_new_game()
    assert game._ship_counts() == SHIP_COUNT


def test_game_has_winner():
    game = init_new_game().start()
    assert game._has_winner() == False
    game.battle().end()
    assert game._has_winner() or game._ship_counts == 0
