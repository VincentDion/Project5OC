# -*- coding: Utf-8 -*

import pymysql
from constants import *
import json
import requests

def insertProductInTable(codes, names, brands, category_id, grades, unique_scans_n, stores, quantity):
    
    connection = pymysql.connect(host='localhost',
                                 user='testp5',
                                 password='123456',
                                 db='testp5',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    sql_insert_query = """ INSERT INTO `Products`
                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

    insert_tuple = (codes, names, brands, category_id, grades, unique_scans_n, stores, quantity)

    result  = cursor.execute(sql_insert_query, insert_tuple)

    connection.commit()

    #print ("Record inserted successfully into Products table")

    connection.close()


def insertCategoryInTable(category_id, category_url_name, category_correct_name):
    
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

    result_category  = cursor.execute(sql_insert_category_query, insert_category_tuple)

    connection.commit()

    print ("Record inserted successfully into Categories table")

    connection.close()


#### BELOW THE CODE FOR CATEGORY INSERTION #####

for key in id_category_name_dict.keys():
    category_id = key
    category_tuple = id_category_name_dict.get(key)
    category_url_name = category_tuple[0]
    category_correct_name = category_tuple[1]
    insertCategoryInTable(category_id, category_url_name, category_correct_name)



""" BELOW THE CODE FOR COMPLETE PRODUCT INSERTION """

for key in id_category_name_dict.keys():
    category_tuple = id_category_name_dict.get(key)
    category_url_name = category_tuple[0]
    if key%10 == 0:
        pass
        #On ne veut pas prendre les catégories mères (ex jus de fruit), juste celles d'en dessous pour éviter les doublons
    else:

        #On parcourt la liste des clés et on récupère le nom URL friendly de chaque valeur
        research_url = 'https://fr.openfoodfacts.org/cgi/search.pl?tagtype_0=categories&tag_contains_0=contains&tag_0=%s&sort_by=unique_scans_n&page_size=%s&action=process&json=1' \
        % (category_url_name, number_of_collected_products_by_category)
        
        r = requests.get(url=research_url)
        data_dict = r.json()
        data = data_dict.get("products")

        i = 0
        while i < len(data) :
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
                if grades != None and "’" not in names and "€" not in names and names != "":
                    insertProductInTable(codes, names, brands, category_id, grades, unique_scans_n, stores, quantity)
                    i = i + 1
                else :
                    i = i + 1
                    # Si le produit n'a pas de note nutritive ou contient des signes mal reconnus, on ne le récupère pas
            except TypeError:
                i += 1
                #En cas de TypeError, on n'ajoute pas le produit, ça pouvait arriver avec des caractères spéciaux mal reconnus

    print("Produits de la catégorie", category_tuple[1], "insérée avec succès dans la base de données")

