import json

import requests

research_url = 'https://fr.openfoodfacts.org/categories.json'

r = requests.get(url=research_url)
data_dict = r.json()
data = data_dict.get("tags")

NUMBER_OF_CATEGORIES = 20

i = 0
ID_CATEGORY_NAME_DICT = {}
while i < NUMBER_OF_CATEGORIES :
    category_complete = data[i]
    category_name = category_complete.get("name")
    category_url_name = category_complete.get("url")
    
    # To work with the existing programm, all categories code have to end by 9 (19, 29, 39 ....)
    code_category = (i + 1) * 10 + 9
    
    # 39 is the number to only get the URL friendly name from the array
    # It is a bit barbaric but it works
    category_url_name = category_url_name[39:]
    ID_CATEGORY_NAME_DICT[code_category] = (category_name, category_url_name)
    i += 1

print(ID_CATEGORY_NAME_DICT)

"""
I didn't get how the categories are sorted, it's not alphabetical.
It is however possible to make a random extract amongts all the categories available.

I didn't find an easy way to regroup categories in child and parent one,
so they are all considered orphan categories
"""