#!/usr/bin/env python3

import math
from dataclasses import dataclass

from geometrik.threed.vector.base import BaseVector


@dataclass(slots=True)
class NumVector(BaseVector):
	__slots__ = ()

	@property
	def norm(self):
		if self.is_unit:
			return 1.0

		return math.hypot(*self)

	@property
	def norm_2(self):
		if self.is_unit:
			return 1.0
		else:
			return self.scalar_product(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({self.x:0.3g}, {self.y:0.3g}, {self.z:0.3g})"

	def __eq__(self, other):
		return (
			math.isclose(self.x, other.x)
			and math.isclose(self.y, other.y)
			and math.isclose(self.z, other.z)
		)

	def normalized(self, tol: float = 1e-15):
		if self.is_unit:
			return self

		n = self.norm
		if n < tol:
			raise ValueError(
				"Impossible de normaliser un vecteur nul ou de norme trop faible."
			)

		return self.__class__(
			self.x / n,
			self.y / n,
			self.z / n,
			is_unit=True,
		)

	def angle_to(self, other, way=None):
		"""Calcule l'angle (en radians) entre `self` et `other`.

		Si `way` est fourni, retourne l'angle orienté dans [-pi, pi] selon le
		signe du produit mixte `(self @ other) * way`. Sinon, retourne l'angle
		non orienté dans [0, pi].
		"""
		ca = (self * other) / (self.norm * other.norm)

		# cap the result in [-1.0 ; 1.0] for the acos
		cb = max(-1.0, min(ca, 1.0))

		# last arccos
		cc = math.acos(cb)
		if way is not None:
			s = (self @ other) * way
			return math.copysign(cc, s)
		else:
			return cc

	def frame(self, other=None):
		"""return a local frame where z is oriented toward other:

		* no solution is returned if self and other are colinears
		* if other is None, an optimal frame is returned, defined everywhere (even at poles)
		"""

		x = self.normalized()

		if other is None:
			""" return an arbitrarily oriented frame optimized to reduce numerical errors,
			the frame can be defined everywhere """

			c_tpl = x.as_tuple
			c_idx = sorted(range(len(c_tpl)), key=lambda i: abs(c_tpl[i]))

			y_lst = [0.0, 0.0, 0.0]
			y_lst[c_idx[1]] = -c_tpl[c_idx[2]]
			y_lst[c_idx[2]] = c_tpl[c_idx[1]]

			other = self.__class__(*y_lst).normalized()

		y = (other @ x).normalized()
		z = x @ y

		return y, z  # east, north


v_null = NumVector(0.0, 0.0, 0.0, True)
v_north = NumVector(0.0, 0.0, 1.0, True)
v_east = NumVector(0.0, 1.0, 0.0, True)
v_down = v_north @ v_east
v_up = v_east @ v_north
