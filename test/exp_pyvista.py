import numpy as np
import pyvista as pv


class SphereVisualizerPV:
	def __init__(self, off_screen=False):
		# off_screen=True est utile pour exporter des images ou intégrer dans un notebook
		self.plotter = pv.Plotter(off_screen=off_screen)
		self._init_scene()

	def _init_scene(self):
		# Sphère unité semi-transparente avec éclairage lissé
		sphere = pv.Sphere(radius=1.0, theta_resolution=40, phi_resolution=40)
		self.plotter.add_mesh(
			sphere,
			color="#4C78A8",
			opacity=0.18,
			smooth_shading=True,
			specular=0.5,
			pickable=False,
		)

		# Ajout des axes de repère X, Y, Z au centre et en coin d'écran
		self.plotter.add_axes()
		self.plotter.show_bounds(
			bounds=[-1.1, 1.1, -1.1, 1.1, -1.1, 1.1],
			grid="back",
			location="outer",
			font_size=10,
		)

	def add_vector(
		self, u, label=None, color="#EF553B", shaft_radius=0.02, tip_radius=0.05
	):
		u = np.asarray(u, dtype=float)
		norm = float(np.linalg.norm(u))

		if norm < 1e-4:
			return self

		# Création d'une flèche 3D native proportionnelle à la norme de u
		arrow = pv.Arrow(
			start=(0.0, 0.0, 0.0),
			direction=u,
			scale=norm,
			tip_length=0.18 / norm if norm > 0.2 else 0.3,
			tip_radius=tip_radius / norm,
			shaft_radius=shaft_radius / norm,
		)
		self.plotter.add_mesh(arrow, color=color, smooth_shading=True, label=label)

		# Étiquette flottante au bout du vecteur si un nom est fourni
		if label:
			self.plotter.add_point_labels(
				[u * 1.08],
				[f"{label} ({norm:.2f})"],
				font_size=12,
				text_color=color,
				shape_opacity=0.0,
				always_visible=True,
			)
		return self

	def add_right_angle(self, u, v, size=0.15, color="gray", line_width=3):
		u, v = np.asarray(u, dtype=float), np.asarray(v, dtype=float)
		nu, nv = np.linalg.norm(u), np.linalg.norm(v)

		if nu < 0.05 or nv < 0.05:
			return self

		ua, va = u / nu, v / nv
		pts = np.array([size * ua, size * (ua + va), size * va])

		# Tracé de la ligne brisée (P1 -> P2 -> P3)
		corner = pv.MultipleLines(points=pts)
		self.plotter.add_mesh(corner, color=color, line_width=line_width)
		return self

	def show(self):
		"""Ouvre la fenêtre VTK/OpenGL native interactive (hors navigateur)."""
		self.plotter.show()

	def save_image(self, path="sphere_pv.png"):
		"""Sauvegarde un rendu HD sans ouvrir de fenêtre (nécessite off_screen=True)."""
		self.plotter.screenshot(path)
		self.plotter.close()


if __name__ == "__main__":
	u = np.array([1.0, 0.0, 0.0])
	v = np.array([0.4, 0.9165, 0.0])  # Vecteur unitaire dans le plan XY
	w = np.cross(u, v)

	viz = SphereVisualizerPV()
	(
		viz.add_vector(u, label="U", color="#EF553B")
		.add_vector(v, label="V", color="#00CC96")
		.add_vector(w, label="U × V", color="#636EFA")
		.add_right_angle(u, w, color="#EF553B")
		.add_right_angle(v, w, color="#00CC96")
	)
	viz.show()
