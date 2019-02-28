# -*- coding: Utf-8 -*

import json

import pymysql
import requests

from constants import *

"""
This file is for the creation and initialization of the database

Please read the README file for how to create the database
for the application

"""

"""

Starting from here the creation of the database

"""

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='testp5',
                             password='123456',
                             db='testp5',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()



cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories (
    category_id INT UNSIGNED PRIMARY KEY,
    category_url_name VARCHAR(100),
    category_correct_name VARCHAR(100)
    );
    """)

connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
    id_product INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code BIGINT UNSIGNED,
    product_name_fr VARCHAR(200),
    brands VARCHAR(100),
    category_id INT UNSIGNED NOT NULL,
    nutrition_grade CHAR(1),
    unique_scan_n INT UNSIGNED,
    stores VARCHAR (100),
    quantity VARCHAR(100)
    );
    """)

connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS History (
    id_research INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_product_research INT UNSIGNED NOT NULL,
    id_product_results INT UNSIGNED NOT NULL
    );
    """)

connection.commit()

cursor.execute("""
    CREATE INDEX ind_id_product_research
    ON History(id_product_research);
    """)

connection.commit()

cursor.execute("""
    CREATE INDEX ind_id_product_results
    ON History(id_product_results);
    """)

cursor.execute("""
    ALTER TABLE Products 
    ADD CONSTRAINT fk_product_category 
        FOREIGN KEY (category_id) 
        REFERENCES Categories(category_id);
    """)

connection.commit()

cursor.execute("""
    ALTER TABLE History 
    ADD CONSTRAINT fk_id_product_research
        FOREIGN KEY (id_product_research)
        REFERENCES Products(id_product);
    """)

connection.commit()

cursor.execute("""
    ALTER TABLE History 
    ADD CONSTRAINT fk_id_product_results
        FOREIGN KEY (id_product_results)
        REFERENCES Products(id_product);
    """)

connection.commit()

"""

Starting here the filling of the database

"""

def insert_product_in_table(codes, names, brands, category_id,
                            grades, unique_scans_n, stores, quantity):
    """Function to add a product in its designated table.

    The tuple of values we insert is obtain by extracting the data from a json file from
    the Open Food Facts database.

    """

    connection = pymysql.connect(host='localhost',
                                 user='testp5',
                                 password='123456',
                                 db='testp5',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    sql_insert_query = """ INSERT INTO `Products` 
                      (code, product_name_fr, brands, category_id, nutrition_grade, unique_scan_n, stores, quantity)
                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

    insert_tuple = (codes, names, brands, category_id, grades, unique_scans_n, stores, quantity)

    result = cursor.execute(sql_insert_query, insert_tuple)

    connection.commit()

    connection.close()


def insert_category_in_table(category_id, category_url_name, category_correct_name):
    """ Function to add a category in its designated table.

    Categories we insert are from a constant dictionnary containing
    all the values necessary.

    """

    connection = pymysql.connect(host='localhost',
                                 user='testp5',
                                 password='123456',
                                 db='testp5',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    sql_insert_category_query = """ INSERT INTO `Categories`
                      VALUES (%s,%s,%s)"""

    insert_category_tuple = (category_id, category_url_name, category_correct_name)

    result_category = cursor.execute(sql_insert_category_query, insert_category_tuple)

    connection.commit()

    print ("Catégorie insérée avec succès dans la base de données")

    connection.close()


"""Below the code for category insertion.

Categories' values can be find in the constants.py file.

"""
for key in ID_CATEGORY_NAME_DICT.keys():
    category_id = key
    category_tuple = ID_CATEGORY_NAME_DICT.get(key)
    category_url_name = category_tuple[0]
    category_correct_name = category_tuple[1]
    insert_category_in_table(category_id, category_url_name, category_correct_name)


"""Below the code for product insertion.

First we only look for the child category product (first condition) to avoid double insertion.
We then create the url by adding the url category name and the number of products we want to extract.
Those two info can be modified in the constants.py file.
The URL return a json with products sorted by 'popularity' (e.g. number of unique scans)
We go through this file to obtain the elements we need for the Product table.

"""
for key in ID_CATEGORY_NAME_DICT.keys():
    category_tuple = ID_CATEGORY_NAME_DICT.get(key)
    category_url_name = category_tuple[0]
    if key % 10 == 0:
        # We do not take the parent category, only child ones
        pass

    else:

        # We create the url by adding the URL name of categories and the number of results.
        # Products are sorted by popularity (number of unique scans)
        research_url = 'https://fr.openfoodfacts.org/cgi/search.pl?tagtype_0=categories\
&tag_contains_0=contains&tag_0=%s&sort_by=unique_scans_n&page_size=%s&action=process&json=1' \
                        % (category_url_name, NUMBER_OF_COLLECTED_PRODUCTS_BY_CATEGORY)

        r = requests.get(url=research_url)
        data_dict = r.json()
        data = data_dict.get("products")

        i = 0
        while i < len(data):
            sub_data = data[i]
            codes = sub_data.get("code")
            names = sub_data.get("product_name_fr")
            brands = sub_data.get("brands")
            grades = sub_data.get("nutrition_grade_fr")
            stores = sub_data.get("stores")
            quantity = sub_data.get("quantity")
            category_id = key
            if stores == "":
                stores = "non renseigné"
            else:
                pass
            unique_scans_n = sub_data.get("unique_scans_n")

            try:
                if grades is not None and "’" not in names and "€" not in names and names != "":
                    # I encountered some troubles with some special characters, so I decided to pass on them
                    insert_product_in_table(codes, names, brands, category_id, grades, unique_scans_n, stores, quantity)
                    i = i + 1
                else:
                    i = i + 1

            # We also pass on any TypeError
            except TypeError:
                i += 1

    print("Produits de la catégorie", category_tuple[1], "insérée avec succès dans la base de données")

connection.close()
