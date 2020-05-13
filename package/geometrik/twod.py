#!/usr/bin/env python3

from __future__ import annotations

import math
import cmath

template_svg = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet href="style.css" type="text/css"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="{viewbox}" version="1.1">
{content}
</svg>
'''

class _common_Point_Vector() :
	def __init__(self, x, y) :
		self.x = x
		self.y = y

	@property
	def param(self) :
		return self.x, self.y

	@property
	def as_complex(self) :
		return complex(self.x, self.y)
		
	@property
	def phase(self) :
		return cmath.phase(self.as_complex)

class Point(_common_Point_Vector) :
	def dist(self, other: Point) :
		return math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 )

	def __repr__(self) :
		return f"Point({self.x:0.3g}, {self.y:0.3g})"

	def projection(self, line: Line) :
		op = Vector.from_2_Point(line.b, self)
		k = (op * line.a) / (line.a.norm_2)
		return line.b + k * line.a

	def __add__(self, other) :
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other) :
		return Point(self.x - other.x, self.y - other.y)

	def _to_path(self) :
		return f"M {self.x:0.3f},{self.y:0.3f}"	
		
class Vector(_common_Point_Vector) :
	""" floating vector class """

	def __repr__(self) :
		return f"Vector({self.x:0.3g}, {self.y:0.3g})"

	@property
	def norm_2(self) :
		return (self.x)**2 + (self.y)**2

	@property
	def norm(self) :
		return math.sqrt( (self.x)**2 + (self.y)**2 )
		
	@staticmethod
	def from_2_Point(a: Point, b: Point) :
		return Vector(b.x - a.x, b.y - a.y)

	def normalized(self) :
		d = self.norm
		return Vector(self.x / d, self.y / d)

	def __neg__(self) :
		return Vector(-1 * self.x, -1 * self.y)

	def __matmul__(self, other) :
		return self.x*other.y - self.y*other.x

	def __mul__(self, other) :
		if isinstance(other, Vector) :
			return self.x*other.x + self.y*other.y
		else :
			return Vector(other * self.x, other * self.y)

	__rmul__ = __mul__

	def __add__(self, other) :
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other) :
		return Vector(self.x - other.x, self.y - other.y)

class Polyline() :
	def __init__(self, p_lst, is_closed=False) :
		self.p_lst = p_lst
		self.is_closed = is_closed
		
	def _to_svg(self) :
		return '<{0} points="{1}" />'.format(
			"polygon" if self.is_closed else "polyline",
			' '.join(f"{p.x:.3f},{p.y:.3f}" for p in self.p_lst)
		)

class Line() :
	""" defined as a colinear vector and a point,
	which is equivalent to a parametric line 
	"""
	def __init__(self, a: Vector, b: Point) :
		self.a = a # a vector colinear to the line
		self.b = b # a point by which the line pass through

	def __repr__(self) :
		return f"Line({self.a}, {self.b})"

	def determinant(self) :
		pass

	@property
	def get_affine_coef(self) :
		m = self.a.y / self.a.x
		p = self.b.y - self.b.x * m
		return m, p

	def debug_affine(self) :
		m, p = self.get_affine_coef
		return f"y = {m} * x + {p}"

	def debug_parametric(self) :
		return f"x(t) = {self.a.x} * t + {self.b.x}\ny(t) = {self.a.y} * t + {self.b.y}"

	@property
	def get_canonical_coef(self) :
		a = self.a.y
		b = -self.a.x
		c = self.a.x * self.b.y - self.a.y * self.b.x
		return a, b, c

	def debug_canonical(self) :
		a, b, c = self.get_canonical_coef
		return f"{a} * x + {b} * y + {c} = 0"

	def intersection_with_line(self, other) :
		# print(f">>> intersection({self.debug_canonical()}, {other.debug_canonical()}")
		a1, b1, c1 = self.get_canonical_coef
		a2, b2, c2 = other.get_canonical_coef

		d = a1*b2 - a2*b1

		if d != 0 :
			y = ( a2*c1 - a1*c2 ) / d
			x = ( b1*c2 - c1*b2 ) / d
			return Point(x, y)

		return None

	def intersection_with_circle(self, other: Circle) -> (Point, Point) :
		# https://mathworld.wolfram.com/Circle-LineIntersection.html
		# first, lets check the line can intersect

		p1 = self.b - other.c
		p2 = self.a + self.b - other.c

		cx, cy, r = other.param

		dx = p2.x - p1.x
		dy = p2.y - p1.y
		dr = dx**2 + dy**2
		dn = p1.x*p2.y - p2.x*p1.y

		dd = r**2 * dr - dn**2

		if 0 <= dd :
			sign_dy = math.copysign(1.0, dy)
			x1 = ( dn*dy + sign_dy*dx * math.sqrt(dd) ) / dr + cx
			x2 = ( dn*dy - sign_dy*dx * math.sqrt(dd) ) / dr + cx
			y1 = ( -dn*dx + abs(dy)*math.sqrt(dd) ) / dr + cy
			y2 = ( -dn*dx - abs(dy)*math.sqrt(dd) ) / dr + cy
			return Point(x1, y1), Point(x2, y2)
		else :
			return None, None
		
	def value_at_time(self, t: float) :
		x = (self.a.x * t) + (self.b.x)
		y = (self.a.y * t) + (self.b.y)
		return Point(x, y)

	@staticmethod
	def from_2_Point(p1: Point, p2: Point) :
		""" return a Line which pass through two points """
		return Line(
			Vector.from_2_Point(p1, p2),
			p1
		)

	@staticmethod
	def from_originPoint_normalVector(origin: Point, normal: Vector) :
		""" return a Line defined by a point it passes through and a normal vector """
		return Line(
			Vector( -normal.y, normal.x ),
			origin
		)
		
class Segment() :
	""" define a segment between A and B, the segment is oriented """
	def __init__(self, a: Point, b: Point) :
		self.a = a
		self.b = b

	def __repr__(self) :
		return f"Segment({self.a}, {self.b})"

	def get_point_at(self, i) :
		""" i must be in [0.0 ; 1.0] """
		return Point(
			(1.0 - i) * self.a.x + i * self.b.x,
			(1.0 - i) * self.a.y + i * self.b.y,
		)

		
	def _to_svg(self) :
		return f'<line x1="{self.a.x:.3f}" y1="{self.a.y:.3f}" x2="{self.b.x:.3f}" y2="{self.b.y:.3f}" />'

	def _to_path(self, standalone=True) :
		return ( f"M {self.a.x},{self.a.y} " if standalone else '') + f"L {self.b.x:0.3f},{self.b.y:0.3f}"

	@property
	def as_vector(self) :
		return Vector.from_2_Point(self.a, self.b)

	@property
	def reversed(self) :
		return Segment(self.b, self.a)

class Circle() :
	def __init__(self, c: Point, r: float) :
		self.c = c # center as Point()
		self.r = r # radius as float()

	def is_inside(self, p: Point, strict=False) :
		""" return True if the point p is inside the circle """
		cp = Vector(self.c, p)
		if strict :
			return len(cp) < self.r
		else :
			return len(cp) <= self.r

	@property
	def param(self) :
		return self.c.x, self.c.y, self.r
		
	def outside_tangent(self, other) :
		""" return the two segments which form the tangent to the two circles self and other """
		
		gamma = ab.phase
		delta = math.asin((other.r - self.r) / len(ab))

		q = math.pi / 2

		return (
			Segment(
				Point(self.c.x + math.cos(gamma - delta - q) * self.r, self.c.y + math.sin(gamma - delta - q) * self.r),
				Point(other.c.x + math.cos(gamma - delta - q) * other.r, other.c.y + math.sin(gamma - delta - q) * other.r)
			), Segment (
				Point(other.c.x + math.cos(gamma + delta + q) * other.r, other.c.y + math.sin(gamma + delta + q) * other.r),
				Point(self.c.x + math.cos(gamma + delta + q) * self.r, self.c.y + math.sin(gamma + delta + q) * self.r)
			)
		)

	def _to_svg(self, style=None) :
		style = '' if style is None else f'class="{style}" '
		return f'<circle {style}cx="{self.c.x}" cy="{self.c.y}" r="{self.r}" />'

	def __repr__(self) :
		return f"Cercle({self.c}, {self.r})"

	@staticmethod
	def from_3_Point(a: Point, b: Point, c: Point) :
		# print(f'>>> Circle.from_3_Point({a}, {b}, {c})')

		s_ab = Segment(a, b)
		s_bc = Segment(b, c)
		
		m_ab = s_ab.get_point_at(0.5)
		m_bc = s_bc.get_point_at(0.5)

		l_ab = Line.from_originPoint_normalVector(m_ab, s_ab.as_vector)
		l_bc = Line.from_originPoint_normalVector(m_bc, s_bc.as_vector)

		o = l_ab.intersection_with_line(l_bc)

		r = o.dist(b)

		return Circle(o, r)

	@staticmethod
	def from_2_Point(a: Point, b: Point, w: float) :
		""" w is the signed inverse of the radius """
		# print(f'>>> Circle.from_3_Point({a}, {b}, {w})')

		if w == 0 :
			return Line.from_2_Point(a, b)

		r = 1/abs(w)
		m = Segment(a, b).get_point_at(0.5)
		line = Line.from_originPoint_normalVector(m, Vector.from_2_Point(a, b))

		circle = Circle(a, r)
		p, q = line.intersection_with_circle(circle) # one point is on the left, one on the right

		ab = Vector.from_2_Point(a, b)
		ap = Vector.from_2_Point(a, p)
		aq = Vector.from_2_Point(a, q)

		if 0 <= w * (ab @ ap) :
			return Circle(q, r)
		else :
			return Circle(p, r)

class Arc() :
	def __init__(self, c, w, start, stop) :
		self.c = c # center as Point()
		self.w = w # curvature as float()
		self.start = start
		self.stop = stop

	@property
	def reversed(self) :
		return Arc(self.c, - self.w, self.stop, self.start)
		
	@staticmethod
	def from_3_Point(a: Point, b: Point, c: Point) :

		tmp = Circle.from_3_Point(a, b, c)
		start = Vector.from_2_Point(tmp.c, a).phase
		stop = Vector.from_2_Point(tmp.c, c).phase

		return Arc(tmp.c, math.copysign(1.0, Vector.from_2_Point(a, b) @ Vector.from_2_Point(b, c)) / tmp.r, start, stop)

	def from_2_Point(a: Point, b: Point, w: float) :
		""" w is the signed inverse of the radius """
		if w == 0 :
			return Segment.from_2_Point(a, b)

		tmp = Circle.from_2_Point(a, b, w)

		start = Vector.from_2_Point(tmp.c, a).phase
		stop = Vector.from_2_Point(tmp.c, b).phase

		return Arc(tmp.c, 1.0 / tmp.r, start, stop)

	def __repr__(self) :
		return f"Arc(center = {self.c}, curvature = {self.w:.3g}, start = {self.start:.3f}, stop = {self.stop:.3f})"

	def get_point_at(self, i) :
		""" i must be in [0.0 ; 1.0] """
		m = (1.0 - i) * self.start + i * self.stop
		return Point(
			self.c.x + math.cos(m) / abs(self.w),
			self.c.y + math.sin(m) / abs(self.w)
		)

	def _to_path(self, standalone=True) :
		m = ( f"M {self.get_point_at(0.0).x},{self.get_point_at(0.0).y} " if standalone else '')
		r = 1 / abs(self.w)
		p = self.get_point_at(1.0)
		return f"A {r:0.3f} {r:0.3f} 0 0 {'1' if 0 < self.w else '0'} {p.x:0.3f} {p.y:0.3f}"

if __name__ == '__main__' :

	import sympy
	from sympy import symbols as sym


	l1 = Line.from_originPoint_normalVector(Point(4,1), Vector(4,-2))
	l2 = Line.from_originPoint_normalVector(Point(1,5), Vector(2,-6))

	print(l1)
	print(l1.debug_canonical())
	print(l2.debug_canonical())

	a1, a2, b1, b2, c1, c2 = sym('a_1 a_2 b_1 b_2 c_1 c_2')
	a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y = sym('a^1_x a^1_y b^1_x b^1_y a^2_x a^2_y b^2_x b^2_y')

	y = (a2*c1 - a1*c2) / (a1*b2 - a2*b1)
	print(sympy.latex(
		y.subs(a1, a1y).subs(a2, a2y).subs(b1, -a1x).subs(b2, -a2x).subs(c1, a1x*b1y - a1y*b1x).subs(c2, a2x*b2y - a2y*b2x))
	)
	print(l1.intersection_with_line(l2))

	sys.exit(0)

	Arc.from_2_Point(Point(-2,2), Point(2,2), 1/5)


	line_o = Line.from_2_Point(Point(-1, 0), Point(5, 3))
	circle_o = Circle(Point(2,2), 1)
	print(line_o)
	print(circle_o)

	line_o.intersection_with_circle(circle_o)



	u = Arc.from_3_Point(
		Point(0, 1),
		Point(1, 0),
		Point(3, 0)
	)
	print(u)

	import sympy

	from sympy import symbols as sym

	x, y, cx, cy, r, a, b, c = sym('x y C_x C_y r a b c')

	line_s = a * x + b * y + c
	circle_s = (x - cx)**2 + (y - cy)**2 - r**2
	
	print(line_s, circle_s)

	u = sympy.solve([circle_s, line_s], [x, y])

	val = {'a': 3, 'b': 6, 'c': 3, 'C_x':2, 'C_y':2, 'r': 1}

	print("x1 =", sympy.latex(u[0][0].expand().simplify()), "=", sympy.latex(u[0][0].subs(val)), "\\\\")
	print("x2 =", sympy.latex(u[1][0].expand().simplify()), "=", sympy.latex(u[1][0].subs(val)), "\\\\")
	print("y1 =", sympy.latex(u[0][1].expand().simplify()), "=", sympy.latex(u[0][1].subs(val)), "\\\\")
	print("y2 =", sympy.latex(u[1][1].expand().simplify()), "=", sympy.latex(u[1][1].subs(val)))


	print(u[0][0].subs(val))
	print(u[0][1].subs(val))
	print(u[1][0].subs(val))
	print(u[1][1].subs(val))

	line_o = Line.from_2_Point(Point(-1, 0), Point(5, 3))
	circle_o = Circle(Point(2,2), 1)

	print(line_o)
	print(line_o.debug_affine())
	print(line_o.debug_canonical())

	line_o.intersection_with_circle(circle_o)
 