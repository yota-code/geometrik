#!/usr/bin/env python3

from geometrik.threed.vector import Vector


def test_init_and_conversions():
	u = Vector("u")
	assert len(u) == 3
	assert u.as_vector is u
	assert u.as_tuple == (u.x, u.y, u.z)
	assert u.as_list == [u.x, u.y, u.z]


def test_arithmetic_operations():
	u = Vector("u")
	v = Vector("v")

	assert (u + v).as_tuple == (u.x + v.x, u.y + v.y, u.z + v.z)
	assert (-u).as_tuple == (-u.x, -u.y, -u.z)
	assert (u - v).as_tuple == (u.x - v.x, u.y - v.y, u.z - v.z)
	assert u.lambda_product(2).as_tuple == (2 * u.x, 2 * u.y, 2 * u.z)


def test_scalar_and_vector_product():
	u = Vector("u")
	v = Vector("v")

	assert u.scalar_product(v) == u.x * v.x + u.y * v.y + u.z * v.z
	assert (u @ v).as_tuple == (
		u.y * v.z - u.z * v.y,
		u.z * v.x - u.x * v.z,
		u.x * v.y - u.y * v.x,
	)


def test_norm_and_normalized():
	u = Vector("u")

	assert u.norm_2 == u.x**2 + u.y**2 + u.z**2
	assert u.norm == u.m.sqrt(u.norm_2)
	assert u.normalized().norm == 1
