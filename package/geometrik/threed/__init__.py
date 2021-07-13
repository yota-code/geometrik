#!/usr/bin/env python3

from geometrik.threed.vector import Vector
from geometrik.threed.plane import Plane

v_null = Vector(0.0, 0.0, 0.0)
v_north = Vector(0.0, 0.0, 1.0)
v_east = Vector(0.0, 1.0, 0.0)
v_down = v_north @ v_east
v_up = v_east @ v_north
