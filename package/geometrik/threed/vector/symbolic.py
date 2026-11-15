#!/usr/bin/env python3

from dataclasses import dataclass

import sympy

from geometrik.threed.vector.base import BaseVector


@dataclass(slots=True)
class SymVector(BaseVector):
	@classmethod
	def symbol(cls, name: str, is_unit: bool = False):
		x, y, z = sympy.symbols(f"{name}_x {name}_y {name}_z")
		return cls(x, y, z, is_unit=is_unit)

	def __repr__(self):
		return f"{self.__class__.__name__}({sympy.latex(self.x)}, {sympy.latex(self.y)}, {sympy.latex(self.z)})"

	@property
	def norm_2(self):
		if self.is_unit:
			return 1
		else:
			return self.scalar_product(self)

	@property
	def norm(self):
		if self.is_unit:
			return 1
		else:
			return sympy.sqrt(self.norm_2)

	def normalized(self, tol: float = 1e-15):
		if self.is_unit:
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
		cc = sympy.acos(cb)
		if way is not None:
			s = (self @ other) * way
			return sympy.sign(s) * cc
		else:
			return cc


v_null = SymVector(0, 0, 0, True)
v_north = SymVector(0, 0, 1, True)
v_east = SymVector(0, 1, 0, True)
v_down = v_north @ v_east
v_up = v_east @ v_north
