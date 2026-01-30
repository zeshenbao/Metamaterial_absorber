"""Tile primitives for absorber patterns."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


Coord = List[float]


def _to_coord(values: Iterable[float]) -> Coord:
    coord = [float(v) for v in values]
    if len(coord) != 3:
        raise ValueError(f"Expected 3 coordinates, got {len(coord)}")
    return coord


@dataclass
class Tile:
    """Represents a single wall tile and its location."""

    group: str
    tile: str
    coord: Coord

    def __post_init__(self) -> None:
        self.coord = _to_coord(self.coord)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"{self.group}_{self.tile}"

    def goto(self, coord: Iterable[float]) -> None:
        """Move this tile to an absolute coordinate."""

        self.coord = _to_coord(coord)

    def translate(self, delta: Iterable[float]) -> None:
        """Translate this tile in place by the given delta."""

        d = _to_coord(delta)
        for idx in range(3):
            self.coord[idx] += d[idx]

    def as_tuple(self) -> tuple[float, float, float]:
        """Return the coordinate as an immutable tuple."""

        return (self.coord[0], self.coord[1], self.coord[2])
