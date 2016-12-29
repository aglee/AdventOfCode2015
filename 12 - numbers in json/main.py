import inspect
import os
import re
import json

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

def sum_from_obj(obj):
	if type(obj) == type({0:0}):
		if "red" in obj.values():
			return 0
		sum = 0
		for v in obj.values():
			sum += sum_from_obj(v)
		return sum
	elif type(obj) == type([]):
		sum = 0
		for v in obj:
			sum += sum_from_obj(v)
		return sum
	elif type(obj) == type(1):
		return obj
	else:
		return 0

def solve1():
	total = 0
	for line in get_input_lines():
		total += sum(map(int, re.findall('-?[0-9]+', line)))
	print('Part 1: total of numbers found in input is {}.'.format(total))

def solve2():
	total = 0
	for line in get_input_lines():
		obj = json.loads(line)
		total += sum_from_obj(obj)
	print('Part 2: total of non-red numbers found in input is {}.'.format(total))

solve1()
solve2()
