#!/usr/bin/env python3

import math
import sympy

import IPython.display


class Point() :
	""" a Point is also a vector initiating at the origin """
	def __init__(self, x, y, z) :
		self.x = x
		self.y = y
		self.z = z

	@property
	def as_tuple(self) :
		return self.x, self.y, self.z

	@staticmethod
	def origin() :
		return Point(0.0, 0.0, 0.0)

	def __repr__(self) :
		try :
			return f"Point({self.x:0.3g}, {self.y:0.3g}, {self.z:0.3g})"
		except TypeError :
			s = f"Point({sympy.latex(self.x)}, {sympy.latex(self.y)}, {sympy.latex(self.z)})"
			return s

	def __sub__(self, other) :
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

	def subs(self, ** nam) :
		return Point(self.x.subs(nam), self.y.subs(nam), self.z.subs(nam))

class Vector(Point) :
	def __init__(self, x, y, z, is_unit=False) :
		self.x = x
		self.y = y
		self.z = z

		self._is_unit = is_unit

	def __iter__(self) :
		return (i for i in (self.x, self.y, self.z))
				
	def __add__(self, other) :
		if isinstance(other, Point) :
			return Vector(
				self.x + other.x,
				self.y + other.y,
				self.z + other.z
			)
			
	def __mul__(self, other) :
		if isinstance(other, Vector) :
			return self.scalar_product(other)
		#elif isinstance(other, (int, float, sympy.core.symbol.Symbol,)) :
		#	return self.lambda_product(other)
		else :
			return self.lambda_product(other)
		#	raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
	__rmul__ = __mul__
	
	def __truediv__(self, other) :
		# print("__truediv__({0}, {1})".format(type(self), type(other)))
		if isinstance(other, (int, float,)) :
			return Vector(self.x / other, self.y / other, self.z / other)
		else :
			raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
	def __rtruediv__(self, other) :
		# print("__rtruediv__({0}, {1})".format(type(self), type(other)))
		if isinstance(other, (int, float,)) :
			return self.__truediv__(other)
			
	def __matmul__(self, other) :
		if isinstance(other, Vector) :
			return self.vector_product(other)
		else :
			raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
	def lambda_product(self, other) :
		""" constant * vector product """
		return Vector(other * self.x, other * self.y, other * self.z)
				
	def scalar_product(self, other) :
		""" scalar product """
		return self.x * other.x + self.y * other.y + self.z * other.z
		
	def vector_product(self, other) :
		""" vectoriel product """
		return Vector(
			self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x,
		)
		
	def __str__(self) :
		return "[" + ', '.join(str(i) for i in self.as_tuple) + "]"
		
	@property
	def norm(self) :
		try :
			return math.sqrt(self.norm_2)
		except TypeError :
			return sympy.sqrt(self.norm_2)

	@property
	def norm_2(self) :
		return self.scalar_product(self)
		
	def normalized(self) :
		if self._is_unit :
			return self
		else :
			n = self.norm
			return Vector(self.x / n, self.y / n, self.z / n, True)

	def angle_to(self, other) :
		c = (self * other) / (
			(1 if self._is_unit else self.norm) *
			(1 if self._is_unit else other.norm)
		)
		try :
			return math.acos(c)
		except TypeError :
			return sympy.acos(c)

	def signed_angle_to(self, other, sign) :
		c = (self * other) / (self.norm * other.norm)
		s = (self @ other) * sign
		return math.copysign( math.acos(c), s )

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

if __name__ == '__main__' :
	a = Vector(1.0, 0.0, 0.0)
	b = Vector(1.0, 1.0, 0.0)
	print(a + b)
	print(a * b)
	print(b * a)
	print(a @ b)
	print(b @ a)
	print(3.0 * b)
	print(b * 3.0)
	print(b.normalize())

	