import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

def move(point, c):
	(x, y) = point
	if c == '<': point = (x - 1, y)
	elif c == '>': point = (x + 1, y)
	elif c == '^': point = (x, y + 1)
	elif c == 'v': point = (x, y - 1)
	else:
		print('Unexpected character "{}"'.format(c))
		exit()
	return point


def solve1(route):
	santa_point = (0, 0)
	visited = set([santa_point])
	for c in route:
		santa_point = move(santa_point, c)
		visited.add(santa_point)
	print('Part 1: {} houses get presents.'.format(len(visited)))

def solve2(route):
	santa_point = robo_santa_point = (0, 0)
	visited = set([santa_point])
	for (i, c) in enumerate(route):
		if i % 2 == 0:
			santa_point = move(santa_point, c)
			visited.add(santa_point)
		else:
			robo_santa_point = move(robo_santa_point, c)
			visited.add(robo_santa_point)
	print('Part 2: {} houses get presents.'.format(len(visited)))

route = get_input_lines()[0]
solve1(route)
solve2(route)
