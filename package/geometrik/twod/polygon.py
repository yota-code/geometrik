#!/usr/bin/env python3

class Polygon() :
	def __init__(self, * p_lst) :
		self.p_lst = list(p_lst)

	def _trapezoid_area(self, p0, p1) :
		return (p1[0] - p0[0]) * (p0[1] + p1[1]) / 2

	def area(self) :
		return sum(self._trapezoid_area(self.p_lst[i], self.p_lst[(i + 1) % len(self.p_lst)]) for i in range(len(self.p_lst)))

if __name__ == '__main__' :

	right_lst = [
		[1, 1],
		[1, 2],
		[2, 2],
		[2, 1],
	]

	left_lst = [
		[1, 1],
		[2, 1],
		[2, 2],
		[1, 2],
	]

	one_lst = [
		[44.1, 4.75833333333333],
		[44.1, 4.96305555555556],
		[43.9138888888889, 4.99305555555556],
		[43.8166666666667, 4.975],
		[43.8055555555556, 4.84166666666667],
		[43.8166666666667, 4.78055555555556],
		[44.1, 4.75833333333333],
	]

	u = Polygon(* right_lst)
	print(u.area())