# -*- coding: Utf-8 -*

import os

from constants import *

# Function to clear the terminal,
# I do not understand lambda stuff right now but it works
clear = lambda: os.system('cls')

def display_categories_in_order():
    """ Function to display the categories on screen.

    The function sorts and display the categories
    for the user to choose one

    """

    clear()
    ordered_list = []

    # First loop to sort keys
    for key in ID_CATEGORY_NAME_DICT.keys():
        category_id = key
        ordered_list.append(category_id)
    ordered_list.sort()

    # Second loop to display the id of categories and their names
    for key in ordered_list:
        category_tuple = ID_CATEGORY_NAME_DICT.get(key)
        category_correct_name = category_tuple[1]
        category_id = key
        if key % 10 == 0:
            pass
        else:
            print(category_id, "<=>", category_correct_name)


def display_products_per_page(products_list,
                              NUMBER_PRODUCTS_PER_PAGE,
                              index_page):
    """ Display a certain number of products on screen."""

    clear()
    start_counter = (index_page - 1) * NUMBER_PRODUCTS_PER_PAGE
    counter = 0
    while counter < NUMBER_PRODUCTS_PER_PAGE and start_counter <= len(products_list):
        try:
            if start_counter < len(products_list):
                print(products_list[start_counter][0],
                      "<=>", products_list[start_counter][1],
                      products_list[start_counter][4],
                      "(marque(s) :", products_list[start_counter][3], ")")
                counter += 1
                start_counter += 1
            else:
                counter += 1
                start_counter += 1
        except UnicodeEncodeError:
            counter += 1
            start_counter += 1
    print("\n\t [p] <== Page Précédente /", "page",
          index_page, "/ Page Suivante ==> [s] \n")
