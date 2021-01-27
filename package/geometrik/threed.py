#!/usr/bin/env python3

import math

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
	def origin(self) :
		return Point(0.0, 0.0, 0.0)

	def __repr__(self) :
		return f"Point({self.x:0.3g}, {self.y:0.3g}, {self.z:0.3g})"

	def __sub__(self, other) :
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

class Vector(Point) :
	def __init__(self, x, y, z, is_unit=False) :
		self.x = x
		self.y = y
		self.z = z

		self._is_unit = is_unit
				
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
		elif isinstance(other, (int, float,)) :
			return self.lambda_product(other)
		else :
			raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
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
			self.x * other.y - self.y * other.x
		)
		
	def __str__(self) :
		return "[" + ', '.join(str(i) for i in self.as_tuple) + "]"
		
	@property
	def norm(self) :
		return math.sqrt(self.norm_2)

	@property
	def norm_2(self) :
		return self.scalar_product(self)
		
	def normalized(self) :
		n = self.norm
		return Vector(self.x / n, self.y / n, self.z / n, True)

	def angle_to(self, other) :
		c = (self * other) / (self.norm * other.norm)
		return math.acos(c)

	def signed_angle_to(self, other, sign) :
		c = (self * other) / (self.norm * other.norm)
		s = (self @ other) * sign
		return math.copysign( math.acos(c), s )

class Plane() :
	def __init__(self, director, point) :
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

	def is_point_on_plane(self, point) :
		""" return True if the point lies on the plane """
		u = point - self.point
		n = self.director

		return math.isclose(n * u, 0.0)




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

	