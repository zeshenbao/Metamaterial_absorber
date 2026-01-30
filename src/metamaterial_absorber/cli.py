"""Command-line interface for building absorbers."""

from __future__ import annotations

import argparse
import sys

from .core import Absorber, Wall
from .patterns import Pattern


def _build_pattern(args: argparse.Namespace) -> Pattern:
    pattern = Pattern()
    if args.pattern == "hilbert":
        pattern.create_hilbert_blueprint(iterations=args.iterations, scale=args.scale)
    elif args.pattern == "ver_rows":
        pattern.create_ver_rows_blueprint(
            pattern_len=args.pattern_len, pattern_wid=args.pattern_wid, scale=args.scale
        )
    elif args.pattern == "dots":
        pattern.create_dots_blueprint(
            pattern_len=args.pattern_len, pattern_wid=args.pattern_wid, scale=args.scale
        )
    else:
        raise ValueError(f"Unknown pattern '{args.pattern}'")
    return pattern


def _build_wall(args: argparse.Namespace) -> Wall:
    return Wall(
        cross_section=args.cross_section,
        tile_len=args.tile_len,
        tile_wid=args.tile_wid,
        tile_height=args.tile_height,
        foundation_thickness=args.foundation_thickness,
        scale=args.scale,
        export=args.export_wall_parts,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a metamaterial absorber STL.")
    parser.add_argument(
        "--pattern",
        choices=["ver_rows", "dots", "hilbert"],
        default="ver_rows",
        help="Pattern blueprint to generate.",
    )
    parser.add_argument("--pattern-len", type=float, default=5.0, help="Pattern length.")
    parser.add_argument("--pattern-wid", type=float, default=5.0, help="Pattern width.")
    parser.add_argument("--iterations", type=int, default=2, help="Hilbert iterations.")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale applied to tiles.")

    parser.add_argument(
        "--cross-section",
        choices=["dogleg", "triangle", "block"],
        default="dogleg",
        help="Wall cross-section to use.",
    )
    parser.add_argument("--tile-len", type=float, default=1.0)
    parser.add_argument("--tile-wid", type=float, default=1.0)
    parser.add_argument("--tile-height", type=float, default=2.0)
    parser.add_argument("--foundation-thickness", type=float, default=4.0)
    parser.add_argument(
        "--export-wall-parts",
        action="store_true",
        help="Export individual wall parts in addition to the absorber.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output STL filename. Defaults to an auto-generated name.",
    )

    args = parser.parse_args(argv)

    pattern = _build_pattern(args)
    wall = _build_wall(args)
    absorber = Absorber(wall, pattern)
    absorber.build()
    filename = absorber.export(args.output)
    print(f"Exported {filename}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
