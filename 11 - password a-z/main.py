import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

# Modifies chars in place.
def increment(chars):
	pos = -1
	while True:
		if chars[pos] == 'z':
			chars[pos] = 'a'
			pos -= 1
		else:
			chars[pos] = chr(ord(chars[pos]) + 1)
			return

def is_valid(chars):
	first_doubled_char = None
	different_doubled_chars_were_found = False
	straight_was_found = False
	for (i, ch) in enumerate(chars):
		if ch in 'iol':
			return False
		if i + 1 < len(chars):
			if ch == chars[i + 1]:
				if first_doubled_char is None:
					first_doubled_char = ch
				elif first_doubled_char != ch:
					different_doubled_chars_were_found = True
		if i + 2 < len(chars):
			if (ord(chars[i + 1]) == ord(ch) + 1) and (ord(chars[i + 2]) == ord(ch) + 2):
				straight_was_found = True
	return different_doubled_chars_were_found and straight_was_found

#def judge(s):
#	chars = list(s)
#	judgment = 'VALID' if is_valid(chars) else 'NOT VALID'
#	print('{} is {}'.format(s, judgment))
#judge('hijklmmn')  # Should be NOT VALID.
#judge('abbceffg')  # Should be NOT VALID.
#judge('abbcegjk')  # Should be NOT VALID.
#judge('abcdffaa')  # Should be VALID.
#judge('ghjaabcc')  # Should be VALID.

chars = list(get_input_lines()[0])
while True:
	if is_valid(chars):
		print('Part 1: {}.'.format(''.join(chars)))
		break
	else:
		increment(chars)
increment(chars)
while True:
	if is_valid(chars):
		print('Part 2: {}.'.format(''.join(chars)))
		break
	else:
		increment(chars)


