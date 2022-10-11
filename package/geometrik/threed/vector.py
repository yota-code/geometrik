#!/usr/bin/env python3

import math
import sympy

class Vector() :

	def __init__(self, x, y, z, is_unit=False) :
		self.x = x
		self.y = y
		self.z = z

		self._is_unit = is_unit

	@property
	def as_tuple(self) :
		return self.x, self.y, self.z

	@staticmethod
	def symbolic(name) :
		Vx, Vy, Vz = sympy.symbols(' '.join(f'{name}_{i}' for i in 'xyz'))
		return Vector(Vx, Vy, Vz)

	def __repr__(self) :
		try :
			return f"{self.__class__.__name__}({self.x:0.3g}, {self.y:0.3g}, {self.z:0.3g})"
		except TypeError :
			s = f"{self.__class__.__name__}({sympy.latex(self.x)}, {sympy.latex(self.y)}, {sympy.latex(self.z)})"
			return s

	def subs(self, v_map) :
		v_lst = self.x, self.y, self.z
		m_lst = list()
		for v in v_lst :
			try :
				v = float(v.subs(v_map))
			except :
				pass
			m_lst.append(v)
		return Vector(* m_lst)

	def __iter__(self) :
		return (i for i in (self.x, self.y, self.z))

	@staticmethod
	def compose(a, b, theta) :
		return math.cos(theta) * a + math.sin(theta) * b

	def deviate(self, other, theta) :
		return math.cos(theta) * self + math.sin(theta) * other
				
	def __add__(self, other) :
		if isinstance(other, Vector) :
			return Vector(
				self.x + other.x,
				self.y + other.y,
				self.z + other.z
			)
	
	def __sub__(self, other) :
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
			
	def __mul__(self, other) :
		if isinstance(other, Vector) :
			return self.scalar_product(other)
		#elif isinstance(other, (int, float, sympy.core.symbol.Symbol,)) :
		#	return self.lambda_product(other)
		else :
			return self.lambda_product(other)
		#	raise ValueError("operation not implemented for this type: {0!r}".format(other))
			
	__rmul__ = __mul__

	def __neg__(self) :
		return Vector(-self.x, -self.y, -self.z)
	
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

	def atan2(self, Fy, Fx) :
		return math.atan2(Fy * self, Fx * self)

	def angle_to(self, other, sign=None) :
		if sign is None :
			c = (self * other) / (
				(1 if self._is_unit else self.norm) *
				(1 if self._is_unit else other.norm)
			)
			try :
				return math.acos(max(-1.0, min(c, 1.0)))
			except TypeError :
				return sympy.acos(c)
		else :
			c = (self * other) / (self.norm * other.norm)
			s = (self @ other) * sign
			return math.copysign(math.acos(max(-1.0, min(c, 1.0))), s)

	def frame(self, other=None) :
		""" return a frame where z is oriented toward other (by default north):

			* no solution is returned if self and other are colinears
			* if other is not specified, v_north is used as other
			* in this case, the frame is not defined at poles
		"""

		if other is None :
			""" return an arbitrarily oriented frame optimized to reduce numerical errors,
			the frame can be defined everywhere """
			c_tpl = self.normalized().as_tuple
			c_max = max(range(len(c_tpl)), key=lambda i: c_tpl[i])

			c_lst = list(c_tpl)
			c_lst[c_max] = 0

			num = sum(c_lst)
			den = c_tpl[c_max]

			y_lst = [1.0, 1.0, 1.0]
			y_lst[c_max] = - num / den

			x = self.normalized()
			y = Vector(* y_lst).normalized()
			z = x @ y

		else :
			x = self
			y = (other @ x).normalized()
			z = x @ y

		return y, z # east, north

	def project(self, normal) :
		return self - ( (self * normal) * normal )
