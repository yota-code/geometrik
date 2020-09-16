#!/usr/bin/env python3

import math

from quaternion import Quaternion

earth_omega = 7292115.0e-11 # earth rotation rate in [rad.s-1]

def wgs84_to_cartesian(lat, lon, alt) :
	a = 6378137.0
	b = a * (1 - (1.0 / 298.257223563))
	lat, lon = math.radians(lat), math.radians(lon)
	n = (a * a) / math.sqrt(
		(a * a) * (math.cos(lat) ** 2) +
		(b * b) * (math.sin(lat) ** 2)
	)
	x = (n + alt) * math.cos(lat) * math.cos(lon)
	y = (n + alt) * math.cos(lat) * math.sin(lon)
	z = ((b * b) / (a * a) * n + alt) * math.sin(lat)
	return x, y, z
	

class Frame() :
	def __init__(self, pos_l=None, pos_r=None, ref=None, name=None) :
		# coordonnées de l'origine dans le repère parent
		self.pos_l = Quaternion.null() if pos_l is None else pos_l
		
		# orientation du nouveau repère par rapport au repère parent
		self.pos_r = (Quaternion.identity() if pos_r is None else pos_r).normalize()
		
		self._ref = ref
		self._name = name
		
	def dbg(self, * pos, ** nam) :
		if __debug__ :
			print(* pos, ** nam)
		
	@property
	def name(self) :
		return "{0} / {1}".format(
			self._name if self._name is not None else "Frame",
			self._ref._name if self._ref is not None else "_absolute_"
		)
		
	def __str__(self) :
		stack = list()
		stack.append(self.name)
		stack.append(' - pos_l: {0}'.format(', '.join(str(i) for i in self.pos_l.to_vector())))
		stack.append(' - pos_r:')
		stack += ['\t' + ', '.join('{0: 3.3f}'.format(i) for i in line) for line in self.pos_r.basis()]
		
		return '\n'.join(stack)
		
	@staticmethod
	def init_NorthEastDown(lat, lon, alt, time=0) :
		"""
		time, c'est l'heure relative par rapport au départ, permet de suivre la rotation de la terre
		"""
		q = Quaternion.from_axial_rotation(0.0, 1.0, 0.0, -90.0)
		lon += math.degrees(earth_omega * time)
		return Frame(
			Quaternion.from_vector(* wgs84_to_cartesian(lat, lon, alt)),
			Quaternion.from_euler_rotation(0.0, -lat, lon) * q,
			None, "NED"
		)
		
	@staticmethod
	def init_EastNorthUp(lat, lon, alt, time=0) :
		q = Quaternion.from_axial_rotation(1.0, 1.0, 1.0, 90.0)
		q.print_basis()
		lon += math.degrees(earth_omega * time)
		return Frame(
			Quaternion.from_vector(* wgs84_to_cartesian(lat, lon, alt)),
			Quaternion.from_euler_rotation(0.0, -lat, lon) * q,
			None, "ENU"
		)
		
	@property
	def reference_lst(self) :
		stack = list()
		f = self
		stack.append(f)
		while f._ref is not None :
			f = f._ref
			stack.append(f)
		return stack
		
	def transport(self, other) :
		"""
		smartly transpose from one frame (self) to another (other)
		validated 2017.03.24
		"""
		self_lst = list()
		f = self
		while f._ref is not None :
			f = f._ref
			self_lst.append(f)
		self_lst.append(None)
		
		other_lst = list()
		f = other
		while f._ref not in self_lst :
			other_lst.append(f)		
			f = f._ref
		other_lst.append(f)		
		
		f = self
		self.dbg(f)
		while f._ref != other_lst[-1]._ref :
			f = f._pop_reference()
			self.dbg(f)
		while other_lst :
			f = other_lst.pop()._push_reference(f)
			self.dbg(f)
		return f
		
	def _pop_reference(self) :
		""" for a frame f4 defined as f0 < f1 < f2 < f3 < f4, return f0 < f1 < f2 < f4 """
		""" self._ref must not be None """
		return Frame(
			self._ref.pos_l + self.pos_l.rotate(self._ref.pos_r),
			self._ref.pos_r * self.pos_r,
			self._ref._ref, self._name
		)
		
	def _push_reference(self, other) :
		""" self._ref must be equal to other._ref """
		# print("attempt to push {0} onto {1}".format(self.name, other.name))
		if self._ref != other._ref :
			raise ValueError("both frames must have the same reference:\n{0}\n{1}".format(self, other))
		return Frame(
			(other.pos_l - self.pos_l).rotate(self.pos_r.conjugate),
			self.pos_r.conjugate * other.pos_r,
			self, other._name
		)
		
	def _to_absolute_iterative(self) :
		"""
		express the current frame in the absolute frame,
		return a Fram whose parent is None
		1% plus rapide qu'en réccursif
		validated 2017.03.22
		"""
		f = self
		while f._ref is not None :
			f = f._pop_reference()
		return f
		
	def _to_absolute_recursive(self) :
		"""
		express the current frame in the absolute frame,
		return a Fram whose parent is None
		validated 2017.03.22
		"""
		if self._ref is None :
			return self
		else :
			return self._pop_reference().to_absolute_recursive()
			
	to_absolute = _to_absolute_iterative
		
	def to_relative_recursive(self, other) :
		"""
		express an absolute frame (other) into the current frame
		validated 2017.03.22
		"""

		if self._ref is None :
			return self._push_reference(other)
		else :
			return self._ref.to_relative_recursive(other)
			
class DynamicFrame() :
	def __init__(self) :
		self.lin_0 = Quaternion.null() # position du centre de gravité
		self.rot_0 = Quaternion.null() # orientation du solide
		self.lin_1 = Quaternion.null() # vitesse du centre de gravité
		self.rot_1 = Quaternion.null() # vitesse de rotation du solide
		self.lin_2 = Quaternion.null() # accéleration du centre de gravité
		self.rot_2 = Quaternion.null() # accélération angulaire du solide
		
		self.ref = None
		
		self.time = 0
		
		self.lin_mass = 1.0
		self.rot_mass
		
	def step(self, time, force, torque) :
		if time <= self.time :
			raise ValueError
		self.lin_2
		
	
if __name__ == '__main__' :
		
	pass

	
	