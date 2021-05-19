#!/usr/bin/env python3

import math

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as plt3

import matplotlib.patches

from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib.patches import FancyArrowPatch

import geometrik.threed as g3d

class arrow_3d(matplotlib.patches.FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        matplotlib.patches.FancyArrowPatch.__init__(self, (0,0), (0,0), * args, ** kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        matplotlib.patches.FancyArrowPatch.draw(self, renderer)

class UnitSpherePlot() :
	def __init__(self) :
		pass

	def __enter__(self) :
		u = np.linspace(0, 2 * np.pi, 100)
		v = np.linspace(0, np.pi, 100)

		sphere_x = np.outer(np.cos(u), np.sin(v))
		sphere_y = np.outer(np.sin(u), np.sin(v))
		sphere_z = np.outer(np.ones(np.size(u)), np.cos(v))

		self.fig = plt.figure()
		self.axe = self.fig.add_subplot(1, 1, 1, projection='3d')
		self.axe.plot_surface(sphere_x, sphere_y, sphere_z, color='b', alpha=0.05)
		self.axe.plot(np.cos(u), np.sin(u), np.zeros_like(u), color='r', alpha=0.2)

		color_map = { 0: 'g', 2: 'b' }
		for i in range(8) :
			color = color_map.get(i, 'black')
			self.axe.plot(
				np.sin(v) * np.cos(i * math.tau / 8),
				np.sin(v) * np.sin(i * math.tau / 8),
				np.cos(v),
				color=color, alpha=0.2
			)
		return self

	def __exit__(self, exc_type, exc_value, traceback) :
		plt.show()

	def add_point(self, point_b, name, color='k') :

		# print(f"{name} = {point_b}")
		
		self.axe.add_artist(arrow_3d(
			[0.0, point_b.x],
			[0.0, point_b.y],
			[0.0, point_b.z],
			mutation_scale=15, arrowstyle='-|>', color=color, shrinkA=0, shrinkB=0
		))
		self.axe.text(
			point_b.x / 2,
			point_b.y / 2,
			point_b.z / 2,
			name,
			horizontalalignment='center', verticalalignment='center', fontsize=10, color=color
		)

	def add_arc(self, point_a, point_b, color='k') :
		x = point_a
		z = (point_a @ point_b).normalized()
		y = z @ x

		d = point_a.angle_to(point_b)
		p_lst = list()
		for t in np.linspace(0.0, d, 100) :
			q = x * math.cos(t) + y * math.sin(t)
			p_lst.append([q.x, q.y, q.z])

		self.axe.plot(
			[i[0] for i in p_lst],
			[i[1] for i in p_lst],
			[i[2] for i in p_lst], color=color
		)

	def add_circle(self, center, other, color='k') :
		x = center
		z = (center @ other).normalized()
		y = z @ x

		d = center.angle_to(other)

		p_lst = list()
		for t in np.linspace(0.0, math.tau, 100) :
			q = (y * math.cos(t) + z * math.sin(t))
			r = (x * math.cos(d) + q * math.sin(d))
			p_lst.append([r.x, r.y, r.z])

		self.axe.plot(
			[i[0] for i in p_lst],
			[i[1] for i in p_lst],
			[i[2] for i in p_lst], color=color
		)

	def add_circle_part(self, Cx, Ax, Bx, color='k') :
		Az = (Cx @ Ax).normalized()
		Ay = Az @ Cx

		Bz = (Cx @ Bx).normalized()
		By = Bz @ Cx

		z = By.signed_angle_to(Ay, Cx)

		d1 = Cx.angle_to(Ax)
		d2 = Cx.angle_to(Bx)

		d = (d1 + d2)/2

		p_lst = list()
		for t in np.linspace(0.0, z, 100) :
			q = (By * math.cos(t) + Bz * math.sin(t))
			r = (Cx * math.cos(d) + q * math.sin(d))
			p_lst.append([r.x, r.y, r.z])

		self.axe.plot(
			[i[0] for i in p_lst],
			[i[1] for i in p_lst],
			[i[2] for i in p_lst], color=color
		)




if __name__ == '__main__' :

	x = g3d.Vector(1.0, 0.0, 0.0)
	y = g3d.Vector(0.0, 1.0, 0.0)
	z = g3d.Vector(0.0, 0.0, 1.0)

	with UnitSpherePlot() as u :
		u.add_point(x, 'x', 'r')
		u.add_point(y, 'y', 'g')
		u.add_point(z, 'z', 'b')
		u.add_arc(x, y, 'k')