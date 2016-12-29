import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

triples = []
total_paper = 0
total_ribbon = 0
for line in get_input_lines():
	(a, b, c) = sorted(map(int, line.split('x')))
	total_paper += 3*a*b + 2*a*c + 2*b*c
	total_ribbon += 2*(a + b) + a*b*c
print('Part 1: total paper is {}.'.format(total_paper))
print('Part 2: total ribbon is {}.'.format(total_ribbon))
