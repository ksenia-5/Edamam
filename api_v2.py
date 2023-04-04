# Code to get requests from the new API V2
# Register to get an APP ID and key https://developer.edamam.com/

import os
import requests
import json
import time

cdir = os.getcwd() # current directory
pdir = os.path.dirname(cdir) # parent directory
fpath = os.path.join(pdir,"edamam_creds.json") #add path of parent direcotry to system

# read json file with api credentials
with open(fpath) as user_file:
    creds = json.load(user_file)
YOUR_APP_ID = creds['YOUR_APP_ID']
YOUR_APP_KEY = creds['YOUR_APP_KEY']

# # # Prompt user to input ingredients (one or more) separated by comma
# INGREDIENTS = input("Input one or multiple ingredients, separated by a comma:")

# # Parse the input to list
# INGREDIENTS = [ingredient.strip() for ingredient in INGREDIENTS.split(",")]
# print(INGREDIENTS)
INGREDIENTS = "strawberry, chocolate"

url = "https://api.edamam.com/api/recipes/v2/"   

# function that returns recipes
def get_recipes(ingredients, url=url):   
    params = {"q": ingredients, 
             "type":"public", 
             "app_id":YOUR_APP_ID,
             "app_key": YOUR_APP_KEY,
             }
    response = requests.get(url, params = params)
    response = response.json()
    if "_links" in response.keys():
        url_next = response["_links"]["next"]["href"]
    else:
        url_next = None
        return None
    recipes = response['hits']
    count = response['count']
    recipes = [recipes[i]['recipe'] for i in range(len(recipes))]
    # print(recipes[0].keys())
    return recipes, url_next, count


def get_all_recipes(ingredients):
    all_recipes, next_url, count = get_recipes(ingredients)
    try:
        while next_url:
            time.sleep(6)
            new_batch, next_url,count = get_recipes(ingredients, url = next_url)
            all_recipes += new_batch
            
    except:
        pass
    print(f"Total matches in database: {count}")
    return all_recipes

all_recipes = get_all_recipes(INGREDIENTS)
print(f"Number of recipes fetched: {len(all_recipes)}")
for recipe in all_recipes[:20]:
    print(recipe['label'])