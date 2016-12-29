import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

def parse_input():
	people = set()
	happiness_effects = {}
	for line in get_input_lines("input.txt"):
		parts = line.split()
		affected_person = parts[0]
		people.add(affected_person)
		happiness_delta = int(parts[3])
		if parts[2] == 'lose': happiness_delta = -happiness_delta
		neighbor = parts[-1][:-1]
		happiness_effects[(affected_person, neighbor)] = happiness_delta
	return (list(people), happiness_effects)

# Copied this function from Day 9.
def all_permutations(items):
	if len(items) < 2: return [items]
	
	perms = []
	for i in range(len(items)):
		shorter_list = items[:]
		item = shorter_list.pop(i)
		for shorter_permutation in all_permutations(shorter_list):
			perms.append([item] + shorter_permutation)
	return perms

def total_happiness_effect(people, happiness_effects):
	total = 0
	for i in range(len(people) - 1):
		total += happiness_effects[(people[i], people[i + 1])]
		total += happiness_effects[(people[i + 1], people[i])]
	total += happiness_effects[(people[len(people) - 1], people[0])]
	total += happiness_effects[(people[0], people[len(people) - 1])]
	return total

def best_happiness(people, happiness_effects):
	best_effect = None
	best_seq = None
	for seq in all_permutations(list(people)):
		eff = total_happiness_effect(seq, happiness_effects)
		if best_effect is None or eff > best_effect:
			best_effect = eff
			best_seq = seq
	return (best_effect, best_seq)

(people, happiness_effects) = parse_input()

(best_effect, best_seq) = best_happiness(people, happiness_effects)
print('Part 1: best change to happiness if {}.'.format(best_effect))

me = "Myself"
people.append(me)
for person in people:
	happiness_effects[(me, person)] = 0
	happiness_effects[(person, me)] = 0

(best_effect, best_seq) = best_happiness(people, happiness_effects)
print('Part 2: best change to happiness if {}.'.format(best_effect))

