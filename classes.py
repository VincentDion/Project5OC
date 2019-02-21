# -*- coding: Utf-8 -*

import os

import pymysql

from constants import *

# Function to clear the terminal, I do not understand lambda stuff right now but it works
clear = lambda: os.system('cls')


class Product:
    """Class for the Products used in the programm.

    Mainly concerning product that is going to be selected,
    and product of replacement.

    """

    def __init__(self, id_product):
        """Initialization of the class agent.

        From a product id given by the programm, we extract all the data
        from the product table to easily access by this method all the necessary values.

        """
        connection = pymysql.connect(host='localhost',
                                     user='testp5',
                                     password='123456',
                                     db='testp5',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()
        sql_query_for_product = """SELECT id_product, code, product_name_fr, brands, category_id, nutrition_grade, stores, unique_scan_n, quantity FROM Products WHERE id_product=%s"""
        cursor.execute(sql_query_for_product, id_product)
        product_details = cursor.fetchone()

        self.id_product = product_details.get("id_product")
        self.code = product_details.get("code")
        self.category_id = product_details.get("category_id")
        self.category_name = ID_CATEGORY_NAME_DICT.get(product_details.get("category_id"))[1]
        self.product_name = product_details.get("product_name_fr")
        self.brands = product_details.get("brands")
        self.nutrition_grade = product_details.get("nutrition_grade")
        self.stores = product_details.get("stores")
        self.unique_scan_n = product_details.get("unique_scan_n")
        self.quantity = product_details.get("quantity")

        # Condition to verify if selected product is from an orphan category
        # or a category with a parent one that need to also be displayed
        if product_details.get("category_id") % 10 == 9:
            self.parent_category = ""
        else:
            product_parent_category_key = int(product_details.get("category_id")/10)*10
            self.parent_category = ID_CATEGORY_NAME_DICT.get(product_parent_category_key)[1]


    def show_detailed_product(self):
        """Better visualization of products' data.

        Through the use of a print, tabs and jump of line,
        this function's goal is to have all the product's data
        displayed in a clear way without complex graphic interface

        """

        # We create the url adress to the Open Food Facts website
        url_off = "https://fr.openfoodfacts.org/produit/%s" % self.code

        # Attempt for a visible rendering of information without a graphic interface
        print("\nDescriptif du produit: \n\n", "\tNom :", self.product_name, "\n\n\tMarques :", self.brands, "\n\n\tQuantité :",
              self.quantity, "\n\n\tCode-barre :", self.code, "\n\n\tCe produit est disponible dans les magasins suivants :",
              self.stores, "\n\n\tNote nutritive :", self.nutrition_grade, "\n\n\tCatégorie(s) :", self.category_name, "/",
              self.parent_category, "\n\n\tPage Open Food Facts :", url_off, "\n")


    def find_better_product_same_category(self):
        """Finding the product with the best nutritive score within same category.

        By using an array of scores from the constants.py file,
        we run through the product table until we find the first product
        with a better grade.

        """

        connection = pymysql.connect(host='localhost',
                                     user='testp5',
                                     password='123456',
                                     db='testp5',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()

        if self.nutrition_grade == "a":
            print("Ce produit possède dejà la meilleure note nutritive attribuable")
            # Variable used to create the History table
            self.replacement_id_product = self.id_product

        else:

            # This list allows us to transform alphabetical grades in numerical grades thanks to their position in the list
            # Numerical grades allow us to use operators
            selected_product_grade_index = GRADES_RANGE.index(self.nutrition_grade)
            # For example, if a product has a 'd' grade,
            # the value of this variable will be 3 (0 for a, 1 for b and so on)

            targeted_product_grade_index = 0

            # Loop to find a better product
            while targeted_product_grade_index <= selected_product_grade_index:

                targeted_product_grade = GRADES_RANGE[targeted_product_grade_index]
                tuple_for_query = (self.category_id, targeted_product_grade)
                sql_query_for_replacement = """SELECT id_product, code, product_name_fr, brands, category_id, nutrition_grade, stores FROM `Products` WHERE category_id = %s AND nutrition_grade = %s"""
                cursor.execute(sql_query_for_replacement, tuple_for_query)

                replacement = cursor.fetchone()

                if replacement is None:
                    print("Cette catégorie ne contient aucun produit de note nutritive",
                          targeted_product_grade, "dans la base de données actuelle")
                else:
                    if targeted_product_grade_index == selected_product_grade_index:
                        print("Il n'y a pas de produit avec une meilleure note dans cette catégorie")
                        self.replacement_id_product = self.id_product
                    else:
                        print("Le meilleur produit trouvé est le suivant :", replacement.get("product_name_fr"),
                              "avec la note nutritive", replacement.get("nutrition_grade"))
                        # This line to ensure it doesn't check inferior grades, loop stops at the best product available
                        targeted_product_grade_index = len(GRADES_RANGE)

                        self.replacement_id_product = replacement.get("id_product")

                targeted_product_grade_index += 1


    def find_better_product_parent_category(self):
        """Finding the product with the best nutritive score within parent category.

        Works the same as previous function but the sql query
        is on the parent category.

        """
        connection = pymysql.connect(host='localhost',
                                     user='testp5',
                                     password='123456',
                                     db='testp5',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()

        if self.nutrition_grade == "a":
            print("Ce produit possède dejà la meilleure note nutritive attribuable")
            self.replacement_id_product = self.id_product

        else:

            # This list allows us to transform alphabetical grades in numerical grades thanks to their position in the list
            # Numerical grades allow us to use operators
            selected_product_grade_index = GRADES_RANGE.index(self.nutrition_grade)
            # For example, if a product has a 'd' grade, the value of this variable will be 3 (0 for a, 1 for b and so on)

            targeted_product_grade_index = 0
            while targeted_product_grade_index <= selected_product_grade_index:
                # Loop to find a better product
                targeted_product_grade = GRADES_RANGE[targeted_product_grade_index]

                # Operation to find the category_id of parent category
                # (category_id of child divided by 10 without float and multiplied back by 10)
                parent_category_id = int(self.category_id/10)*10

                next_category_id = parent_category_id + 10
                tuple_for_query = (parent_category_id, next_category_id, targeted_product_grade)
                sql_query_for_replacement = """SELECT id_product, code, product_name_fr, brands, category_id, nutrition_grade, stores FROM `Products` WHERE category_id > %s AND category_id < %s AND nutrition_grade = %s"""
                cursor.execute(sql_query_for_replacement, tuple_for_query)
                replacement = cursor.fetchone()

                if replacement is None:
                    print("Ces catégories ne contiennent aucun produit de note nutritive",
                          targeted_product_grade, "dans la base de données actuelle")
                    self.replacement_id_product = self.id_product
                else:
                    if targeted_product_grade_index == selected_product_grade_index:
                        print("Il n'y a pas de produit avec une meilleure note dans ces catégories")
                        self.replacement_id_product = self.id_product
                    else:
                        print("\nLe meilleur produit trouvé est le suivant :", replacement.get("product_name_fr"),
                              "avec la note nutritive", replacement.get("nutrition_grade"))
                        print("\nLe produit a été trouvé dans la catégorie :",
                              ID_CATEGORY_NAME_DICT.get(replacement.get("category_id"))[1])

                        targeted_product_grade_index = len(GRADES_RANGE)
                        self.replacement_id_product = replacement.get("id_product")

                targeted_product_grade_index += 1


class History:
    """ Class for the history functionnality.

    Methods to manipulate the history.
    Create, display or reset it.

    """

    def __init__(self):
        """ Initialization of the class agent.

        From a specific query returning the history with names
        we create a list to be manipulated by the methods.

        """

        connection = pymysql.connect(host='localhost',
                                     user='testp5',
                                     password='123456',
                                     db='testp5',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()

        # Query to get the history table with the correct name of the products from the products table
        cursor.execute("""
            SELECT History.id_research, Ps.product_name_fr AS search, Pr.product_name_fr AS result, History.id_product_results AS id_product
            FROM History
            INNER JOIN Products AS Ps
            ON History.id_product_research = Ps.id_product
            INNER JOIN Products AS Pr
            ON History.id_product_results = Pr.id_product
            ORDER BY History.id_research DESC""")

        history = cursor.fetchall()
        id_selection = 0
        history_list = []
        while id_selection < len(history):
            sub_selection = history[id_selection]
            itera = id_selection + 1
            # itera is the number displayed on the left, indication of which number the user has to press
            name_search = sub_selection.get("search")
            name_result = sub_selection.get("result")
            code_research = sub_selection.get("id_product")
            history_list.append([itera, name_search, name_result, code_research])
            id_selection += 1
        self.history_list = history_list


    def show_history(self):
        """ Display on the user screen the history list """

        i = 0
        while i < len(self.history_list):
            print(self.history_list[i][0], "<=>", self.history_list[i][1], "remplacé par", self.history_list[i][2])
            i += 1


    def reset(self):
        """ Reset the history by deleting all entries in table """

        connection = pymysql.connect(host='localhost',
                                     user='testp5',
                                     password='123456',
                                     db='testp5',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()

        cursor.execute("""DELETE FROM History""")
        print("Historique réinitialisé avec succès")
        connection.commit()
