import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

def is_nice(s):
	if len(s) < 3: return False
	disallowed_successors = { 'a': 'b', 'c': 'd', 'p': 'q', 'x': 'y' }
	vowel_count = 0
	double_was_found = False
	for (i, current) in enumerate(s):
		if current in 'aeiou': vowel_count += 1
		if i + 1 < len(s):
			next = s[i + 1]
			if next == disallowed_successors.get(current): return False
			if current == next: double_was_found = True
	return vowel_count >= 3 and double_was_found
			
#def judge(s):
#	judgment = "NICE" if is_nice(s) else "NAUGHTY"
#	print('{} is {}'.format(s, judgment))
#judge("ugknbfddgicrmopn")  # Should be NICE.
#judge("aaa")  # Should be NICE.
#judge("jchzalrnumimnmhp")  # Should be NAUGHTY.
#judge("haegwjzuvuyypxyu")  # Should be NAUGHTY.
#judge("dvszwmarrgswjxmb")  # Should be NAUGHTY.

def is_nice2(s):
	if len(s) < 3: return False
	pairs_first_indexes = {}
	repeated_ab_was_found = False
	aba_was_found = False
	for i in range(len(s) - 1):
		a = s[i]
		b = s[i + 1]

		pair_index = pairs_first_indexes.get(a + b)
		if pair_index == None:
			pairs_first_indexes[a + b] = i
		elif i >= pair_index + 2:
			repeated_ab_was_found = True

		if i + 2 < len(s):
			if a == s[i + 2]: aba_was_found = True
	return repeated_ab_was_found and aba_was_found
			
#def judge2(s):
#	judgment = "NICE" if is_nice2(s) else "NAUGHTY"
#	print('{} is {}'.format(s, judgment))
#judge2("qjhvhtzxzqqjkmpb")  # Should be NICE.
#judge2("xxyxx")  # Should be NICE.
#judge2("uurcxstgmygtbstg")  # Should be NAUGHTY.
#judge2("ieodomkazucvgmuy")  # Should be NAUGHTY.

lines = get_input_lines()
nice_count = map(is_nice, lines).count(True)
print('Part 1: found {} nice strings.'.format(nice_count))
nice_count = map(is_nice2, lines).count(True)
print('Part 2: found {} nice strings.'.format(nice_count))


