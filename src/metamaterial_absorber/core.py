"""Core geometry builders for metamaterial absorbers."""

from __future__ import annotations

import logging
from math import cos, pi, sin, tan
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .patterns import Pattern

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    import cadquery as cq
    from cadquery import exporters
except Exception as exc:  # pragma: no cover - optional dependency
    cq = None
    exporters = None
    _CADQUERY_IMPORT_ERROR = exc
else:  # pragma: no cover - optional dependency
    _CADQUERY_IMPORT_ERROR = None


def _require_cadquery() -> None:
    if cq is None or exporters is None:
        raise ImportError(
            "cadquery is required for geometry generation. "
            "Install with 'pip install metamaterial-absorber[cadquery]' "
            "or use the conda-based instructions in the README."
        ) from _CADQUERY_IMPORT_ERROR


class Absorber:
    """Combine a wall definition and a pattern blueprint."""

    def __init__(self, wall: "Wall", pattern: "Pattern") -> None:
        _require_cadquery()
        self.pattern = pattern
        self.wall = wall
        self.result = cq.Workplane("XY")

    def build(self) -> None:
        """Build the absorber by placing tiles from the blueprint."""

        for part in self.pattern.blueprint:
            if part.group == "sides":
                self.result = self.result.add(self.wall.sides[part.tile].translate(part.as_tuple()))
            elif part.group == "corners":
                self.result = self.result.add(self.wall.corners[part.tile].translate(part.as_tuple()))
            elif part.group == "other":
                self.result = self.result.add(self.wall.other[part.tile].translate(part.as_tuple()))
            else:
                raise ValueError(f"Unknown tile group: {part.group}")

    def export(self, filename: str | None = None) -> str:
        """Export the built absorber as an STL file."""

        _require_cadquery()
        if filename is None:
            suffix = f"_iter{self.pattern.iterations}" if self.pattern.iterations is not None else ""
            filename = f"{self.wall.cs_choice}_{self.pattern.name}{suffix}.stl"
        exporters.export(self.result, filename)
        logger.info("Exported absorber to %s", filename)
        return filename


