#!/usr/bin/env python3

import math
import sympy

class Vector() :

	def __init__(self, x, y, z, is_unit=False, is_symbolic=False) :
		self.x = x
		self.y = y
		self.z = z

		self._is_unit = is_unit

		self._is_symbolic = is_symbolic
		self.m = sympy if is_symbolic else math

	@property
	def as_tuple(self) :
		return self.x, self.y, self.z

	@staticmethod
	def symbolic(name) :
		Vx, Vy, Vz = sympy.symbols(' '.join(f'{name}_{i}' for i in 'xyz'))
		return Vector(Vx, Vy, Vz, is_symbolic=True)

	def __repr__(self) :
		if self._is_symbolic :
			return f"{self.__class__.__name__}({sympy.latex(self.x)}, {sympy.latex(self.y)}, {sympy.latex(self.z)})"
		return f"{self.__class__.__name__}({self.x:0.3g}, {self.y:0.3g}, {self.z:0.3g})"

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

	def deflect(self, other, theta) :
		return self.m.cos(theta) * self + self.m.sin(theta) * other
				
	def __add__(self, other) :
		return Vector(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z,
			is_symbolic = self._is_symbolic or other._is_symbolic
		)
	
	def __sub__(self, other) :
		return self + (- other)
		Vector(
			self.x - other.x,
			self.y - other.y,
			self.z - other.z,
			is_symbolic = self._is_symbolic or other._is_symbolic
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

	def __neg__(self) :
		return Vector(
			-self.x,
			-self.y,
			-self.z,
			is_symbolic = self._is_symbolic
		)
	
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
	
	def lambda_product(self, k:float) :
		""" constant * vector product """
		return Vector(
			k * self.x,
			k * self.y,
			k * self.z,
			is_symbolic = self._is_symbolic
		)
				
	def scalar_product(self, other) :
		""" scalar product """
		return self.x * other.x + self.y * other.y + self.z * other.z
		
	def vector_product(self, other) :
		""" vectoriel product """
		return Vector(
			self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x,
			is_symbolic = self._is_symbolic or other._is_symbolic
		)
		
	def __str__(self) :
		return "[" + ', '.join(str(i) for i in self.as_tuple) + "]"
		
	@property
	def norm(self) :
		return self.m.sqrt(self.norm_2)

	@property
	def norm_2(self) :
		return self.scalar_product(self)
		
	def normalized(self) :
		n = self.norm

		return Vector(
			self.x / n,
			self.y / n,
			self.z / n,
			is_unit=True,
			is_symbolic=self._is_symbolic
		)

	def atan2(self, Fy, Fx) :
		return self.m.atan2(Fy * self, Fx * self)

	def angle_to(self, other, way=None) :
		# part of the formula for the angle between two vectors
		ca = (self * other) / (self.norm * other.norm)

		# if the result is numeric, cap it in [-1.0 ; 1.0] for the acos to come
		cb = max(-1.0, min(ca, 1.0)) if not ca._is_symbolic else ca

		# last arccos
		cc = self.m.acos(cb)

		if way is None :
			s = (self @ other) * way
			if cc._is_symbolic :
				return sympy.sign(s) * cc
			else :
				return math.copysign(cc, s)
		else :
			return cc

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

	def project_normal(self, normal) :
		return self - self.project_tangent(normal)

	def project_tangent(self, tangent) :
		return ((self * tangent) * tangent)
