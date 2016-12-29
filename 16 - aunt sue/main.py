import inspect
import os
import re

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

detected_data = {
	"children": 3,
	"cats": 7,
	"samoyeds": 2,
	"pomeranians": 3,
	"akitas": 0,
	"vizslas": 0,
	"goldfish": 5,
	"trees": 3,
	"cars": 2,
	"perfumes": 1
}

def aunt_matches_part_1(aunt):
	for (k, v) in aunt.iteritems():
		if v != detected_data.get(k): return False
	return True

def aunt_matches_part_2(aunt):
	for (k, v) in aunt.iteritems():
		detected_value = detected_data.get(k)
		if detected_value is None:
			return False
		elif k in ('cats', 'trees'):
			if v <= detected_value:
				return False
		elif k in ('pomeranians', 'goldfish'):
			if v >= detected_value:
				return False
		elif v != detected_value:
			return False
	return True

all_aunts = []
for line in get_input_lines():
	aunt = {}
	# E.g. "Sue 1: goldfish: 9, cars: 0, samoyeds: 9".
	for match in re.findall('([a-z]+): ([0-9]+)', line):
		aunt[match[0]] = int(match[1])
	all_aunts.append(aunt)

def solve1():
	for (i, aunt) in enumerate(all_aunts):
		if aunt_matches_part_1(aunt):
			# The problem statement uses 1-based indexes for the aunt, hence "+ 1".
			print('Part 1: The aunt number is {}.'.format(i + 1))
			return
	print('ERROR: solve1() found no solution.')

def solve2():
	for (i, aunt) in enumerate(all_aunts):
		if aunt_matches_part_2(aunt):
			# The problem statement uses 1-based indexes for the aunt, hence "+ 1".
			print('Part 2: The aunt number is {}.'.format(i + 1))
			return
	print('ERROR: solve2() found no solution.')

solve1()
solve2()




