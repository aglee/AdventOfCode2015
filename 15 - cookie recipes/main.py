import inspect
import os

def get_input_lines(file_name = "input.txt"):
	file_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	file_path = os.path.join(file_dir, file_name)
	return [line.rstrip('\n') for line in open(file_path)]

class Ingredient(object):
	# Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
	# => name = 'Sugar', prop_values = (3, 0, 0, -3), calories = 2
	def __init__(self, input_string):
		(self.name, props_string) = input_string.split(':')
		numbers = map(lambda x: int(x.split()[1]), props_string.split(", "))
		self.prop_values = numbers[:-1]
		self.calories = numbers[-1]
	
def cookie_score(ingredients, amounts):
	product = 1
	for prop_index in range(len(ingredients[0].prop_values)):
		weighted_sum = 0
		for (i, ing) in enumerate(ingredients):
			weighted_sum += amounts[i] * ing.prop_values[prop_index]
		if weighted_sum < 0:
			return 0
		product *= weighted_sum
	return product

def cookie_calories(ingredients, amounts):
	calories = 0
	for (i, ing) in enumerate(ingredients):
		calories += amounts[i] * ing.calories
	return calories

# Returns all possible lists of non-negative ints where
# len(list) == num_ingredients and sum(list) == total_teaspoons.
def all_possible_recipes(total_teaspoons, num_ingredients):
	if num_ingredients == 0: return []
	if num_ingredients == 1: return [[total_teaspoons]]

	recipes = []
	for amt in range(0, total_teaspoons + 1):
		for sub_recipe in all_possible_recipes(total_teaspoons - amt, num_ingredients - 1):
			recipes.append([amt] + sub_recipe)
	return recipes

# Load input.
file_name = "input.txt"
#file_name = "test.txt"
ingredients = []
for line in get_input_lines(file_name):
	ingredients.append(Ingredient(line))

# Parts 1 and 2 at the same time.
max_score = -1
max_score_with_calorie_constraint = -1
for recipe in all_possible_recipes(100, len(ingredients)):
	score = cookie_score(ingredients, recipe)
	if score > max_score:
		max_score = score
	if score > max_score_with_calorie_constraint and cookie_calories(ingredients, recipe) == 500:
		max_score_with_calorie_constraint = score
print('Part 1: highest score is {}.'.format(max_score))
print('Part 2: highest score with calorie constraint is {}.'.format(max_score_with_calorie_constraint))


