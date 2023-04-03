#Welcome message
#Register to get an APP ID and key https://developer.edamam.com/

import os
import sys
import requests
import json

#cdir = os.getcwd() # current directory
#pdir = os.path.dirname(cdir) # parent directory
#sys.path.append(os.path.join(pdir,"creds.py")) #add path of parent direcotry to system
#from creds import YOUR_APP_ID, YOUR_APP_KEY # import private ID and KEY stored in creds.py file in parent directory
#fpath = os.path.join(pdir,"edamam_creds.json") #add path of parent direcotry to system

# convert creds to json file?
# with open(fpath) as user_file:
# creds = json.load(user_file)

#YOUR_APP_ID = creds['YOUR_APP_ID']
#OUR_APP_KEY = creds['YOUR_APP_KEY']

#alternatively input ID and KEY value on each run
YOUR_APP_ID = input("Input your application id: ")
YOUR_APP_KEY = input("Input your application id: ")

# Prompt user to input ingredients (one or more) separated by comma
INGREDIENTS = input("Input one or multiple ingredients, separated by a comma:")

# Parse the input to list
# Store as INGREDIENTS = [ ]

url  = "https://api.edamam.com/search?q={INGREDIENTS}&app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"

response = requests.get(url)
response = response.json()


 recipes = response['hits']
 def get_recipe_labels(ingredient):

     response = requests.get(url)
     response = response.json()
     recipes = response['hits']

     recipe_ingredients = [[recipes[i]['recipe']["ingredientLines"] for i in range(len(recipes))]]
     recipe_labels = [recipes[i]['recipe']['label'] for i in range(len(recipes))]
     return recipe_ingredients

 for i in range(len(recipes)):
     recipe = recipes[i]['recipe']
     recipe_title = recipe['label']
     print(recipe_title)

 recipes = get_recipe_labels(INGREDIENTS)
 for recipe in recipes:
     print(recipe)

# query until response is empty

# convert recipes to pandas dataframe, for easier sorting  ## Or could we store this data as a CSV file?
# store id, health label, cooking time, number of ingredients, dish type

# user inputs sort parameter

# sort by parameter

# present top three, numbered 1,2,3

# user chooses recipe to print by inputing value

# make a request to api for chosen recipe (id)
# label, cooking time, ingredients, instructions and image

# write response to file and save