from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re


# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# TODO: implement me
	if len(recipeName) <= 0:
		return None
	a = re.sub('[-_-]', ' ', recipeName)
	b = re.sub('[^a-zA-Z ]', '', a)
	c = b.lower()
	d = c.title()
	e = d.strip() # leading and trialing whitespace
	f = re.sub('[ ]+', ' ', e) 

	return f


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():

	data = request.json
	dataType = data.get('type')
	cookTime = data.get('cookTime')

	for i in cookbook.values():
		if data.get('name') == i.get('name'):
			return 'not implemented', 400

	if dataType not in ['recipe', 'ingredient']:
		return 'you messed up ya goose', 400

	if dataType == 'ingredient' and cookTime < 0:
		return 'time traveler', 400
	
	# one element per name
	if dataType == 'recipe':
		nameList = []
		requiredItems = data.get('requiredItems')
		for item in requiredItems:
			nameList.append(item.get('name'))

		if len(nameList) != len(set(nameList)):
			return 'not implemented', 400
	
	cookbook[data.get('name')] = data
	return 'not implemented', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():

	name = request.args.get('name')
	item = cookbook[name]

	ingredients = {}
	ingredientList = []

	recipeRecursion(name, ingredients)

	for name in ingredients:
		ingredientList.append
		({
			"name": name,
			"quanity": ingredients[name]
		})

		item = cookbook[name]
		cooktime += item.get('cookTime') * name.value

	output = {
		"name": name,
		"cookTime": cooktime,
		"ingredients": ingredientList
	}

	return output, 200

def recipeRecursion(name, ingredients): 
	item = cookbook[name]
	requiredItems = item.get('requiredItems')

	for item in requiredItems:
		dataType = cookbook[item].get('type')
		name = item.get('name')
		if dataType == 'recipe':
			return recipeRecursion(name, ingredients)
		else:
			ingredients[name] += item.get('quantity')
			return
	
# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
