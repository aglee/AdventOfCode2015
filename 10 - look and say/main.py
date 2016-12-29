import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

def look_and_say(s):
	repeater = None
	repeat_count = 0
	output = ''
	for c in s:
		if c == repeater:
			repeat_count += 1
		else:
			if repeat_count > 0:
				output += str(repeat_count) + repeater
			repeater = c
			repeat_count = 1
	if repeat_count > 0:
		output += str(repeat_count) + repeater
	return output


s = get_input_lines()[0]
for _ in range(40):
	s = look_and_say(s)
print('Part 1: length is {}.'.format(len(s)))

s = get_input_lines()[0]
for _ in range(50):
	s = look_and_say(s)
print('Part 2: length is {}.'.format(len(s)))
