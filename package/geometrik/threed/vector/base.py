#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Literal

import sympy

from geometrik.threed.vector.numeric import NumVector
from geometrik.threed.vector.symbolic import SymVector

Way = Literal[-1, 1]


@dataclass(slots=True)
class Vector:
	x: float | sympy.Expr
	y: float | sympy.Expr
	z: float | sympy.Expr

	def __new__(cls, *args):
		if len(args) == 3:
			return object.__new__(NumVector)
		elif len(args) == 1 and isinstance(args[0], str):
			return object.__new__(SymVector)

		raise TypeError("Constructeur invalide")

	def __iter__(self):
		yield self.x
		yield self.y
		yield self.z

	def __len__(self):
		return 3

	@property
	def as_vector(self):
		return self

	@property
	def as_tuple(self):
		return tuple(self)

	@property
	def as_list(self):
		return list(self)

	def __add__(self, other):
		return self.__class__(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z,
		)

	def __neg__(self):
		return self.__class__(
			-self.x,
			-self.y,
			-self.z,
		)

	def __sub__(self, other):
		return self + (-other)

	def lambda_product(self, k):
		"""constant * vector product"""
		return self.__class__(
			k * self.x,
			k * self.y,
			k * self.z,
		)

	def scalar_product(self, other):
		"""scalar product"""
		return self.x * other.x + self.y * other.y + self.z * other.z

	def vector_product(self, other):
		"""vectoriel product"""
		return self.__class__(
			self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x,
		)

	def __matmul__(self, other):
		if isinstance(other, Vector):
			return self.vector_product(other)
		else:
			raise ValueError(f"operation not implemented for this type: {other!r}")

	def atan2(self, Fy, Fx):
		return self.m.atan2(Fy * self, Fx * self)

	def northeast_frame(self):
		"""Return a north east frame.
		* The origin is given by the vector itself,
		* the Fe point toward the east
		* the Fn point toward the north"""
		Ez = Vector(0, 0, 1)

		Fe = (Ez @ self).normalized()
		Fn = self.normalized() @ Fe

		return Fn, Fe

	def oriented_frame(self, heading: float, w: Way = 1):
		"""Return a nort east frame rotated with a given heading."""
		Fn, Fe = self.northeast_frame()

		Fx = Fn.deflect(Fe, heading)
		Fy = Fx @ self.normalized()

		return Fx, w * Fy

	def project_normal(self, normal):
		"""Project the vector on a normal vector."""
		return self - self.project_tangent(normal)

	def project_tangent(self, tangent):
		"""Project the vector on a tangent vector."""
		return ((self * tangent) / (tangent.norm_2)) * tangent
