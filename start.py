"""
Register to get an APP ID and key https://developer.edamam.com/    
"""
import os
import sys 
import requests

cdir = os.getcwd() # current directory
pdir = os.path.dirname(cdir) # parent directory
sys.path.append(os.path.join(pdir,"creds.py")) #add path of parent direcotry to system
from creds import YOUR_APP_ID, YOUR_APP_KEY # import private ID and KEY stored in creds.py file in parent directory

# alternatively imput ID and KEY value on each run
#YOUR_APP_ID = input("Input your application id: ")
# YOUR_APP_KEY = input("Input your application id: ")

# INGREDIENT = input("Input ingredient: ")
INGREDIENT = "tofu"

url  = f"https://api.edamam.com/search?q={INGREDIENT}&app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"

response = requests.get(url)
response = response.json()
# print(response)

recipes = response['hits']

for i in range(len(recipes)):
    recipe = recipes[i]['recipe']
    recipe_title = recipe['label']
    print(recipe_title)
