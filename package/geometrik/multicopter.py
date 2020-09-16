#!/usr/bin/env python3

from geometry.frame import Frame
from geometry.quaternion import Quaternion

"""
Le point de départ, l'origine est choisie arbitrairement,
puis la première frame est la frame NED, puis LRD, puis XYZ puis celles des propellers

"""

class Propeller(Frame) :
	def __init__(self, pos_l=None, pos_r=None, reference=None, name=None, is_right=True) :
		Frame.__init__(self, pos_l, pos_r, reference, name)
		self.is_right = is_right
		
class Multicopter() :
	""" un truc sans surface porteuse """
	
	gravity = 9.807
	inertial_x = 1.2
	interial_y = 1.2
	interi
	
	def __init__(self, lat, lon, alt) :
		self.contact_lst = list()
		self.prop_lst = list()
		
		self.time = 0.0
		self.weight = 2.0
		
		self.local_frame = Frame.init_NorthEastDown(lat, lon, alt)
		self.horizontal_frame = Frame(ref=self.local_frame)
		self.body_frame = Frame(ref=self.horizontal_frame)
		
	def add_propeller(is_right, pos, ori=None) :
		if ori is None :
			ori = geometry.quaternion.identity()
		self.prop_lst.append(pos, ori, self.body_frame, 'prop_{0}'.format(len(self.prop_lst) + 1))
		self.contact_lst.append(pos)
		
		#  la poussée est en Z, is_right = True si le sens de rotation est de x vers y
		
		
def setup_hexacopter(lat, lon, alt) :
	m = Multicopter(lat, lon, alt)
	
	m.add_propeller(True, Quaternion.from_vector(2.0, 1.0, 0.0))
	m.add_propeller(False, Quaternion.from_vector(0.0, 2.0, 0.0), Quaternion.from_axial_rotation(1.0, 0.0, 0.0, -15.0))
	m.add_propeller(True, Quaternion.from_vector(-2.0, 1.0, 0.0))
	m.add_propeller(False, Quaternion.from_vector(-2.0, -1.0, 0.0))
	m.add_propeller(True, Quaternion.from_vector(0.0, -2.0, 0.0), Quaternion.from_axial_rotation(1.0, 0.0, 0.0, 15.0))
	m.add_propeller(False, Quaternion.from_vector(2.0, -1.0, 0.0))
	
	m.contact_lst.append(Quaternion.from_vector(1.0, 1.0, -1.0))
	m.contact_lst.append(Quaternion.from_vector(1.0, -1.0, -1.0))
	m.contact_lst.append(Quaternion.from_vector(-1.0, -1.0, -1.0))
	m.contact_lst.append(Quaternion.from_vector(-1.0, 1.0, -1.0))

if __name__ == __main__ :
	u = setup_hexacopter(0.0, 0.0, 0.0)