"""Pattern generators for metamaterial absorbers."""

from __future__ import annotations

from .tiles import Tile


class Pattern:
    """Create blueprints describing how to place tiles."""

    def __init__(self) -> None:
        self.blueprint: list[Tile] = []
        self.iterations: int | None = None
        self.name: str | None = None
        self.scale: float = 1.0

    @staticmethod
    def _gen_hilbert_system(iterations: int) -> str:
        if iterations < 0:
            raise ValueError("iterations must be >= 0")

        axiom = "A"
        rule_a = "+BF-AFA-FB+"
        rule_b = "-AF+BFB+FA-"

        system = axiom
        for _ in range(iterations):
            system = system.replace("A", "a").replace("B", "b")
            system = system.replace("a", rule_a).replace("b", rule_b)

        system = system.replace("A", "").replace("B", "")

        while "+-" in system:
            system = system.replace("+-", "")

        while "-+" in system:
            system = system.replace("-+", "")

        system = system.replace("F+", "+").replace("F-", "-")
        return system

    def _reset(self) -> None:
        self.blueprint = []

    def create_hilbert_blueprint(self, iterations: int = 2, scale: float = 1.0) -> None:
        """Generate tiles for a Hilbert curve pattern."""

        self._reset()
        self.name = "hilbert"
        self.iterations = iterations
        self.scale = scale

        system = self._gen_hilbert_system(iterations)

        position = [0.0, 0.0, 0.0]
        angle = 0  # 0 degrees == right

        if iterations % 2 == 0:
            self.blueprint.append(Tile("sides", "hor", [-1 * scale, 0, 0]))

        for letter in system:
            if letter == "F":
                if angle == 0:
                    self.blueprint.append(Tile("sides", "hor", position))
                    position[0] += 1 * scale
                elif angle == 180:
                    self.blueprint.append(Tile("sides", "hor", position))
                    position[0] -= 1 * scale
                elif angle == 90:
                    self.blueprint.append(Tile("sides", "ver", position))
                    position[1] -= 1 * scale
                elif angle == 270:
                    self.blueprint.append(Tile("sides", "ver", position))
                    position[1] += 1 * scale
                else:
                    raise ValueError("Invalid angle in Hilbert system")
            elif letter == "+":
                if angle == 0:
                    self.blueprint.append(Tile("corners", "left_down", position))
                    position[1] -= 1 * scale
                elif angle == 180:
                    self.blueprint.append(Tile("corners", "right_up", position))
                    position[1] += 1 * scale
                elif angle == 90:
                    self.blueprint.append(Tile("corners", "left_up", position))
                    position[0] -= 1 * scale
                elif angle == 270:
                    self.blueprint.append(Tile("corners", "right_down", position))
                    position[0] += 1 * scale
                else:
                    raise ValueError("Invalid angle in Hilbert system")

                angle = (angle + 90) % 360
            elif letter == "-":
                if angle == 0:
                    self.blueprint.append(Tile("corners", "left_up", position))
                    position[1] += 1 * scale
                elif angle == 180:
                    self.blueprint.append(Tile("corners", "right_down", position))
                    position[1] -= 1 * scale
                elif angle == 90:
                    self.blueprint.append(Tile("corners", "right_up", position))
                    position[0] += 1 * scale
                elif angle == 270:
                    self.blueprint.append(Tile("corners", "left_down", position))
                    position[0] -= 1 * scale
                else:
                    raise ValueError("Invalid angle in Hilbert system")

                angle = (angle - 90) % 360

    def create_ver_rows_blueprint(
        self, pattern_len: float = 5.0, pattern_wid: float = 5.0, scale: float = 1.0
    ) -> None:
        """Generate vertical rows of tiles."""

        self._reset()
        self.name = "ver_rows"
        self.iterations = None
        self.scale = scale

        for i in range(int(pattern_len)):
            for j in range(int(pattern_wid)):
                self.blueprint.append(Tile("sides", "ver", [i * scale, j * scale, 0]))

    def create_dots_blueprint(
        self, pattern_len: float = 10.0, pattern_wid: float = 10.0, scale: float = 1.0
    ) -> None:
        """Generate a dot grid using intersection tiles."""

        self._reset()
        self.name = "dots"
        self.iterations = None
        self.scale = scale

        for i in range(int(pattern_len)):
            for j in range(int(pattern_wid)):
                self.blueprint.append(Tile("other", "inter", [i * scale, j * scale, 0]))

    def create_new_blueprint(self) -> None:
        """Placeholder for new pattern generators."""

        raise NotImplementedError("Define a new pattern generator in create_new_blueprint().")
