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

		print(f"{name} = {point_b}")
		
		point_a = g3d.Point.origin()

		self.axe.add_artist(arrow_3d(
			[point_a.x, point_b.x],
			[point_a.y, point_b.y],
			[point_a.z, point_b.z],
			mutation_scale=15, arrowstyle='-|>', color=color, shrinkA=0, shrinkB=0
		))
		self.axe.text(
			(point_a.x + point_b.x)/2,
			(point_a.y + point_b.y)/2,
			(point_a.z + point_b.z)/2,
			name,
			horizontalalignment='center', verticalalignment='center', fontsize=10, color=color
		)

if __name__ == '__main__' :

	with UnitSpherePlot() as u :
		u.add_vector(None, g3d.Vector(1.0, 0.0, 0.0), 'x', 'r')
		u.add_vector(None, g3d.Vector(0.0, 1.0, 0.0), 'y', 'g')
		u.add_vector(None, g3d.Vector(0.0, 0.0, 1.0), 'z', 'b')