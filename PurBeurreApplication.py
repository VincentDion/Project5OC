# -*- coding: Utf-8 -*

import os

import pymysql

from constants import *
from classes import *
from functions import *


# Function to clear the terminal, I do not understand lambda stuff right now but it works
clear = lambda: os.system('cls')

# Connection to database
connection = pymysql.connect(host='localhost',
                             user='testp5',
                             password='123456',
                             db='testp5',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

run_main_loop = 0
user_menu_choice = 0
# Loop for the whole program
while run_main_loop == 0:
    clear()
    print("Bienvenue dans le menu principal de l'application Pure Beurre.\n")
    user_menu_choice = input("Pour accéder à la fonctionnalité de remplacement de produit appuyez sur la touche [p].\
\nPour la fonctionnalité d'historique, appuyez sur la touche [h]\n\
Vous pouvez également quitter à tout moment l'application en tapant [quit] et en validant avec Entrée\n\n\
Appuyez sur [p] ou [h] et validez votre choix en appuyant sur Entrée => ")

    if user_menu_choice == "h":
        HistoryList = History()
        if len(HistoryList.history_list) == 0:
            print("\nVotre historique est vide, utilisez l'application de remplacement de produit \
et sauvegardez votre résultat pour remplir l'historique\n")
            run_loop_empty_history = 0
            # Loop to wait for the user to press Enter and go back to the main menu
            while run_loop_empty_history == 0:
                try:
                    user_history_empty = input("Appuyez sur la touche [Entrée] pour retourner au menu principal")
                    assert user_history_empty == "" or user_history_empty == "quit"

                except AssertionError:
                    print("")
                    run_loop_empty_history = 0

                else:
                    if user_history_empty == "quit":
                        exit()
                    elif user_history_empty == "":
                        run_loop_empty_history = 1
        else:
            user_history_selection = 0
            run_loop_history_selection = 0
            HistoryList.show_history()
            while run_loop_history_selection == 0:
                user_history_selection = input("Rentrez le nombre associé à votre choix ou tapez [RESET] pour réinitialiser l'historique\
\n(ATTENTION : Réinitialiser l'historique est une commande définitive) \n=> ")
                if user_history_selection == "RESET":
                    HistoryList.reset()
                    run_loop_history_selection = 1
                elif user_history_selection == "quit":
                    exit()
                else:
                    try:
                        user_history_selection = int(user_history_selection)
                        assert user_history_selection <= len(HistoryList.history_list)
                        assert user_history_selection > 0

                    except ValueError:
                        print("Veuillez rentrer le nombre correspondant")
                        run_loop_history_selection = 0

                    except AssertionError:
                        print("Veuillez rentrer un nombre présent dans cette liste")
                        run_loop_history_selection = 0

                    else:
                        user_history_selection = int(user_history_selection)
                        user_history_selection -= 1
                        History_Product = Product(HistoryList.history_list[user_history_selection][3])
                        History_Product.show_detailed_product()

                        run_loop_final_history = 0
                        while run_loop_final_history == 0:

                            try:
                                user_back_menu = input("Appuyez sur la touche [Entrée] pour retourner au menu principal ")
                                assert user_back_menu == "" or user_back_menu == "quit"

                            except AssertionError:
                                print("")
                                run_loop_final_history = 0

                            else:
                                if user_back_menu == "quit":
                                    exit()
                                elif user_back_menu == "":
                                    run_loop_final_history = 1
                                    run_loop_history_selection = 1

    elif user_menu_choice == "p":

        cursor.execute("""SELECT category_id, category_correct_name FROM Categories""")
        response = cursor.fetchall()

        choice = 0
        while choice < len(response):
            sub_choice = response[choice]
            id_cat = sub_choice.get("category_id")
            name_cat = sub_choice.get("category_correct_name")
            choice = choice + 1

        # Run the function for the user to choose a category
        display_categories_in_order()

        run_loop_categories = 0
        user_category_choice = 0
        # Loop for the user choice of category
        while run_loop_categories == 0:
            user_category_choice = input("Tapez le code catégorie associé à votre choix et appuyez sur Entrée ==>  ")
            if user_category_choice == "quit":
                exit()
            else:
                try:
                    user_cat_choice = int(user_category_choice)
                    assert user_cat_choice in ID_CATEGORY_NAME_DICT

                except ValueError:
                    print("Veuillez rentrer un nombre associé à une catégorie")
                    run_loop_categories = 0

                except AssertionError:
                    print("Veuillez rentrer un nombre associé à une catégorie")
                    run_loop_categories = 0

                else:
                    clear()
                    print("Vous avez choisi le numéro", user_cat_choice)
                    run_loop_categories = 1

        # From here we extract from the product table products from selected category
        sql_product_by_category_query = """SELECT id_product, product_name_fr, brands, quantity FROM Products WHERE category_id=%s"""
        cursor.execute(sql_product_by_category_query, user_cat_choice)
        response = cursor.fetchall()

        choice = 0
        products_list = []
        # Loop to create a list with products elements to be displayed on screen
        while choice < len(response):
            sub_choice = response[choice]
            itera = choice + 1
            name_prod = sub_choice.get("product_name_fr")
            brands_prod = sub_choice.get("brands")
            code_prod = sub_choice.get("id_product")
            quantity_prod = sub_choice.get("quantity")
            products_list.append([itera, name_prod, code_prod, brands_prod, quantity_prod])
            choice = choice + 1

        # Variable to display on which page the user is
        index_page = 1

        # Run of the function with a constant from constants.py file
        display_products_per_page(products_list, NUMBER_PRODUCTS_PER_PAGE, index_page)

        user_choice = 0
        run_loop_product_selection = 0
        # Loop for user input (select a product or change page)
        while run_loop_product_selection == 0:
            user_choice = input("Tapez le nombre ou la lettre associés à votre choix et appuyez sur Entrée ==>  ")
            # p for previous page
            if user_choice == "p":
                # We check here if the user is already on first page
                if index_page == 1:
                    print("Vous êtes déjà sur la première page\n")
                else:
                    index_page -= 1
                    utils_pba.functions.display_products_per_page(products_list, NUMBER_PRODUCTS_PER_PAGE, index_page)
            # s for next page
            elif user_choice == "s":
                # We check here if user is on last page
                if index_page == int(len(response)/NUMBER_PRODUCTS_PER_PAGE)+1:
                    print("Vous êtes sur la dernière page\n")
                else:
                    index_page += 1
                    utils_pba.functions.display_products_per_page(products_list, NUMBER_PRODUCTS_PER_PAGE, index_page)
            elif user_choice == "quit":
                exit()
            else:
                # Try bloc to assert user is typing a valid number
                try:
                    check = int(user_choice)
                    assert check > NUMBER_PRODUCTS_PER_PAGE * (index_page - 1)
                    assert check <= NUMBER_PRODUCTS_PER_PAGE * (index_page)
                    assert check <= len(response)

                except ValueError:
                    print("Veuillez rentrer le chiffre correspondant ou la lettre de changement de page")
                    run_loop_product_selection = 0

                except AssertionError:
                    print("Veuillez rentrer un chiffre présent dans cette page de produits")
                    run_loop_product_selection = 0

                else:
                    print("Vous avez choisi le numéro ", user_choice)
                    user_choice = int(user_choice)
                    run_loop_product_selection = 1

        # Array start at 0, so we substract one
        index_choice = int(user_choice) - 1

        # Variable containing the sub-list of the selected product
        result = products_list[index_choice]

        # Creation of the Product class agent for the selected product
        ChosenProduct = Product(result[2])
        ChosenProduct.show_detailed_product()

        run_loop_replacement = 0
        # Loop to ask the user if she/he wants a replacement and from which category
        while run_loop_replacement == 0:
            # If category is orphan, replace by product of same category
            if ChosenProduct.category_id % 10 == 9:
                user_replacement_validation = input("Le programme va maintenant rechercher un meilleur produit, appuyez sur la touche [Entrée] pour valider")
                if user_replacement_validation == "":
                    ChosenProduct.find_better_product_same_category()
                    # If selected product is already the best available
                    if ChosenProduct.replacement_id_product == ChosenProduct.id_product:
                        pass
                    # Else we create a new class product agent to be displayed
                    else:
                        ReplacementProduct = Product(ChosenProduct.replacement_id_product)
                        ReplacementProduct.show_detailed_product()
                    run_loop_replacement = 1
                elif user_replacement_validation == "quit":
                    exit()
                else:
                    run_loop_replacement = 0
            # Here, selected category has a parent one the user can choose a replacement in
            else:
                user_replacement_choice = input("Souhaitez-vous un remplacement dans la même sous-catégorie ou parmi la catégorie générale ? \n\n \
Appuyez sur [m] pour même categorie ou [g] pour catégorie générale => ")
                # User chooses a replacement in same category
                if user_replacement_choice == "m":
                    ChosenProduct.find_better_product_same_category()
                    if ChosenProduct.replacement_id_product == ChosenProduct.id_product:
                        pass
                    else:
                        ReplacementProduct = Product(ChosenProduct.replacement_id_product)
                        ReplacementProduct.show_detailed_product()
                    run_loop_replacement = 1
                # User chooses a replacement in parent category
                elif user_replacement_choice == "g":
                    ChosenProduct.find_better_product_parent_category()
                    if ChosenProduct.replacement_id_product == ChosenProduct.id_product:
                        pass
                    else:
                        ReplacementProduct = Product(ChosenProduct.replacement_id_product)
                        ReplacementProduct.show_detailed_product()
                    run_loop_replacement = 1
                elif user_replacement_choice == "quit":
                    exit()
                else:
                    pass

        run_loop_history_save = 0

        # Loop for the saving functionnality
        while run_loop_history_save == 0:
            user_history_choice = input("Souhaitez-vous sauvegarder le résultat de cette recherche ?\n\n \
Appuyez sur [s] pour sauvegarder ou [m] pour retourner au menu principal sans sauvegarder => ")
            # User chooses to save the results
            if user_history_choice == "s":
                sql_insert_history_query = """INSERT INTO History (id_product_research, id_product_results) VALUES (%s, %s)"""
                tuple_history_insert = (ChosenProduct.id_product, ChosenProduct.replacement_id_product)
                cursor.execute(sql_insert_history_query, tuple_history_insert)
                connection.commit()
                run_loop_history_save = 1
            # User chooses t ogo back to menu without saving
            elif user_history_choice == "m":
                run_loop_history_save = 1
            elif user_history_choice == "quit":
                exit()
            else:
                pass

    elif user_menu_choice == "quit":
        exit()

    else:
        pass

connection.close()
