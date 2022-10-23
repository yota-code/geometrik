#!/usr/bin/env python3

from geometrik.threed.vector import Vector, VectorPlot
from geometrik.threed.plane import Plane

v_null = Vector(0.0, 0.0, 0.0, True)
v_north = Vector(0.0, 0.0, 1.0, True)
v_east = Vector(0.0, 1.0, 0.0, True)
v_down = v_north @ v_east
v_up = v_east @ v_north