class Wall:
    """Build wall segments and cross-sections for absorbers."""

    def __init__(
        self,
        cross_section: str = "dogleg",
        tile_len: float = 1.0,
        tile_wid: float = 1.0,
        tile_height: float = 2.0,
        foundation_thickness: float = 4.0,
        scale: float = 1.0,
        export: bool = True,
    ) -> None:
        _require_cadquery()

        self.scale = scale
        self.tile_len = tile_len * self.scale
        self.tile_wid = tile_wid * self.scale
        self.tile_height = tile_height * self.scale
        self.foundation_thickness = foundation_thickness * self.scale

        self.cs_choice = cross_section
        self.cross_section = None
        self.export = export

        self.comps: Dict[str, "cq.Workplane"] | None = None
        self.sides: Dict[str, "cq.Workplane"] | None = None
        self.corners: Dict[str, "cq.Workplane"] | None = None
        self.other: Dict[str, "cq.Workplane"] | None = None

        self.max_wid = 0.0

        self.set_cross_section()
        self.make_wall_components()

    def set_cross_section(self, choice: str | None = None) -> None:
        """Set or reselect the cross section."""

        if choice is None:
            choice = self.cs_choice

        cross_sections = {
            "dogleg": self._make_dogleg_basic,
            "triangle": self._make_triangle_basic,
            "block": self._make_block_basic,
        }

        try:
            builder = cross_sections[str(choice)]
        except KeyError as exc:
            valid = ", ".join(sorted(cross_sections))
            raise ValueError(f"Unknown cross section '{choice}'. Valid: {valid}") from exc

        self.cross_section = builder()

    def export_parts(self) -> None:
        """Export generated wall tiles as STL files."""

        if not self.comps or not self.sides or not self.corners:
            raise RuntimeError("Wall components are not generated")

        bundle = {"comps": self.comps, "sides": self.sides, "corners": self.corners}
        for item in bundle:
            for key in bundle[item]:
                exporters.export(bundle[item][key], f"{item[:-1]}_{key}.stl")

    def _make_block_basic(self):
        self.max_wid = self.tile_wid

        geo_xz = (
            cq.Workplane("XZ")
            .rect(self.tile_wid / 2, self.tile_height)
            .extrude(self.max_wid / 2)
            .mirror(mirrorPlane="XZ", union=True)
        )

        geo_xy = cq.Workplane("XY").union(geo_xz)

        block_side = (
            geo_xy.faces("<Z")
            .rect(self.tile_len, self.tile_wid)
            .extrude(-self.foundation_thickness)
        )

        return block_side

    def _make_triangle_basic(self):
        pts = [
            (-self.tile_len / 2, 0),
            (self.tile_len / 2, 0),
            (0, self.tile_height),
        ]

        self.max_wid = self.tile_wid

        geo_xz = (
            cq.Workplane("XZ")
            .polyline(pts)
            .close()
            .extrude(self.tile_wid / 2)
            .mirror(mirrorPlane="XZ", union=True)
        )

        geo_xy = cq.Workplane("XY").union(geo_xz)

        tria_side = (
            geo_xy.faces("<Z")
            .rect(self.tile_len, self.tile_wid)
            .extrude(-self.foundation_thickness)
        )

        return tria_side

    def _make_dogleg_basic(self):
        foundation_thickness = self.foundation_thickness
        tile_len = self.tile_len
        tile_height = self.tile_height
        angle = (pi / 6) / 2

        h = tile_height / 2
        w = h * tan(angle)

        k = 1 / tan(2 * angle)
        k_w = 1 / (1 - tan(angle) ** 2)
        a = tile_len - 2 * w
        s = a * cos(2 * angle)

        dx = s * cos(2 * angle)
        dy = s * sin(2 * angle)

        xs_1 = (s + dy) / (2 * k)
        xs_2 = (s + dy) / (2 * k) + dx
        ys_1 = (s + dy) / 2
        ys_2 = (s - dy) / 2

        xs = (xs_1 + xs_2) / 2
        ys = (ys_1 + ys_2) / 2

        xa = xs
        c1 = xa
        c2 = a - c1

        area_left_pts = [
            (0, 0),
            (xa, 0),
            (xs, ys),
            (xs_1, ys_1),
        ]

        area_right_pts = [
            (xa, 0),
            (a, 0),
            (xs_2, ys_2),
            (xs, ys),
        ]

        pts = [
            (0, 0),
            (1.5 * w, -1.5 * h),
            ((1.5 - k_w) * w, -2 * h),
            ((-0.5 - k_w) * w, -2 * h),
            (-0.5 * w, -1.5 * h),
            (-w, -h),
        ]

        max_wid = 2 * (abs((-0.5 - k_w) * w - c2))
        self.max_wid = max_wid

        geo_xz = (
            cq.Workplane("XZ")
            .center(0, 0)
            .polyline(pts)
            .close()
            .extrude(max_wid / 2)
            .mirror(mirrorPlane="XZ", union=True)
        )

        geo_xy = cq.Workplane("XY").union(geo_xz).translate((0, 0, tile_height))

        dog_side = geo_xy.union(
            cq.Workplane("XY")
            .center(0, 0)
            .rect(max_wid, max_wid)
            .extrude(-foundation_thickness)
        )

        area_right_side = (
            cq.Workplane("XZ")
            .center((1.5 - k_w) * w, 0)
            .polyline(area_left_pts)
            .close()
            .extrude(max_wid / 2)
            .mirror(mirrorPlane="XZ", union=True)
        )

        area_left_side = (
            cq.Workplane("XZ")
            .center((-0.5 - k_w) * w - a, 0)
            .polyline(area_right_pts)
            .close()
            .extrude(max_wid / 2)
            .mirror(mirrorPlane="XZ", union=True)
        )

        circle_right_side = (
            cq.Workplane("XZ")
            .center((1.5 - k_w) * w + c1, s / 2)
            .circle(s / 2)
            .extrude(max_wid / 2)
            .mirror(mirrorPlane="XZ", union=True)
        )

        circle_left_side = (
            cq.Workplane("XZ")
            .center((-0.5 - k_w) * w - c2, s / 2)
            .circle(s / 2)
            .extrude(max_wid / 2)
            .mirror(mirrorPlane="XZ", union=True)
        )

        dog_side = dog_side.union(area_left_side).union(area_right_side)
        dog_side = dog_side.cut(circle_right_side).cut(circle_left_side)

        return dog_side

    def make_wall_components(self) -> None:
        """Generate wall parts and corners."""

        self._make_components()
        self._make_sides()
        self._make_corners()

        if self.export:
            self.export_parts()

    def _make_components(self) -> None:
        comps = {}
        comps["ver"] = self.cross_section
        comps["hor"] = comps["ver"].rotate((0, 0, 0), (0, 0, 1), 90)
        comps["inter"] = comps["ver"].intersect(comps["hor"])
        comps["union"] = comps["ver"].union(comps["hor"])

        self.comps = comps
        self.other = {"inter": comps["inter"], "union": comps["union"]}

    def _make_sides(self) -> None:
        sides = {
            "ver": self.comps["ver"],
            "hor": self.comps["hor"],
            "ver_half_down": None,
            "ver_half_up": None,
            "hor_half_left": None,
            "hor_half_right": None,
        }

        for key in list(sides):
            if key in {"ver", "hor"}:
                continue

            if key.startswith("hor"):
                comp_key, face_key = "hor", ">X"
            elif key.startswith("ver"):
                comp_key, face_key = "ver", ">Y"
            else:
                raise ValueError(f"Invalid side key: {key}")

            if key.endswith("left") or key.endswith("down"):
                sides[key] = (
                    self.comps[comp_key].faces(face_key).workplane(-self.max_wid / 2).split(
                        keepBottom=True
                    )
                )
            elif key.endswith("right") or key.endswith("up"):
                sides[key] = (
                    self.comps[comp_key].faces(face_key).workplane(-self.max_wid / 2).split(
                        keepTop=True
                    )
                )
            else:
                raise ValueError(f"Invalid side key: {key}")

        self.sides = sides

    def _make_corners(self) -> None:
        corners = {"left_down": None, "left_up": None, "right_down": None, "right_up": None}
        for key in corners:
            parts = key.split("_")
            corners[key] = (
                self.comps["inter"]
                .union(self.sides[f"hor_half_{parts[0]}"])
                .union(self.sides[f"ver_half_{parts[1]}"])
            )
        self.corners = corners
