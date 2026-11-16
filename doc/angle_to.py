#!/usr/bin/env python3

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import math

    import marimo as mo
    import sympy
    from geometrik.threed.vector.numeric import NumVector
    from geometrik.threed.vector.symbolic import SymVector

    return NumVector, SymVector, math, mo, sympy


@app.cell
def _(mo):
    mo.md(r"""
    # Documentation de `angle_to()`

    La méthode `angle_to(other, way=None)` calcule l'angle (en radians) entre deux vecteurs `self` ($\vec{u}$) et `other` ($\vec{v}$) :

    - **Sans vecteur de référence (`way=None`)** : angle non orienté dans $[0, \pi]$.
    - **Avec vecteur de référence (`way` fourni)** : angle orienté dans $[-\pi, \pi]$, dont le signe est donné par le produit mixte $(\vec{u} \wedge \vec{v}) \cdot \vec{w}$.
    """)
    return


@app.cell
def _(SymVector, mo, sympy):
    u_sym = SymVector.symbol("u")
    v_sym = SymVector.symbol("v")
    w_sym = SymVector.symbol("w")

    angle_unoriented = u_sym.angle_to(v_sym)
    angle_oriented = u_sym.angle_to(v_sym, way=w_sym)

    u_unit_sym = SymVector.symbol("u", is_unit=True)
    v_unit_sym = SymVector.symbol("v", is_unit=True)
    angle_unit_sym = u_unit_sym.angle_to(v_unit_sym)
    angle_unit_oriented_sym = u_unit_sym.angle_to(v_unit_sym, way=w_sym)

    mo.md(
    	f"""
    	## 1. Résolution littérale (`SymVector`)

    	Soient $\\vec{{u}} = ({sympy.latex(u_sym.x)}, {sympy.latex(u_sym.y)}, {sympy.latex(u_sym.z)})$,
    	$\\vec{{v}} = ({sympy.latex(v_sym.x)}, {sympy.latex(v_sym.y)}, {sympy.latex(v_sym.z)})$
    	et un vecteur d'orientation $\\vec{{w}} = ({sympy.latex(w_sym.x)}, {sympy.latex(w_sym.y)}, {sympy.latex(w_sym.z)})$.

    	### Cas général
    	- **Angle non orienté** :
    	$$\\theta = \\arccos\\left(\\frac{{\\vec{{u}} \\cdot \\vec{{v}}}}{{\\|\\vec{{u}}\\| \\, \\|\\vec{{v}}\\|}}\\right) = {sympy.latex(angle_unoriented)}$$

    	- **Angle orienté selon $\\vec{{w}}$** :
    	$$\\theta_{{\\vec{{w}}}} = \\operatorname{{signe}}\\big((\\vec{{u}} \\wedge \\vec{{v}}) \\cdot \\vec{{w}}\\big)\\,\\theta = {sympy.latex(angle_oriented)}$$

    	### Cas de vecteurs unitaires (`is_unit=True`, $\\|\\vec{{u}}\\| = \\|\\vec{{v}}\\| = 1$)
    	- **Angle non orienté** :
    	$$\\theta = {sympy.latex(angle_unit_sym)}$$

    	- **Angle orienté selon $\\vec{{w}}$** :
    	$$\\theta_{{\\vec{{w}}}} = {sympy.latex(angle_unit_oriented_sym)}$$
    	"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Illustration numérique interactive (`NumVector`, vecteurs unitaires)

    Modifiez les angles sphériques (azimut $\phi$ et élévation $\theta$) des vecteurs $\vec{u}$ et $\vec{v}$ — automatiquement unitaires — ainsi que l'axe d'orientation $\vec{w}$.
    """)
    return


