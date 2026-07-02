"""
geometry.py
Python geometry engine — all measurements in pixels.
Shapes are stored in a session registry so the agent can reference them by ID.
"""

import math
from typing import Dict, Any


_registry: Dict[str, Any] = {}   # shape_id -> shape object
_counters: Dict[str, int] = {}   # "circle" -> 1, 2, ...


def _next_id(shape_type: str) -> str:
    _counters[shape_type] = _counters.get(shape_type, 0) + 1
    return f"{shape_type}_{_counters[shape_type]}"


# ── Shape classes ────────────────────────────────────────────────────────────

class Square:
    def __init__(self, side: float):
        if side <= 0:
            raise ValueError(f"side_length must be > 0px. Got: {side}px.")
        self.side = side

    def resize(self, amount: float):
        new = self.side + amount
        if new <= 0:
            raise ValueError(f"Resulting side ({new}px) must be > 0.")
        self.side = new

    @property
    def area(self): return self.side ** 2
    @property
    def perimeter(self): return 4 * self.side
    @property
    def diagonal(self): return self.side * math.sqrt(2)

    def describe(self, sid):
        return (f"[{sid}] Square | side={self.side:.1f}px | "
                f"area={self.area:.1f}px² | perimeter={self.perimeter:.1f}px | "
                f"diagonal={self.diagonal:.1f}px")


class Circle:
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError(f"radius must be > 0px. Got: {radius}px.")
        self.radius = radius

    def resize(self, amount: float):
        new = self.radius + amount
        if new <= 0:
            raise ValueError(f"Resulting radius ({new}px) must be > 0.")
        self.radius = new

    @property
    def area(self): return math.pi * self.radius ** 2
    @property
    def circumference(self): return 2 * math.pi * self.radius
    @property
    def diameter(self): return 2 * self.radius

    def describe(self, sid):
        return (f"[{sid}] Circle | radius={self.radius:.1f}px | "
                f"diameter={self.diameter:.1f}px | area={self.area:.1f}px² | "
                f"circumference={self.circumference:.1f}px")


class Rectangle:
    def __init__(self, width: float, height: float):
        if width <= 0:
            raise ValueError(f"width must be > 0px. Got: {width}px.")
        if height <= 0:
            raise ValueError(f"height must be > 0px. Got: {height}px.")
        self.width = width
        self.height = height

    def resize(self, amount: float):
        """Scale both dimensions by adding amount (positive=bigger, negative=smaller)."""
        factor = (self.width + amount) / self.width
        new_w, new_h = self.width * factor, self.height * factor
        if new_w <= 0 or new_h <= 0:
            raise ValueError("Resize would result in zero or negative dimensions.")
        self.width, self.height = new_w, new_h

    @property
    def area(self): return self.width * self.height
    @property
    def perimeter(self): return 2 * (self.width + self.height)
    @property
    def diagonal(self): return math.sqrt(self.width ** 2 + self.height ** 2)

    def describe(self, sid):
        return (f"[{sid}] Rectangle | width={self.width:.1f}px height={self.height:.1f}px | "
                f"area={self.area:.1f}px² | perimeter={self.perimeter:.1f}px | "
                f"diagonal={self.diagonal:.1f}px")


# ── Registry helpers ─────────────────────────────────────────────────────────

def create_shape(shape_type: str, **kwargs) -> str:
    shape_type = shape_type.lower()
    if shape_type == "circle":
        shape = Circle(kwargs["radius"])
    elif shape_type == "square":
        shape = Square(kwargs["side"])
    elif shape_type == "rectangle":
        shape = Rectangle(kwargs["width"], kwargs["height"])
    else:
        raise ValueError(f"Unknown shape '{shape_type}'. Choose: circle, square, rectangle.")
    sid = _next_id(shape_type)
    _registry[sid] = shape
    return f"Created: {shape.describe(sid)}"


def resize_shape(shape_id: str, amount: float) -> str:
    shape = _get(shape_id)
    shape.resize(amount)
    return f"Resized: {shape.describe(shape_id)}"


def erase_shape(shape_id: str) -> str:
    _get(shape_id)
    del _registry[shape_id]
    return f"Shape '{shape_id}' erased."


def list_shapes() -> str:
    if not _registry:
        return "No shapes on the canvas."
    return "\n".join(s.describe(sid) for sid, s in _registry.items())


def _get(shape_id: str):
    if shape_id not in _registry:
        ids = list(_registry.keys())
        raise ValueError(f"Shape '{shape_id}' not found. Existing shapes: {ids}")
    return _registry[shape_id]
