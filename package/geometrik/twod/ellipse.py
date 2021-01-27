#!/usr/bin/env python3

import collections
import math

import numpy as np
import matplotlib.pyplot as plt

def semi_factorial(n) :
	# https://en.wikipedia.org/wiki/Double_factorial
	result = 1
	while (n > 0) :
		result *= n
		n -= 2
	return result

class Ellipse() :
	def __init__(self, a, b, c=0, d=0, f=0, g=-1) :
		# https://en.wikipedia.org/wiki/2*fllipse#General_ellipse
		self.m = np.matrix([
			[a, c, d],
			[c, b, f],
			[d, f, g]
		])
	
	def from_canonical(self, xa, yb, xo, yo, theta) :
		# xa is the semi major axis
		# yb is the semi minor axis
		# xo and yo are the coordinates of the center of the ellipse
		# theta is the orientation of the ellipse
		a = xa**2 * math.sin(theta)**2 + yb**2 * math.cos(theta)**2
		b = xa**2 * math.cos(theta)**2 + yb**2 * math.sin(theta)**2
		c = (yb**2 - xa**2)*math.sin(theta)*math.cos(theta)

		f = a*xo**2 + 2*c*xo*yo + b*yo**2 - xa**2*yb**2

	def get_parameters(self) :
		return self.m[0, 0], self.m[1,1], self.m[0, 1], self.m[0, 2], self.m[1, 2], self.m[2, 2]

	def axis_len(self) :
		a, b, c, d, f, g = self.get_parameters()

		delta = 2*c**2 - 4*a*b
		q0 = math.sqrt((a - b)**2 + 2*c**2)
		q1 = 2*(2*a*f**2 + 2*b*d**2 - 6*c*d*f + (delta)*g)

		long_axis = (-math.sqrt(q1*((a + b) + q0))) / (delta)
		short_axis = (-math.sqrt(q1*((a + b) - q0))) / (delta)

		return long_axis, short_axis

	def circumference(self, a, b, max_iter=32) :
		# https://en.wikipedia.org/wiki/Ellipse#Circumference (Ivory & Bessel Formula)

		""" this function iterate as long as the next term add a contribution to the accuracy """

		h = (a - b)**2 / (a + b)**2

		result = 0.0
		prev = None
		for i in range(max_iter) :
			result += (
				( semi_factorial(2*(i+1)-1) / (2**(i+1) * math.factorial(i+1) )) *
				( (h**(i+1)) / (2*(i+1) - 1)**2 )
			)
			if result == prev :
				break
			prev = result
		return math.pi*(a + b)*(1 + result)

class PolarEarthSlice(Ellipse) :

	a = 6378137.0
	inv_f = 298.257223563

	def __init__(self) :
		self.f = 1.0 / self.inv_f
		self.b = self.a * (1.0 - self.f)
		self.e = math.sqrt(2.0*self.f - self.f**2)

	def circumference(self) :
		return Ellipse.circumference(self, self.a, self.b)

	def demo(self) :
		shape = collections.defaultdict(list)
		radius = dict()

		n = 1024

		radius['ns'] = self.circumference() / math.tau
		radius['ew'] = self.a
		radius['average'] = (radius['ns'] + radius['ew']) / 2
		radius['average 2 ns'] = (2*radius['ns'] + radius['ew']) / 3
		radius['average 2 ew'] = (radius['ns'] + 2*radius['ew']) / 3

		for k, v in radius.items() :
			print(f'{k} = {v}, {v - self.a}, {v - self.b} {v.hex()}')

		for i in range(n) :
			t = i * math.pi / (2*n)
			# if not math.pi/4 - 0.2  < t < math.pi/4 + 0.2 :
			# 	continue
			# t = i * math.tau / (n)
			shape['wgs'].append((self.a * math.cos(t), self.b * math.sin(t)))
			for k, v in radius.items() :
				shape[k].append((radius[k] * math.cos(t), radius[k] * math.sin(t)))

		for k in shape :
			plt.plot([i[0] for i in shape[k]], [i[1] for i in shape[k]], label=k)
		plt.axis('equal')
		plt.legend()
		plt.show()

if __name__ == '__main__' :

	v = PolarEarthSlice()
	v.demo()

