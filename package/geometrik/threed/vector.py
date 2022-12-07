#!/usr/bin/env python3

import math
import numbers

from operator import is_
import sympy

class Vector() :

	def __init__(self, x, y, z, is_unit=False) :

		self.x = x
		self.y = y
		self.z = z

		self._is_unit = is_unit

		self._is_symbolic = self.is_symbolic
		self.m = sympy if self._is_symbolic else math

	@property
	def is_symbolic(self) :
		return not all(isinstance(i, numbers.Number) for i in self.as_tuple)

	@property
	def as_tuple(self) :
		return self.x, self.y, self.z

	@staticmethod
	def new_symbolic(name) :
		Vx, Vy, Vz = sympy.symbols(' '.join(f'{name}_{i}' for i in 'xyz'))
		return Vector(Vx, Vy, Vz)

	def __repr__(self) :
		if self._is_symbolic :
			return f"{self.__class__.__name__}({sympy.latex(self.x)}, {sympy.latex(self.y)}, {sympy.latex(self.z)})"
		return f"{self.__class__.__name__}({self.x:0.3g}, {self.y:0.3g}, {self.z:0.3g})"

	def __iter__(self) :
		return (i for i in (self.x, self.y, self.z))

	def deflect(self, other, theta) :
		return self.m.cos(theta) * self + self.m.sin(theta) * other
				
	def __add__(self, other) :
		return Vector(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z,
		)
	
	def __sub__(self, other) :
		return self + (- other)
			
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
		)
		
	def __str__(self) :
		return "[" + ', '.join(str(i) for i in self.as_tuple) + "]"
		
	@property
	def norm(self) :
		if self._is_unit :
			return 1
		else :
			# if self._is_symbolic :
			# 	return sympy.symbols('Mn')
			# else :
			return self.m.sqrt(self.norm_2)

	@property
	def norm_2(self) :
		if self._is_unit :
			return 1
		else :
			# if self._is_symbolic :
			# 	return sympy.symbols('Mn') ** 2
			# else :
			return self.scalar_product(self)
		
	def normalized(self) :
		if self._is_unit :
			return self

		n = self.norm

		return Vector(
			self.x / n,
			self.y / n,
			self.z / n,
			is_unit=True,
		)

	def atan2(self, Fy, Fx) :
		return self.m.atan2(Fy * self, Fx * self)

	def angle_to(self, other, way=None) :
		# part of the formula for the angle between two vectors
		ca = (self * other) / (self.norm * other.norm)

		# if the result is numeric, cap it in [-1.0 ; 1.0] for the acos to come
		try :
			cb = max(-1.0, min(float(ca), 1.0))
		except TypeError :
			cb = ca

		# last arccos
		cc = self.m.acos(cb)
		if way is not None :
			s = (self @ other) * way
			try :
				return math.copysign(float(cc), float(s))
			except TypeError :
				return sympy.sign(s) * cc				
		else :
			return cc

	def oriented_frame(self, heading, w=1) : # in radians
		Fn, Fe = self.northeast_frame()

		Fx = Fn.deflect(Fe, heading)
		Fy = Fx @ self.normalized()
		
		return Fx, w*Fy

	
	def northeast_frame(self) :
		Ez = Vector(0, 0, 1)

		Fe = (Ez @ self).normalized()
		Fn = self.normalized() @ Fe

		return Fn, Fe

	def frame(self, other=None) :
		# TODO, migrer dans globe parce que ça a pas de sens ici ?
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
		return ((self * tangent) / (tangent.norm_2)) * tangent

	def rotate(self, axis, alpha) :
		# rotation via le produit triple
		# https://math.stackexchange.com/questions/4277293/finding-vec-b-from-vec-a-times-vec-b-vec-a-and-alpha-angle-vec
		# c'est tellement overkill !!!

		M = axis.normalized()

		An = self.project_normal(M)
		At = self.project_tangent(M)

		AxB = M * An.norm_2 * self.m.sin(alpha)
		Bn = (An * (AxB.norm * (1 / self.m.tan(alpha))) - (An @ AxB) ) * (1 / An.norm_2)
		# Bt = At

		return Bn + At

	def rotate(self, axis, alpha=None) :

		if alpha is None and self._is_symbolic :
			alpha = sympy.Symbol('alpha')
	
		M = axis.normalized()

		An = self.project_normal(M)
		At = self.project_tangent(M)

		Bn = An.deflect(An @ M, alpha)

		return Bn + At

	def subs(self, v_map) :
		# if not self._is_symbolic :
		# 	raise NotImplementedError
		v_lst = self.x, self.y, self.z
		m_lst = list()
		is_symbolic = False
		for v in v_lst :
			try :
				v = v.subs(v_map)
			except AttributeError :
				try :
					v = float(v)
				except TypeError : # can not convert to float directly, there is still some bit a sympy inside
					is_symbolic = True
			m_lst.append(v)
		return Vector(* m_lst)

	def res(self, v_map) :
		return Vector(* [
			( i if isinstance(i, numbers.Number) else float(i.subs(v_map)) )
			for i in self.as_tuple
		])

	def simplify(self) :
		return Vector(* [v.simplify() for v in self.as_tuple], is_symbolic=True)

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches

from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch

class arrow_3d(matplotlib.patches.FancyArrowPatch):
	def __init__(self, xs, ys, zs, *args, **kwargs):
		matplotlib.patches.FancyArrowPatch.__init__(self, (0,0), (0,0), * args, ** kwargs)
		self._verts3d = xs, ys, zs

	def do_3d_projection(self, renderer=None):
		xs3d, ys3d, zs3d = self._verts3d
		xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
		self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
		return np.min(zs)


class VectorPlot() :
	def __init__(self, pth=None) :
		self.pth = pth

	def __enter__(self) :
		self.fig = plt.figure()
		self.axe = self.fig.add_subplot(1, 1, 1, projection='3d')

		return self

	def __exit__(self, exc_type, exc_value, traceback) :
		self.axe.view_init(elev=20.0, azim=0.0)
		if self.pth is None :
			plt.show()
		else :
			plt.savefig(str(self.pth))

	def add_point(self, Ax, name, color='k') :
		self.axe.add_artist(arrow_3d(
			[0.0, Ax.x],
			[0.0, Ax.y],
			[0.0, Ax.z],
			mutation_scale=15, arrowstyle='-|>', color=color, shrinkA=0, shrinkB=0
		))
		self.axe.text(
			2 * Ax.x / 3,
			2 * Ax.y / 3,
			2 * Ax.z / 3,
			name,
			horizontalalignment='center', verticalalignment='center', fontsize=10, color=color
		)

	def add_floating(self, Ax, Bx, name, color='k') :
		self.axe.add_artist(arrow_3d(
			[Ax.x, Ax.x + Bx.x],
			[Ax.y, Ax.y + Bx.y],
			[Ax.z, Ax.z + Bx.z],
			mutation_scale=15, arrowstyle='-|>', color=color, shrinkA=0, shrinkB=0
		))
		self.axe.text(
			2 * (Ax.x + Bx.x) / 3 + Ax.x / 3,
			2 * (Ax.y + Bx.y) / 3 + Ax.y / 3,
			2 * (Ax.z + Bx.z) / 3 + Ax.z / 3,
			name,
			horizontalalignment='center', verticalalignment='center', fontsize=10, color=color
		)

