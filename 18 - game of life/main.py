import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

# True means on, False means off.
class LightGrid(object):
	def __init__(self, width, height, input_lines = None):
		self.width = width
		self.height = height
		self.lights = []
		if input_lines is None:
			for _ in range(height):
				self.lights.append([False] * width)
		else:
			for line in input_lines:
				row_of_lights = map(lambda x: x == '#', list(line))
				self.lights.append(row_of_lights)

	def turn_on(self, x, y):
		self.lights[y][x] = True

	def turn_off(self, x, y):
		self.lights[y][x] = False

	def turn_corners_on(self):
		self.turn_on(0, 0)
		self.turn_on(self.width - 1, 0)
		self.turn_on(0, self.height - 1)
		self.turn_on(self.width - 1, self.height - 1)

	def num_on(self):
		return sum([row.count(True) for row in self.lights])

	def is_on(self, x, y):
		if x < 0 or x >= self.width or y < 0 or y >= self.height:
			return False
		return self.lights[y][x]

	def num_live_neighbors(self, x, y):
		count = 0
		for (dx, dy) in ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)):
			if self.is_on(x + dx, y + dy):
				count += 1
		return count
		
	def next_iteration(self):
		new_lights = LightGrid(self.width, self.height)
		for y in range(self.height):
			for x in range(self.width):
				# A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
				# A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
				live_neighbors = self.num_live_neighbors(x, y)
				if self.is_on(x, y):
					if live_neighbors in (2, 3): new_lights.turn_on(x, y)
				else:
					if live_neighbors == 3: new_lights.turn_on(x, y)
		return new_lights
	
def solve(should_force_corners_on):
	lights = LightGrid(100, 100, get_input_lines())
	if should_force_corners_on: lights.turn_corners_on()
	for _ in range(100):
		lights = lights.next_iteration()
		if should_force_corners_on: lights.turn_corners_on()
	return lights.num_on()

print('Part 1: num lights on is {}.'.format(solve(False)))
print('Part 2: num lights on is {}.'.format(solve(True)))