@app.cell
def _(mo):
    u_az = mo.ui.slider(-180, 180, value=0, step=5, label="u : azimut (°)")
    u_el = mo.ui.slider(-90, 90, value=0, step=5, label="u : élévation (°)")

    v_az = mo.ui.slider(-180, 180, value=90, step=5, label="v : azimut (°)")
    v_el = mo.ui.slider(-90, 90, value=0, step=5, label="v : élévation (°)")

    use_way = mo.ui.checkbox(
    	value=True, label="Utiliser un vecteur d'orientation `way`"
    )
    way_choice = mo.ui.dropdown(
    	options={
    		"Z+ (0, 0, 1)": (0.0, 0.0, 1.0),
    		"Z- (0, 0, -1)": (0.0, 0.0, -1.0),
    		"Y+ (0, 1, 0)": (0.0, 1.0, 0.0),
    		"X+ (1, 0, 0)": (1.0, 0.0, 0.0),
    	},
    	value="Z+ (0, 0, 1)",
    	label="Vecteur `way`",
    )

    mo.hstack(
    	[
    		mo.vstack([u_az, u_el]),
    		mo.vstack([v_az, v_el]),
    		mo.vstack([use_way, way_choice]),
    	],
    	justify="space-around",
    )
    return u_az, u_el, use_way, v_az, v_el, way_choice


@app.cell
def _(NumVector, math, mo, u_az, u_el, use_way, v_az, v_el, way_choice):
    def unit_from_angles(az_deg: float, el_deg: float) -> NumVector:
    	az = math.radians(az_deg)
    	el = math.radians(el_deg)
    	return NumVector(
    		math.cos(el) * math.cos(az),
    		math.cos(el) * math.sin(az),
    		math.sin(el),
    	).normalized()

    u_num = unit_from_angles(u_az.value, u_el.value)
    v_num = unit_from_angles(v_az.value, v_el.value)
    w_num = NumVector(*way_choice.value, is_unit=True) if use_way.value else None

    dot_uv = u_num * v_num
    cross_uv = u_num @ v_num
    angle_rad = u_num.angle_to(v_num, way=w_num)
    angle_deg = math.degrees(angle_rad)

    if w_num is not None:
    	triple = cross_uv * w_num
    	orientation_info = (
    		f"- **Vecteur `way`** : `{w_num}`\n"
    		f"- **Produit mixte $(\\vec{{u}} \\wedge \\vec{{v}}) \\cdot \\vec{{w}}$** : `{triple:.4f}`"
    	)
    else:
    	orientation_info = (
    		"- **Mode** : non orienté (`way=None`, résultat dans $[0, \\pi]$)"
    	)

    mo.md(
    	f"""
    	### Résultats (`NumVector.angle_to`)

    	- $\\vec{{u}}$ (unitaire, $\\|\\vec{{u}}\\| = {u_num.norm:.3f}$) : `{u_num}`
    	- $\\vec{{v}}$ (unitaire, $\\|\\vec{{v}}\\| = {v_num.norm:.3f}$) : `{v_num}`
    	- **Produit scalaire $\\vec{{u}} \\cdot \\vec{{v}}$** : `{dot_uv:.4f}`
    	- **Produit vectoriel $\\vec{{u}} \\wedge \\vec{{v}}$** : `{cross_uv}`
    	{orientation_info}

    	> **Angle calculé** : `{angle_rad:.4f} rad` (**`{angle_deg:.2f}°`**)
    	"""
    )
    return


@app.cell
def _():


    return


@app.cell
def _(mo):
    import numpy as np
    import plotly.graph_objects as go

    # debounce=True permet de ne mettre à jour la figure que lorsqu'on relache le slider

    # Curseurs pour le Vecteur U (angles en degrés pour plus de lisibilité)
    theta_u = mo.ui.slider(0, 360, value=0, step=5, label="θ_u (Azimut °)")
    phi_u = mo.ui.slider(0, 180, value=90, step=5, label="φ_u (Polaire °)")

    # Curseurs pour le Vecteur V
    theta_v = mo.ui.slider(0, 360, value=90, step=5, label="θ_v (Azimut °)")
    phi_v = mo.ui.slider(0, 180, value=90, step=5, label="φ_v (Polaire °)")

    # Affichage groupé des curseurs côte à côte
    mo.hstack([
        mo.vstack([mo.md("**Vecteur U (Rouge)**"), theta_u, phi_u]),
        mo.vstack([mo.md("**Vecteur V (Vert)**"), theta_v, phi_v])
    ])
    return go, np, phi_u, phi_v, theta_u, theta_v


