#!/usr/bin/env python3

import sympy
from geometric.treed.vector.base import Vector


class SymVector(Vector):
	m = sympy

	def __init__(self, name, is_unit=False):
		self.x, self.y, self.z = self.m.symbols(" ".join(f"{name}_{i}" for i in "xyz"))
		self._is_unit = is_unit

	def __repr__(self):
		return f"{self.__class__.__name__}({self.m.latex(self.x)}, {self.m.latex(self.y)}, {self.m.latex(self.z)})"

	@property
	def norm_2(self):
		if self._is_unit:
			return 1
		else:
			return self.scalar_product(self)

	@property
	def norm(self):
		if self._is_unit:
			return 1
		else:
			return self.m.sqrt(self.norm_2)

	def normalized(self, tol: float = 1e-15):
		if self._is_unit:
			return self

		n = self.norm
		try:
			n = float(n)
			if n < tol:
				raise ValueError(
					"Impossible de normaliser un vecteur nul ou de norme trop faible."
				)
		except TypeError:
			pass

		return self.__class__(
			self.x / n,
			self.y / n,
			self.z / n,
			is_unit=True,
		)

	def angle_to(self, other, way=None):
		# part of the formula for the angle between two vectors
		ca = (self * other) / (self.norm * other.norm)

		try:
			cb = max(-1.0, min(float(ca), 1.0))
		except TypeError:
			cb = ca

		# last arccos
		cc = self.m.acos(cb)
		if way is not None:
			s = (self @ other) * way
			return self.m.sign(s) * cc
		else:
			return cc
