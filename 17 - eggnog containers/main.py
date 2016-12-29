import inspect
import os
import re

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

# Interprets the bitmask as selecting a subset of containers.
# Each bit indicates whether the corresponding container is selected.
def examine_bitmask(bitmask, containers):
	total_volume = 0
	num_containers_used = 0  # I.e. the number of 1-bits.
	for bit_index in range(len(containers)):
		if bitmask & (1<<bit_index) != 0:
			total_volume += containers[bit_index]
			num_containers_used += 1
	return (total_volume, num_containers_used)

# Load input.
(containers, target_volume) = (map(int, get_input_lines()), 150)
#(containers, target_volume) = ([20, 15, 10, 5, 5], 25)

# Parts 1 and 2 at the same time.
num_volume_matches = 0
num_used_counts = {}
# Considers all 2^n possible subsets of containers.
for num in range((1<<len(containers)) - 1):
	(total_volume, num_containers_used) = examine_bitmask(num, containers)
	if total_volume == target_volume:
		num_volume_matches += 1
		if num_used_counts.get(num_containers_used) is None:
			num_used_counts[num_containers_used] = 1
		else:
			num_used_counts[num_containers_used] += 1
print('Part 1: Number of ways to add up to {} is {}.'.format(target_volume, num_volume_matches))
min_count = min(num_used_counts.keys())
print('Part 2: Minimum number of containers is {}, wih {} ways to fill them.'.format(min_count, num_used_counts[min_count]))

