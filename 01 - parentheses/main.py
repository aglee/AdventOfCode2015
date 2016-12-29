import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

input = get_input_lines()[0]
floor = 0
basement_char_pos = None
for (pos, ch) in enumerate(input):
	if ch == '(':
		floor += 1
	elif ch == ')':
		floor -= 1
	else:
		print('unexpected character "{}"'.format(ch))
		exit()
	if floor == -1 and basement_char_pos == None:
		basement_char_pos = pos
print('Part 1: final floor is {}.'.format(floor))
# The problem asks for a 1-based character index, hence the "+ 1".
print('Part 2: first entered basement at character {}.'.format(basement_char_pos + 1))