@app.cell
def _(go, mo, np, phi_u, phi_v, theta_u, theta_v):
    # Fonction utilitaire pour convertir les angles en vecteur unitaire 3D
    def sph_to_cart(theta_deg, phi_deg):
        t = np.radians(theta_deg)
        p = np.radians(phi_deg)
        return np.array([
            np.sin(p) * np.cos(t),
            np.sin(p) * np.sin(t),
            np.cos(p)
        ])

    # 1. Calcul des deux vecteurs dynamiques
    u = sph_to_cart(theta_u.value, phi_u.value)
    v = sph_to_cart(theta_v.value, phi_v.value)

    # 2. Calcul du troisième vecteur (Produit vectoriel U x V)
    w = np.cross(u, v)
    norme_w = np.linalg.norm(w)

    # 3. Construction de la scène 3D
    fig = go.Figure()

    # Sphère unité transparente
    t_grid = np.linspace(0, 2 * np.pi, 40)
    p_grid = np.linspace(0, np.pi, 40)
    fig.add_trace(go.Surface(
        x=np.outer(np.cos(t_grid), np.sin(p_grid)),
        y=np.outer(np.sin(t_grid), np.sin(p_grid)),
        z=np.outer(np.ones(40), np.cos(p_grid)),
        opacity=0.15,
        colorscale="Blues",
        showscale=False,
        hoverinfo="skip"
    ))

    def ajouter_angle_droit(vec_a, vec_b, taille=0.12, couleur="gray"):
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
    
        # On n'affiche rien si l'un des vecteurs est quasi nul (cas u et v colinéaires)
        if norm_a < 0.05 or norm_b < 0.05:
            return
        
        # Normalisation pour garantir un carré parfait quelle que soit la longueur de w
        a_unit = vec_a / norm_a
        b_unit = vec_b / norm_b
    
        # Calcul des 3 points du coin (P1 -> P2 -> P3)
        p1 = taille * a_unit
        p2 = taille * (a_unit + b_unit)
        p3 = taille * b_unit
    
        pts = np.array([p1, p2, p3])
    
        fig.add_trace(go.Scatter3d(
            x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
            mode="lines",
            line=dict(color=couleur, width=3),
            showlegend=False,
            hoverinfo="skip"
        ))

    # Fonction d'aide pour ajouter un vecteur (tige + pointe)
    def ajouter_vecteur(vec, nom, couleur):
        norme = np.linalg.norm(vec)
        # Tige
        fig.add_trace(go.Scatter3d(
            x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]],
            mode="lines+markers",
            marker=dict(size=[3, 5], color=couleur),
            line=dict(color=couleur, width=6),
            name=f"{nom} (‖{norme:.2f}‖)"
        ))
        # Pointe (affichée uniquement si le vecteur n'est pas nul)
        if norme > 0.05:
            fig.add_trace(go.Cone(
                x=[vec[0]], y=[vec[1]], z=[vec[2]],
                u=[vec[0]], v=[vec[1]], w=[vec[2]],
                sizemode="absolute",
                sizeref=0.12,
                anchor="tip",
                colorscale=[[0, couleur], [1, couleur]],
                showscale=False,
                hoverinfo="skip"
            ))

    ajouter_vecteur(u, "Vecteur U", "#EF553B")          # Rouge
    ajouter_vecteur(v, "Vecteur V", "#00CC96")          # Vert
    ajouter_vecteur(w, "Produit U × V", "#636EFA")      # Bleu

    # Ajout des deux marqueurs d'angle droit au pied des vecteurs
    ajouter_angle_droit(u, w, taille=0.15, couleur="#EF553B")  # Angle droit entre U et W
    ajouter_angle_droit(v, w, taille=0.15, couleur="#00CC96")  # Angle droit entre V et W


    # Réglages de la caméra et des proportions
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1.2, 1.2], title="X"),
            yaxis=dict(range=[-1.2, 1.2], title="Y"),
            zaxis=dict(range=[-1.2, 1.2], title="Z"),
            aspectmode="cube",
            uirevision="constant"  # Conserve l'angle de vue quand on bouge les curseurs !
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.05)
    )

    mo.ui.plotly(fig)
    return


if __name__ == "__main__":
    app.run()
