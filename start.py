"""
Register to get an APP ID and key https://developer.edamam.com/    
"""
import os
import sys 
import requests
import json

cdir = os.getcwd() # current directory
pdir = os.path.dirname(cdir) # parent directory
fpath = os.path.join(pdir,"edamam_creds.json") #add path of parent direcotry to system

# convert creds to json file?
with open(fpath) as user_file:
    creds = json.load(user_file)

YOUR_APP_ID = creds['YOUR_APP_ID']
YOUR_APP_KEY = creds['YOUR_APP_KEY']

# alternatively imput ID and KEY value on each run
# YOUR_APP_ID = input("Input your application id: ")
# YOUR_APP_KEY = input("Input your application id: ")

# INGREDIENT = input("Input ingredient: ")
# INGREDIENT = ["tofu","chicken","tomato"]



def get_recipe_labels(ingredient):
    url  = f"https://api.edamam.com/search?q=['tofu','chicken','tomato']&from=0&to=10&app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
    # url  = f"https://api.edamam.com/search?q={INGREDIENT}&from=0&to=10&app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
    # url1 = f"https://api.edamam.com/api/v2?q={INGREDIENT}&app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
    response = requests.get(url)
    response = response.json()
    recipes = response['hits']
    # list comprehension
    recipe_ingredients = [[recipes[i]['recipe']["ingredientLines"] for i in range(len(recipes))]] 
    recipe_labels = [recipes[i]['recipe']['label'] for i in range(len(recipes))]
    return recipe_ingredients

recipes = get_recipe_labels("tofu")
for recipe in recipes:
    print(recipe)