#!/usr/bin/env python3

"""
https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
http://math.stackexchange.com/questions/331021/does-anyone-know-any-resources-for-quaternions-for-truly-understanding-them

http://stackoverflow.com/questions/1171849/finding-quaternion-representing-the-rotation-from-one-vector-to-another
https://bitbucket.org/sinbad/ogre/src/9db75e3ba05c/OgreMain/include/OgreVector3.h?fileviewer=file-view-default#cl-651

http://www.camelsoftware.com/2016/02/21/quaternion-formulas/
"""

import math
import collections

class Quaternion() :
	def __init__(self, w, x, y, z, is_unit=False) :
		self.w = w
		self.x = x
		self.y = y
		self.z = z
		self._is_unit = is_unit
	
	@staticmethod
	def identity() :
		return Quaternion(1.0, 0.0, 0.0, 0.0)
		
	@staticmethod
	def null() :
		return Quaternion(0.0, 0.0, 0.0, 0.0)
		
	@property
	def norm(self) :
		return math.sqrt(self._norm_2)
		
	def basis(self) :
		""" return the orthogonal basis after a transformation by q """
		xi = Quaternion.from_vector(1.0, 0.0, 0.0)
		yi = Quaternion.from_vector(0.0, 1.0, 0.0)
		zi = Quaternion.from_vector(0.0, 0.0, 1.0)
		
		xf = xi.rotate(self)
		yf = yi.rotate(self)
		zf = zi.rotate(self)
		
		print(xf, yf, zf)
		return
		
		return [p for p in list(zip(xf, yf, zf))[1:]]
		
	def rotation_to(self, other) :
		""" return the quaternion required to pass from self to other """
		# http://stackoverflow.com/questions/1171849/finding-quaternion-representing-the-rotation-from-one-vector-to-another
		pass
		
	@staticmethod
	def from_vector(x, y, z) :
		return Quaternion(0.0, x, y, z)
		
	def as_matrix(self) :
		return np.array([
			[ self.w, -self.x, -self.y, -self.z ],
			[ self.x,  self.w, -self.z,  self.y ],
			[ self.y,  self.z,  self.w, -self.x ],
			[ self.z, -self.y,  self.x,  self.w ]
		], dtype=np.float64)
		
	def as_vector(self) :
		return np.array([
			[ self.w ],
			[ self.x ],
			[ self.y ],
			[ self.z ]
		], dtype=np.float64)		

	def to_vector(self) :
		return self.x, self.y, self.z

	def rotate(self, q) :
		return q * self * q.conjugate
		
	@staticmethod
	def from_axial_rotation(x, y, z, alpha, mode='degrees') :
		"""
			where x, y, z are the components of the rotation axis
			alpha is the amount of rotation in radians
		"""
		if mode == 'degrees' :
			alpha = math.radians(alpha)
			
		return Quaternion(
			math.cos(alpha / 2.0),
			x * math.sin(alpha / 2.0),
			y * math.sin(alpha / 2.0),
			z * math.sin(alpha / 2.0)
		).normalize()
		
	def to_axial_rotation(self, mode='degrees') :
		r = 2.0 * math.acos(self.w)
		if mode == 'degrees' :
			r = math.degrees(r)
		q = math.sqrt(1.0 - (self.w * self.w)) # presque inutile... si le vecteur est normalisé
		return (
			self.x / q,
			self.y / q,
			self.z / q,
			r
		)
		
	@staticmethod
	def from_euler_rotation(phi, theta, psi, mode='degrees') :
		"""
		roll, pitch & yaw
		return a unit-quaternion which describe the euler rotation of yaw - theta - roll, in this order
		"""
		
		if mode == 'degrees' :
			phi, theta, psi = math.radians(phi), math.radians(theta), math.radians(psi)
		
		rc, rs = math.cos(phi / 2.0), math.sin(phi / 2.0)
		pc, ps = math.cos(theta / 2.0), math.sin(theta / 2.0)
		yc, ys = math.cos(psi / 2.0), math.sin(psi / 2.0)
		
		return Quaternion(
			(yc * pc * rc) + (ys * ps * rs),
			(yc * pc * rs) - (ys * ps * rc),
			(yc * ps * rc) + (ys * pc * rs),
			(ys * pc * rc) - (yc * ps * rs)
		).normalize()
		
	def to_euler(self, mode='degrees') :
		k = 2.0 * ((self.w * self.y) - (self.x * self.z))
		k = min(1.0, k)
		k = max(k, -1.0)
		phi, theta, psi = (
			math.atan2(2.0 * ((self.w * self.x) + (self.y * self.z)),  1.0 - 2.0 * ((self.x * self.x) + (self.y * self.y))),
			math.asin(k),
			math.atan2(2.0 * ((self.w * self.z) + (self.x * self.y)),  1.0 - 2.0 * ((self.y * self.y) + (self.z * self.z)))
		)
		if mode == 'degrees' :
			phi, theta, psi = math.degrees(phi), math.degrees(theta), math.degrees(psi)
		return phi, theta, psi

	def __mul__(self, other) :
		if isinstance(other, Quaternion) :
			q = Quaternion(
				(self.w * other.w) - (self.x * other.x) - (self.y * other.y) - (self.z * other.z),
				(self.w * other.x) + (self.x * other.w) + (self.y * other.z) - (self.z * other.y),
				(self.w * other.y) - (self.x * other.z) + (self.y * other.w) + (self.z * other.x),
				(self.w * other.z) + (self.x * other.y) - (self.y * other.x) + (self.z * other.w)
			)
		else :
			q = self.__rmul__(other)
		#print("__mul__({0}, {1}) => {2}".format(self, other, q))
		return q			
			
	def __rmul__(self, other) :
		if isinstance(other, float) or isinstance(other, int) :
			q = Quaternion(other * self.w, other * self.x, other * self.y, other * self.z)
		#print("__rmul__({0}, {1}) => {2}".format(self, other, q))
		return q
			
	def __truediv__(self, other) :
		#print("__truediv__({0}, {1})".format(self, other))
		if isinstance(other, Quaternion) :
			return self * (1.0 / other)
		else :
			return self.__rdiv__(other)
			
	def __rtruediv__(self, other) :
		#print("__rdiv__({0}, {1})".format(self, other))
		if isinstance(other, float) or isinstance(other, int) :
			return self.conjugate  * (other / self._norm_2)
			# if u is a unit quaternion, then 1.0 / u == u.conjugate
			
	def __add__(self, other) :
		if isinstance(other, Quaternion) :
			return Quaternion(
				self.w + other.w,
				self.x + other.x,
				self.y + other.y,
				self.z + other.z
			)
		elif isinstance(other, float) or isinstance(other, int) :
			return Quaternion(
				self.w + other,
				self.x,
				self.y,
				self.z
			)

	def __sub__(self, other) :
		if isinstance(other, Quaternion) :
			return Quaternion(
				self.w - other.w,
				self.x - other.x,
				self.y - other.y,
				self.z - other.z
			)
		elif isinstance(other, float) or isinstance(other, int) :
			return Quaternion(
				self.w - other,
				self.x,
				self.y,
				self.z
			)

	@property
	def value(self) :
		return self.w, self.x, self.y, self.z
			
	@property
	def conjugate(self) :
		return __class__(self.w, -self.x, -self.y, -self.z)
		
	@property
	def _norm_2(self) :
		return (self.w * self.w) + (self.x * self.x) + (self.y * self.y) + (self.z * self.z)
		
	@property
	def norm(self) :
		return math.sqrt(self._norm_2)
		
	def normalize(self) :
		n = self.norm
		return Quaternion(self.w / n, self.x / n, self.y / n, self.z / n, True) if n != 1.0 else self
		
	def __str__(self) :
		return ("({0:+.3g} {1:+.3g}i {2:+.3g}j {3:+.3g}k)".format(* self.value))
		
if __name__ == '__main__' :
	
	p = Quaternion.from_euler_rotation(0.0, -90.0, 0.0)
	p.basis()
	
	p = Quaternion.identity()
	p.basis()
	
	r1 = Quaternion.from_axial_rotation(0.0, 0.0, 1.0, 90.0)
	r1.basis()
	r2 = Quaternion.from_axial_rotation(1.0, 0.0, 0.0, 180.0)
	r2.basis()
	q = r1 * r2
	q.basis()
	print(q.to_axial_rotation())
	
	
	