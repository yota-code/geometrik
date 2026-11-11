import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import proj3d


class arrow_3d(matplotlib.patches.FancyArrowPatch):
	def __init__(self, xs, ys, zs, *args, **kwargs):
		matplotlib.patches.FancyArrowPatch.__init__(
			self, (0, 0), (0, 0), *args, **kwargs
		)
		self._verts3d = xs, ys, zs

	def do_3d_projection(self, renderer=None):
		xs3d, ys3d, zs3d = self._verts3d
		xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
		self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
		return np.min(zs)


class VectorPlot:
	def __init__(self, pth=None):
		self.pth = pth

	def __enter__(self):
		self.fig = plt.figure()
		self.axe = self.fig.add_subplot(1, 1, 1, projection="3d")

		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.axe.view_init(elev=20.0, azim=0.0)
		if self.pth is None:
			plt.show()
		else:
			plt.savefig(str(self.pth))

	def add_point(self, Ax, name, color="k"):
		self.axe.add_artist(
			arrow_3d(
				[0.0, Ax.x],
				[0.0, Ax.y],
				[0.0, Ax.z],
				mutation_scale=15,
				arrowstyle="-|>",
				color=color,
				shrinkA=0,
				shrinkB=0,
			)
		)
		self.axe.text(
			2 * Ax.x / 3,
			2 * Ax.y / 3,
			2 * Ax.z / 3,
			name,
			horizontalalignment="center",
			verticalalignment="center",
			fontsize=10,
			color=color,
		)

	def add_floating(self, Ax, Bx, name, color="k"):
		self.axe.add_artist(
			arrow_3d(
				[Ax.x, Ax.x + Bx.x],
				[Ax.y, Ax.y + Bx.y],
				[Ax.z, Ax.z + Bx.z],
				mutation_scale=15,
				arrowstyle="-|>",
				color=color,
				shrinkA=0,
				shrinkB=0,
			)
		)
		self.axe.text(
			2 * (Ax.x + Bx.x) / 3 + Ax.x / 3,
			2 * (Ax.y + Bx.y) / 3 + Ax.y / 3,
			2 * (Ax.z + Bx.z) / 3 + Ax.z / 3,
			name,
			horizontalalignment="center",
			verticalalignment="center",
			fontsize=10,
			color=color,
		)
