#!/usr/bin/env python3


def Vector(*args, is_unit=False):
	if len(args) == 3 and all(isinstance(a, (int, float)) for a in args):
		from geometrik.threed.vector.numeric import NumVector

		return NumVector(*args, is_unit=is_unit)

	from geometrik.threed.vector.symbolic import SymVector

	if len(args) == 1 and isinstance(args[0], str):
		return SymVector.symbol(args[0], is_unit=is_unit)
	if len(args) == 3:
		return SymVector(*args, is_unit=is_unit)

	raise TypeError("Constructeur invalide")
