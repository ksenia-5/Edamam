# Welcome message
# Register to get an APP ID and key https://developer.edamam.com/
# maximum 10 requests per min - max 100 recipes returned for every search

import os
import sys
import requests
import json

# cdir = os.getcwd() # current directory
# pdir = os.path.dirname(cdir) # parent directory
# sys.path.append(os.path.join(pdir,"creds.py")) #add path of parent direcotry to system
# from creds import YOUR_APP_ID, YOUR_APP_KEY # import private ID and KEY stored in creds.py file in parent directory
# fpath = os.path.join(pdir,"edamam_creds.json") #add path of parent direcotry to system

# convert creds to json file?
# with open(fpath) as user_file:
# creds = json.load(user_file)

# YOUR_APP_ID = creds['YOUR_APP_ID']
# OUR_APP_KEY = creds['YOUR_APP_KEY']

# alternatively input ID and KEY value on each run
YOUR_APP_ID = input("Input your application id: ")
YOUR_APP_KEY = input("Input your application key: ")


# Prompt user to input ingredients (one or more) separated by comma
INGREDIENTS = input("Input one or multiple ingredients, separated by a comma:")

# Parse the input to list
# Store as INGREDIENTS = [ ]


# def get_recipes(ingredient):
#     url = f"https://api.edamam.com/search?q={ingredient}&app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
#     response = requests.get(url)
#     response = response.json()
#     recipes = response['hits']
#
#     return recipes
#
# recipes = get_recipes(INGREDIENTS)
#
# for recipe in recipes:
#     print(recipe["recipe"]["label"])
#     print(recipe["recipe"]["totalTime"])
#     print(recipe["recipe"]["ingredientLines"])
#     print(recipe["recipe"]["dishType"])
#
# # query until response is empty

import pandas as pd

# function that returns recipes
def get_recipes(ingredients, start=0, end=10):

    # add app_id and app_key
    params = {"q": INGREDIENTS,
              # "app_id": "",
              # "app_key": "",
              "from": start,
              "to": end
              }
    url = "https://api.edamam.com/search"
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
            new_batch, count, last_end = get_recipes(ingredients, start=last_end, end=last_end + 10)
            all_recipes += new_batch
    except:
        pass
    return all_recipes


# convert list of dictionaries to pandas dataframe with features of interest as columns
def df_from_list_of_dicts(recipes):
    df = pd.DataFrame()
    features = ['label', 'totalTime']
    for feature in features:
        df[feature] = [recipe[feature] for recipe in recipes]
    df['number_ingredients'] = [len(recipe["ingredientLines"]) for recipe in recipes]
    return df

all_recipes = get_all_recipes(INGREDIENTS)

# store id, health label, cooking time, number of ingredients, dish type
pd.set_option('display.max_columns', None)
recipe_df = df_from_list_of_dicts(all_recipes)
print(recipe_df.head(10))

# user inputs sort parameter
sort_by = input("Would you like to sort by: \n\
    1 - dish type\
    2 - total cooking time\
    3 - number of ingredients\n\
    Enter number:\n")

# sort by parameter
sort_dict = {'1': 'dishType',
             '2': 'totalTime',
             '3': 'number_ingredients'}
recipes_sorted = recipe_df.sort_values(sort_dict[sort_by])

# present top three, numbered 1,2,3
print(recipes_sorted.head(10))

# # user chooses recipe to print by inputing value
#
# # make a request to api for chosen recipe (id)
# # user chooses recipe to print by inputing value
# recipe_id = int(input("Enter the number of recipe you wish to print:\n"))
# selected_label = recipes_sorted.loc[recipe_id, 'label']
#
# print("You have selected", selected_label, end="\n\n")
# for recipe in all_recipes:
#     if recipe['label'] == selected_label:
#         print(f"Total preparation time: {recipe['totalTime']} minutes.", end="\n\n")
#         # print(recipe['healthLabels'])
#
#         print("You will need the following ingredients:")
#         for ingredient in recipe['ingredientLines']:
#             print(ingredient)
#
# # label, cooking time, ingredients, instructions and image
#
# write response to file and save