#!/usr/bin/env python3

import math

class Vector3d() :
	def __init__(self, x, y, z, is_unit=False) :
		self.x = x
		self.y = y
		self.z = z
		self._is_unit = is_unit
		
	@property
	def values(self) :
		return self.x, self.y, self.z
		
	def __add__(self, other) :
		if isinstance(other, Vector3d) :
			return Vector3d(
				self.x + other.x,
				self.y + other.y,
				self.z + other.z
			)
			
	def __mul__(self, other) :
		if isinstance(other, Vector3d) :
			return self.s_product(other)
		elif isinstance(other, (int, float,)) :
			return self.k_product(other)
		else :
			raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
	__rmul__ = __mul__
	
	def __truediv__(self, other) :
		# print("__truediv__({0}, {1})".format(type(self), type(other)))
		if isinstance(other, (int, float,)) :
			return Vector3d(self.x / other, self.y / other, self.z / other)
		else :
			raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
	def __rtruediv__(self, other) :
		# print("__rtruediv__({0}, {1})".format(type(self), type(other)))
		if isinstance(other, (int, float,)) :
			return self.__truediv__(other)
			
	def __matmul__(self, other) :
		if isinstance(other, Vector3d) :
			return self.v_product(other)
		else :
			raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
	def k_product(self, other) :
		""" constant * vector product """
		return Vector3d(other * self.x, other * self.y, other * self.z)
		
	_norm_2 = k_product
		
	def s_product(self, other) :
		""" scalar product """
		return self.x * other.x + self.y * other.y + self.z * other.z
		
	def v_product(self, other) :
		""" vectoriel product """
		return Vector3d(
			self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x
		)
		
	def __str__(self) :
		return "[" + ', '.join(str(i) for i in self.values) + "]"
		
	@property
	def norm(self) :
		return math.sqrt(self._norm_2())
		
	def normalize(self) :
		q = self / self.norm
		q._is_unit = True
		return q

if __name__ == '__main__' :
	a = Vector3d(1.0, 0.0, 0.0)
	b = Vector3d(1.0, 1.0, 0.0)
	print(a + b)
	print(a * b)
	print(b * a)
	print(a @ b)
	print(b @ a)
	print(3.0 * b)
	print(b * 3.0)
	print(b.normalize())

	