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

	cooktime = 0

	if len(cookbook) == 0:
		return 'empty mpty mty mt', 400

	name = request.args.get('name')
	if name not in cookbook:
		return 'empty emty mty mt', 400
	
	if cookbook[name].get('type') == 'ingredient':
		return 'ingredienta', 400

	item = cookbook[name]

	ingredients = {}
	ingredientList = []

	if recipeRecursion(name, ingredients, 1) == 0:
		return 'empty emty mty mt', 400

	for ingName in ingredients:
		ingredientList.append ({
			"name": ingName,
			"quantity": ingredients[ingName]
		})
		cooktime += cookbook[ingName].get('cookTime') * ingredients[ingName]

	output = {
		"name": name,
		"cookTime": cooktime,
		"ingredients": ingredientList
	}

	return output, 200

def recipeRecursion(name, ingredients, multiplier):
	if name not in cookbook:
		return 0 

	item = cookbook[name]

	if item.get('type') == 'ingredient':
		if name not in ingredients:
			ingredients[name] = 0
		return 1
	
	requiredItems = item.get('requiredItems', [])\
	
	for reqItem in requiredItems:
		reqName = reqItem.get('name')
		if reqName not in cookbook:
			return 0
		quantity = reqItem.get('quantity')

		if recipeRecursion(reqName, ingredients, quantity) == 1:
			ingredients[reqName] += quantity * multiplier	
	
# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
