import inspect, os

fileDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
filePath = os.path.join(fileDir, "input.txt")  # "input.txt" or "test.txt"
lines = [line.rstrip('\n') for line in open(filePath)]

def quoting_diff(s):
	num_tossed = 0
	return len(s) - num_tossed

total_tossed = 0
for line in lines:
	total_tossed += quoting_diff(s)
print(total_tossed)
