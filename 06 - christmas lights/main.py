import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

class LightGrid(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.lights = []
		for _ in range(height):
			self.lights.append([0] * width)

	def toggle_rect(self, x1, y1, x2, y2):
		for row in range(y1, y2 + 1):
			for col in range(x1, x2 + 1):
				self.lights[row][col] = (1 - self.lights[row][col])

	def turn_on_rect(self, x1, y1, x2, y2):
		for row in range(y1, y2 + 1):
			for col in range(x1, x2 + 1):
				self.lights[row][col] = 1

	def turn_off_rect(self, x1, y1, x2, y2):
		for row in range(y1, y2 + 1):
			for col in range(x1, x2 + 1):
				self.lights[row][col] = 0

	def num_on(self):
		return sum([sum(row) for row in self.lights])

	def do_command(self, line):
		parts = line.split()
		(x1, y1) = map(int, parts[-3].split(','))
		(x2, y2) = map(int, parts[-1].split(','))
		if x1 > x2: (x1, x2) = (x2, x1)
		if y1 > y2: (y1, y2) = (y2, y1)
		if parts[0] == 'toggle': self.toggle_rect(x1, y1, x2, y2)
		elif parts[:2] == ['turn', 'on']: self.turn_on_rect(x1, y1, x2, y2)
		elif parts[:2] == ['turn', 'off']: self.turn_off_rect(x1, y1, x2, y2)
		else:
			print('Unexpected input line "{}".'.format(line))
			exit()

class LightGrid2(LightGrid):
	def __init__(self, width, height):
		super(LightGrid2, self).__init__(width, height)

	def toggle_rect(self, x1, y1, x2, y2):
		for row in range(y1, y2 + 1):
			for col in range(x1, x2 + 1):
				self.lights[row][col] += 2

	def turn_on_rect(self, x1, y1, x2, y2):
		for row in range(y1, y2 + 1):
			for col in range(x1, x2 + 1):
				self.lights[row][col] += 1

	def turn_off_rect(self, x1, y1, x2, y2):
		for row in range(y1, y2 + 1):
			for col in range(x1, x2 + 1):
				if self.lights[row][col] > 0:
					self.lights[row][col] -= 1

lines = get_input_lines()

lights = LightGrid(1000, 1000)
for line in lines:
	lights.do_command(line)
print('Part 1: {} lights are on.'.format(lights.num_on()))

lights = LightGrid2(1000, 1000)
for line in lines:
	lights.do_command(line)
print('Part 2: {} lights are on.'.format(lights.num_on()))

