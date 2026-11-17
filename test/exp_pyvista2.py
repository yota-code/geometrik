import numpy as np
import pyvista as pv


class InteractiveSpherePV:
	def __init__(self):
		self.plotter = pv.Plotter(window_size=(1100, 800))
		self.angles = {"theta_u": 0.0, "phi_u": 90.0, "theta_v": 90.0, "phi_v": 90.0}

		# Stockage des maillages dynamiques pour les modifier sur place
		self.meshes = {}
		self._init_scene()
		self._init_dynamic_actors()
		self._init_sliders()

	def _sph_to_cart(self, theta_deg, phi_deg):
		t, p = np.radians(theta_deg), np.radians(phi_deg)
		return np.array([np.sin(p) * np.cos(t), np.sin(p) * np.sin(t), np.cos(p)])

	def _make_arrow(self, vec):
		norm = float(np.linalg.norm(vec))
		if norm < 1e-3:
			# Maillage quasi invisible si le vecteur est nul
			return pv.Sphere(radius=0.001)
		return pv.Arrow(
			start=(0.0, 0.0, 0.0),
			direction=vec,
			scale=norm,
			tip_length=0.18 / norm if norm > 0.2 else 0.3,
			tip_radius=0.045 / norm,
			shaft_radius=0.018 / norm,
		)

	def _make_right_angle(self, u, v, size=0.15):
		nu, nv = np.linalg.norm(u), np.linalg.norm(v)
		if nu < 0.05 or nv < 0.05:
			return pv.Sphere(radius=0.001)
		ua, va = u / nu, v / nv
		pts = np.array([size * ua, size * (ua + va), size * va])
		return pv.MultipleLines(points=pts)

	def _init_scene(self):
		sphere = pv.Sphere(radius=1.0, theta_resolution=40, phi_resolution=40)
		self.plotter.add_mesh(
			sphere, color="#4C78A8", opacity=0.18, smooth_shading=True
		)
		self.plotter.add_axes()
		self.plotter.show_bounds(bounds=[-1.1, 1.1, -1.1, 1.1, -1.1, 1.1], grid="back")

	def _init_dynamic_actors(self):
		# Création initiale des objets vides qui seront remplis par update()
		self.meshes["u"] = pv.PolyData()
		self.meshes["v"] = pv.PolyData()
		self.meshes["w"] = pv.PolyData()
		self.meshes["angle_uw"] = pv.PolyData()
		self.meshes["angle_vw"] = pv.PolyData()

		self.update()

		self.plotter.add_mesh(
			self.meshes["u"], color="#EF553B", smooth_shading=True, label="U"
		)
		self.plotter.add_mesh(
			self.meshes["v"], color="#00CC96", smooth_shading=True, label="V"
		)
		self.plotter.add_mesh(
			self.meshes["w"], color="#636EFA", smooth_shading=True, label="U × V"
		)
		self.plotter.add_mesh(self.meshes["angle_uw"], color="#EF553B", line_width=3)
		self.plotter.add_mesh(self.meshes["angle_vw"], color="#00CC96", line_width=3)
		self.plotter.add_legend(bcolor="white", face="circle")

	def update(self):
		u = self._sph_to_cart(self.angles["theta_u"], self.angles["phi_u"])
		v = self._sph_to_cart(self.angles["theta_v"], self.angles["phi_v"])
		w = np.cross(u, v)

		# Mise à jour sur place en mémoire GPU/VTK (ultra-rapide)
		self.meshes["u"].copy_from(self._make_arrow(u))
		self.meshes["v"].copy_from(self._make_arrow(v))
		self.meshes["w"].copy_from(self._make_arrow(w))
		self.meshes["angle_uw"].copy_from(self._make_right_angle(u, w))
		self.meshes["angle_vw"].copy_from(self._make_right_angle(v, w))

	def _init_sliders(self):
		configs = [
			("theta_u", "Azimut U (°)", 0, 360, (0.03, 0.88), (0.25, 0.88), "#EF553B"),
			("phi_u", "Polaire U (°)", 0, 180, (0.03, 0.76), (0.25, 0.76), "#EF553B"),
			("theta_v", "Azimut V (°)", 0, 360, (0.03, 0.60), (0.25, 0.60), "#00CC96"),
			("phi_v", "Polaire V (°)", 0, 180, (0.03, 0.48), (0.25, 0.48), "#00CC96"),
		]

		for key, title, vmin, vmax, p_a, p_b, color in configs:

			def make_callback(k):
				def callback(value):
					self.angles[k] = value
					self.update()

				return callback

			self.plotter.add_slider_widget(
				callback=make_callback(key),
				rng=[vmin, vmax],
				value=self.angles[key],
				title=title,
				pointa=p_a,
				pointb=p_b,
				style="modern",
				color=color,
				title_height=0.02,
				tube_width=0.004,
				slider_width=0.015,
				interaction_event="always",
			)

	def show(self):
		self.plotter.show()


if __name__ == "__main__":
	app = InteractiveSpherePV()
	app.show()
