#!/usr/bin/env python3

import math

import sympy

import geometrik.threed as g3d

class Plane() :
	# define a plane
	def __init__(self, normal: g3d.vector.Vector, point=None) :
		self.normal = normal.normalized()

	def distance(self, point) :
		u = point - self.point
		n = self.normal

		return (n * u) / n.norm

	def is_on_plane(self, point) :
		""" return True if the point lies on the plane """
		return math.isclose( self.distance(point), 0.0 )

	def project(self, vector) :
		return vector - ( vector * self.normal * self.normal )

	def frame(self, other=None) :
		""" return a frame where z is oriented toward other:

			* no solution is returned if self and other are colinears
			* if other is not specified, v_north is used as other
			* in this case, the frame is not defined at poles
		
		"""
		if other is None :
			other = g3d.vector.v_north

		x = self.normal
		y = ( g3d.vector.v_north @ x ).normalized()
		z = x @ y

		return y, z

	def frame_optimal(self) :
		""" return an arbitrary frame optimized for numerical errors, the frame can be defined everywhere """

		c_tpl = self.normal.as_tuple
		c_max = max(range(len(c_tpl)), key=lambda i: c_tpl[i])

		c_lst = list(c_tpl)
		c_lst[c_max] = 0

		num = sum(c_lst)
		den = c_tpl[c_max]

		y_lst = [1.0, 1.0, 1.0]
		y_lst[c_max] = - num / den

		x = self.normal
		y = g3d.vector.Vector(* y_lst).normalized()
		z = x @ y
		return y, z


# class GenericPlane() :
# 	def __init__(self, normal, point=None) :
# 		self.normal = normal
# 		self.point = point 

# 	@staticmethod
# 	def from_three_points(self, c, a, b) :
# 		v1 = a - c
# 		v2 = b - c
# 		return GenericPlane(v1 @ v2, c)
