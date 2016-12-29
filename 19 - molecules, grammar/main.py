import inspect
import os
import re
import Queue

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

# Represents molecules as tuples of atom names.
class Machine(object):
	def __init__(self, lines):
		self.rules = {}
		for line in lines:
			if len(line) == 0:
				break
			(symbol, replacement) = line.split(' => ')
			replacement_atoms = self.split_into_atoms(replacement)
			if self.rules.get(symbol) == None:
				self.rules[symbol] = [replacement_atoms]
			else:
				self.rules[symbol].append(replacement_atoms)

	def dump_rules(self):
		for k in sorted(self.rules.keys()):
			print('{} => {}'.format(k, ' | '.join(map(lambda x: ''.join(x), self.rules[k]))))

	def replacements_for_symbol(self, symbol):
		if self.rules.get(symbol) == None:
			return []
		else:
			return self.rules[symbol]

	def split_into_atoms(self, s):
			return tuple(re.findall('[A-Z][a-z]|[A-Z]|e', s))
	
	def possible_productions(self, molecule):
		prods = set()
		for i in range(len(molecule)):
			for replacement in self.replacements_for_symbol(molecule[i]):
				new_molecule = tuple(molecule[:i] + replacement + molecule[i+1:])
				prods.add(tuple(new_molecule))
		return prods

lines = get_input_lines()
machine = Machine(lines)
machine.dump_rules()
molecule = machine.split_into_atoms(lines[-1])
#print(molecule)
print(len(machine.possible_productions(molecule)))





