Oui, VTK est clairement un canon pour tuer une mouche si vous vous arrêtez à 3 vecteurs, même s'il devient vite rentable dès que vous ajoutez des champs vectoriels, des surfaces de niveau ou des trajectoires complexes sur votre sphère.
Quant à Trame, c'est un framework open-source en pur Python créé par Kitware (les développeurs de VTK et ParaView) qui permet de transformer n'importe quel script VTK ou PyVista en une application web interactive sans écrire une seule ligne de JavaScript ou de HTML.

Comment fonctionne Trame sous le capot ?

Lorsque vous utilisez PyVista dans un environnement web comme marimo ou Jupyter, Trame joue le rôle de traducteur temps réel entre votre noyau Python et Firefox :
• Synchronisation bidirectionnelle via WebSocket. Trame maintient un canal ouvert en permanence entre Python et votre navigateur. Dès qu'une variable change en Python, l'état est poussé vers l'interface web, et inversement.
• Intégration de vtk.js et Vuetify. Il pilote automatiquement la bibliothèque WebGL vtk.js pour afficher la scène 3D dans le navigateur, et utilise les composants graphiques Vuetify (boutons, menus, barres d'outils) pour l'habillage autour de la vue 3D.
• Deux modes de calcul au choix. Comme vu précédemment, Trame sait basculer à la volée entre le rendu local dans Firefox (Python envoie uniquement la géométrie 3D) et le rendu distant (votre GPU sous Manjaro calcule l'image et streame le flux vidéo vers le navigateur).

Si VTK/PyVista vous semble trop lourd pour la suite

Si vous trouvez la dépendance VTK (~100 à 200 Mo installés) disproportionnée et que vous cherchez une alternative beaucoup plus légère offrant une vraie fenêtre OpenGL native hors navigateur sous Manjaro :
• VisPy : Bibliothèque scientifique Python ultra-légère bâtie directement sur OpenGL moderne (shaders). Idéale pour afficher des milliers de vecteurs ou de points à 60 FPS sans l'usine à gaz VTK, mais son intégration dans marimo est plus rudimentaire.
• Matplotlib : Déjà installé partout, fenêtre Qt/GTK native sous Manjaro, intégration mo.mpl.interactive() directe dans marimo, mais rendu 3D logiciel lent et gestion parfois capricieuse des superpositions en profondeur.
Si vous souhaitez tester VisPy pour une alternative ultra-légère en fenêtre native, ou si vous préférez rester sur PyVista pour préparer vos calculs complexes de demain, dites-moi ce que vous envisagez comme prochains objets géométriques sur la sphère.

VisPy est effectivement une excellente piste pour la fluidité OpenGL pure, mais pour une approche « GeoGebra 3D » orientée géométrie analytique et euclidienne, K3D-jupyter ou pythreejs (ou encore Manim en mode interactif OpenGL) correspondent souvent mieux à la manipulation d'objets géométriques purs.

Ce qu'il faut savoir avant de plonger dans VisPy

• Philosophie « bas niveau » orientée données. VisPy est conçu à l'origine pour afficher des millions de points ou des signaux temps réel directement sur la carte graphique via des shaders GLSL. Contrairement à GeoGebra, il ne possède pas de primitives géométriques haut niveau intégrées (pas d'objet « flèche 3D », « arc de cercle » ou « plan » prêt à l'emploi : il faut construire soi-même les triangles des cônes et les lignes).
• Intégration dans marimo. VisPy s'exécute à merveille dans une fenêtre native (PyQt6/PySide6 ou GLFW) sous Manjaro, mais son intégration dans un notebook marimo nécessite de passer par un backend WebGL expérimental (vispy.app.use_app('jupyter_rfb')), nettement moins mature que Plotly ou PyVista.

Les alternatives les plus proches d'un « GeoGebra 3D » en Python

Si votre besoin principal est la géométrie dans l'espace (plans, intersections, angles, projections, sphères, arcs) plutôt que la simulation physique lourde :

Outil	Esprit « GeoGebra 3D »	Fenêtre native (hors navigateur)	Intégration dans marimo
VisPy	Faible (très orienté shaders et nuages de points bruts).	Excellente (OpenGL pur très léger).	Moyenne (via jupyter_rfb).
Manim (OpenGL)	Très fort. Primitives géométriques riches (vecteurs, angles, arcs, plans, transformations).	Oui (fenêtre interactive Pyglet/OpenGL).	Moyenne (export vidéo/image ou fenêtre externe).
K3D-jupyter / pythreejs	Bon (moteur Three.js léger, vecteurs, maillages, texte LaTeX 3D).	Non (web uniquement).	Bonne (via anywidget / widgets).
PyVista	Bon (primitives prêtes : Arrow, Disc, Arc, Plane, intersections booléennes).	Excellente (VTK/OpenGL).	Bonne (via trame).


Un détail utile si vous gardez PyVista pour la géométrie

Même s'il vient du monde de la physique, PyVista embarque déjà presque toutes les primitives géométriques d'un GeoGebra 3D sans que vous ayez à coder les maillages à la main : pv.CircularArc() pour vos angles entre vecteurs, pv.Plane() ou pv.Disc() pour le plan engendré par \(\vec{u}\) et \(\vec{v}\), et pv.Text3D() pour annoter vos figures.
Si vous testez VisPy, souhaitez-vous que je vous fournisse le squelette minimal pour dessiner une sphère filaire et des vecteurs avec vispy.scene (afin de vous éviter la configuration des caméras et shaders de départ) ?
