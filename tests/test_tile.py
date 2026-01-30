import pytest

from metamaterial_absorber.tiles import Tile


def test_tile_translate_and_goto():
    tile = Tile("sides", "ver", [0, 0, 0])
    tile.translate([1, 2, 3])
    assert tile.coord == [1.0, 2.0, 3.0]

    tile.goto([4, 5, 6])
    assert tile.coord == [4.0, 5.0, 6.0]


def test_tile_coord_validation():
    with pytest.raises(ValueError):
        Tile("sides", "ver", [0, 0])
