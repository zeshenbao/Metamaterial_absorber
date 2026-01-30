"""Example: generate a dot pattern absorber and export to STL."""

from metamaterial_absorber import Absorber, Pattern, Wall


def main() -> None:
    wall = Wall(cross_section="triangle", foundation_thickness=1.0, export=False)
    pattern = Pattern()
    pattern.create_dots_blueprint(pattern_len=5, pattern_wid=5, scale=1.0)

    absorber = Absorber(wall, pattern)
    absorber.build()
    absorber.export("triangle_dots.stl")


if __name__ == "__main__":
    main()
