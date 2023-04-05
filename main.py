#Welcome message
#Register to get an APP ID and key https://developer.edamam.com/
# maximum 10 requests per min - max 100 recipes returned for every search

import os
import requests
import json
import pandas as pd

cdir = os.getcwd() # current directory
pdir = os.path.dirname(cdir) # parent directory
fpath = os.path.join(pdir,"edamam_creds.json") #add path of parent direcotry to system

# read json file with api credentials
with open(fpath) as user_file:
    creds = json.load(user_file)
YOUR_APP_ID = creds['YOUR_APP_ID']
YOUR_APP_KEY = creds['YOUR_APP_KEY']


# # Prompt user to input ingredients (one or more) separated by comma
INGREDIENTS = input("Input one or multiple ingredients, separated by a comma:")

# Parse the input to list
INGREDIENTS = [ingredient.strip() for ingredient in INGREDIENTS.split(",")]
print(INGREDIENTS)
 
# function that returns recipes
def get_recipes(ingredients, start = 0, end = 10):
    # url  = f"https://api.edamam.com/search?q={ingredients}&app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}&from={start}&to={end}"
    params = {"q": INGREDIENTS,
              "app_id": YOUR_APP_ID,
              "app_key": YOUR_APP_KEY,
              "from": start,
              "to": end
              }
    url  = "https://api.edamam.com/search"
    response = requests.get(url, params=params)
    response = response.json()

    try:
        recipes = response['hits']
        count = response['count']
        recipes = [recipes[i]['recipe'] for i in range(len(recipes))]
        return recipes, count, end
    except:
        print("API throttle limit")
        return None

def get_all_recipes(ingredients):
    all_recipes = []
    try:
        new_batch, count, last_end = get_recipes(ingredients)
        all_recipes = new_batch
        while len(new_batch) != 0:
            new_batch, count, last_end = get_recipes(ingredients, start = last_end, end = last_end + 10)
            all_recipes += new_batch 
    except:
        pass
    return all_recipes

# convert list of dictionaries to pandas dataframe with features of interest as columns
def df_from_list_of_dicts(recipes):
    df = pd.DataFrame()
    features = ['label','totalTime','healthLabels']
    for feature in features:
        df[feature] = [recipe[feature] for recipe in recipes]
    df['number_ingredients'] = [len(recipe["ingredientLines"]) for recipe in recipes]
    df['dishType'] = [recipe['dishType'][0] for recipe in recipes]
    return df


all_recipes = get_all_recipes(INGREDIENTS)
recipe_df = df_from_list_of_dicts(all_recipes)
print(recipe_df.head())

# sort by parameter
sort_dict = {'1':'dishType',
             '2': 'totalTime',
             '3': 'number_ingredients'}

# user inputs sort parameter
sort_by = input("Would you like to sort by: \n\
    1 - dish type\
    2 - total cooking time\
    3 - number of ingredients\n\
    Enter number:\n")

recipes_sorted = recipe_df.sort_values(sort_dict[sort_by])

# present top three, numbered 1,2,3
print(recipes_sorted)

# user chooses recipe to print by inputing value
recipe_id = int(input("Enter the number of recipe you wish to print:\n"))
selected_label = recipes_sorted.loc[recipe_id,'label']

print("You have selected", selected_label, end="\n\n")
for recipe in all_recipes:
    if recipe['label'] == selected_label:
        print(f"Total preparation time: {recipe['totalTime']} minutes.", end="\n\n")
        # print(recipe['healthLabels'])
        
        print("You will need the following ingredients:")
        for ingredient in recipe['ingredientLines']:
            print(ingredient)
        
# label, cooking time, ingredients, instructions and image

# write response to file and save