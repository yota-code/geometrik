#!/usr/bin/env python3

import math

import sympy

import geometrik.threed as g3d

class Plane() :

	# define a plane which pass through the point (0, 0), defined by its normal vector
	def __init__(self, normal: g3d.Vector) :
		self.normal = normal.normalized()

	def distance(self, point: g3d.Vector) :
		return (self.normal * point) / self.normal.norm

	def is_on_plane(self, point) :
		""" return True if the point lies on the plane """
		return math.isclose( self.distance(point), 0.0 )


	def frame(self, other=g3d.Vector(0.0, 0.0, 1.0, True)) :
		""" return a frame where z is oriented toward other (by default north):

			* no solution is returned if self and other are colinears
			* if other is not specified, v_north is used as other
			* in this case, the frame is not defined at poles
		"""

		if other is None :
			""" return an arbitrarily oriented frame optimized to reduce numerical errors,
			the frame can be defined everywhere """
			c_tpl = self.normal.as_tuple
			c_max = max(range(len(c_tpl)), key=lambda i: c_tpl[i])

			c_lst = list(c_tpl)
			c_lst[c_max] = 0

			num = sum(c_lst)
			den = c_tpl[c_max]

			y_lst = [1.0, 1.0, 1.0]
			y_lst[c_max] = - num / den

			x = self.normal
			y = g3d.Vector(* y_lst).normalized()
			z = x @ y

		else :
			x = self.normal
			y = (other @ x).normalized()
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
