import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

class Reindeer(object):
	def __init__(self, line):
		parts = line.split()
		self.name = parts[0]
		self.km_per_second = int(parts[3])
		self.fly_seconds = int(parts[6])
		self.rest_seconds = int(parts[-2])

	def distance_flown_at_time(self, t):
		# Let a "period" be a full block of time flying plus a full block of time resting.
		period = self.fly_seconds + self.rest_seconds
		
		# The number of FULL periods elapsed at time t.
		num_periods = t / period
		
		# Add up the flying time in those FULL periods.
		d = num_periods * self.km_per_second * self.fly_seconds
		
		# Number of seconds the reindeer is into a PARTIAL period at time t.
		partial_period = t % period
		
		# Of that PARTIAL period, the reindeer spent at most fly_seconds flying.
		return d + min(partial_period, self.fly_seconds)*self.km_per_second

def leader_and_distance_at_time(racers, t):
	(leader, best_distance) = (None, -1)
	for r in racers:
		dist = r.distance_flown_at_time(t)
		if dist > best_distance:
			(leader, best_distance) = (r, dist)
	return (leader, best_distance)

# Load input.
(file_name, race_duration) = ("input.txt", 2503)
#(file_name, race_duration) = ("test.txt", 1000)
racers = []  # "Reindeer" is a confusing plural to my eye.
for line in get_input_lines(file_name):
	racers.append(Reindeer(line))

# Part 1.
(leader, best_dist) = leader_and_distance_at_time(racers, race_duration)
print('Part 1: best DISTANCE after {} seconds is {}.'.format(race_duration, best_dist))

# Part 2.
scores = {}
for i in range(race_duration):
	# Increment the score for *all* racers that are in the lead.
	(leader, best_dist) = leader_and_distance_at_time(racers, i + 1)
	for r in racers:
		if r.distance_flown_at_time(i + 1) == best_dist:
			if scores.get(r.name): scores[r.name] += 1
			else: scores[r.name] = 1
print('Part 2: best SCORE after {} seconds is {}.'.format(race_duration, max(scores.values())))

