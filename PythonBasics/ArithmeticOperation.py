"""Simple arithmetic operations module with a CLI.

Provides: add, subtract, multiply, divide, power, modulo and a small
command-line interface that accepts an operation and one or more numbers.

Usage (examples):
  python ArithmeticOperation.py add 1 2 3
  python ArithmeticOperation.py div 10 2

If no arguments are provided the script runs an interactive prompt.
"""
from __future__ import annotations

import argparse
import functools
import operator
import sys
from typing import Iterable


def add(*values: float) -> float:
	return sum(values)


def subtract(first: float, *rest: float) -> float:
	return functools.reduce(operator.sub, rest, first)


def multiply(*values: float) -> float:
	return functools.reduce(operator.mul, values, 1.0)


def divide(first: float, *rest: float) -> float:
	# sequential division: (((a / b) / c) / ...)
	result = first
	for r in rest:
		if r == 0:
			raise ZeroDivisionError("Division by zero")
		result /= r
	return result


def power(base: float, exponent: float) -> float:
	return base ** exponent


def modulo(a: float, b: float) -> float:
	if b == 0:
		raise ZeroDivisionError("Modulo by zero")
	return a % b


OP_MAP = {
	"add": (add, "Add all numbers"),
	"sub": (subtract, "Subtract subsequent numbers from the first"),
	"mul": (multiply, "Multiply all numbers"),
	"div": (divide, "Sequentially divide the first by the rest"),
	"pow": (power, "Raise first number to the power of the second"),
	"mod": (modulo, "Modulo (remainder) of two numbers"),
}


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
	p = argparse.ArgumentParser(description="Perform simple arithmetic operations")
	p.add_argument("operation", nargs="?", choices=OP_MAP.keys(), help="operation to perform")
	p.add_argument("numbers", nargs="*", help="numbers (one or more)")
	return p.parse_args(list(argv) if argv is not None else None)


def _to_floats(strs: Iterable[str]) -> list[float]:
	nums = []
	for s in strs:
		try:
			if "." in s or "e" in s.lower():
				nums.append(float(s))
			else:
				# allow integers too
				nums.append(int(s))
		except ValueError:
			raise ValueError(f"Invalid numeric value: {s!r}")
	return [float(x) for x in nums]


def main(argv: Iterable[str] | None = None) -> int:
	args = parse_args(argv)
	if not args.operation:
		# interactive mode
		try:
			print("No operation specified. Enter interactive mode.")
			print("Available operations:")
			for k, (_, desc) in OP_MAP.items():
				print(f"  {k}\t- {desc}")
			op = input("Operation: ").strip()
			if op not in OP_MAP:
				print("Unknown operation")
				return 2
			raw = input("Enter numbers separated by space: ").strip().split()
			nums = _to_floats(raw)
		except (KeyboardInterrupt, EOFError):
			print()
			return 0
	else:
		op = args.operation
		if not args.numbers:
			print("Please provide numbers for the operation", file=sys.stderr)
			return 2
		try:
			nums = _to_floats(args.numbers)
		except ValueError as e:
			print(str(e), file=sys.stderr)
			return 2

	func = OP_MAP[op][0]
	try:
		# validate arity for operations that need exactly two args
		if op in ("pow", "mod") and len(nums) != 2:
			print(f"Operation '{op}' requires exactly two numbers", file=sys.stderr)
			return 2
		if op == "sub" and len(nums) < 1:
			print("Subtraction requires at least one number", file=sys.stderr)
			return 2
		if op in ("add", "mul") and len(nums) < 1:
			print(f"Operation '{op}' requires at least one number", file=sys.stderr)
			return 2

		result = func(*nums)
	except ZeroDivisionError as e:
		print(f"Error: {e}", file=sys.stderr)
		return 3
	except Exception as e:
		print(f"Error: {e}", file=sys.stderr)
		return 4

	# print result in a user-friendly way
	# If it's integral, show as int
	if abs(result - round(result)) < 1e-12:
		print(int(round(result)))
	else:
		print(result)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
