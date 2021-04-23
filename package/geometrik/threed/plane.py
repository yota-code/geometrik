#!/usr/bin/env python3

import math

class Plane() :
	# define a plane
	def __init__(self, director, point=None) :
		self.director = director
		self.point = point 

	@staticmethod
	def from_three_points(self, o, a, b) :
		v1 = a - o
		v2 = b - o
		v0 = v1 @ v2
		return Plane(v0, o)

	def distance_to_point(self, point) :
		u = point - self.point
		n = self.director

		return (n * u) / n.norm

	def is_on_plane(self, point) :
		""" return True if the point lies on the plane """
		u = point - self.point
		n = self.director

		return math.isclose(n * u, 0.0)

	def project(self, vector) :
		return vector - ( vector * self.director * self.director )