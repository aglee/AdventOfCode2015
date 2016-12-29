import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

def parse_input(lines):
	cities = set()
	distances = {}
	for line in lines:
		parts = line.split()
		(city1, city2, dist) = (parts[0], parts[2], int(parts[4]))
		cities.add(city1)
		cities.add(city2)
		distances[(city1, city2)] = dist
		distances[(city2, city1)] = dist
	return (list(cities), distances)

def all_permutations(items):
	if len(items) < 2: return [items]
	
	perms = []
	for i in range(len(items)):
		shorter_list = items[:]
		item = shorter_list.pop(i)
		for shorter_permutation in all_permutations(shorter_list):
			perms.append([item] + shorter_permutation)
	return perms

def total_distance(cities, distances):
	total = 0
	for i in range(len(cities) - 1):
		total += distances[(cities[i], cities[i + 1])]
	return total

def solve1(cities, distances):
	shortest = None
	for seq in all_permutations(cities):
		path_length = total_distance(seq, distances)
		if shortest is None or path_length < shortest:
			shortest = path_length
	print('Part 1: shortest path length is {}.'.format(shortest))

def solve2(cities, distances):
	longest = None
	for seq in all_permutations(cities):
		path_length = total_distance(seq, distances)
		if longest is None or path_length > longest:
			longest = path_length
	print('Part 2: longest path length is {}.'.format(longest))

(cities, distances) = parse_input(get_input_lines())
solve1(cities, distances)
solve2(cities, distances)

