import md5
import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]


def solve(secret_key, prefix):
	num = 0
	while True:
		num += 1
		s = secret_key + str(num)
		m = md5.new(s).hexdigest()
		if m.startswith(prefix):
			return num

secret_key = get_input_lines()[0]
print('Part 1: {}'.format(solve(secret_key, "00000")))
print('Part 2: {}'.format(solve(secret_key, "000000")))
