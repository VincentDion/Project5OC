import pymysql
from constants import *
import os

clear = lambda: os.system('cls')

class Product:
    def __init__(self, code):
        self.code = code

    def ShowDetailedProduct(self, code):
        connection = pymysql.connect(host='localhost',
                             user='testp5',
                             password='123456',
                             db='testp5',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()
        sql_query_for_product = """SELECT code, product_name_fr, brands, category_id, nutrition_grade, stores, unique_scan_n, quantity FROM Products WHERE code=%s"""
        cursor.execute(sql_query_for_product, code)
        product_details = cursor.fetchone()
        if product_details.get("category_id")%10 == 9:
            product_main_category = id_category_name_dict.get(product_details.get("category_id"))[1]
            product_parent_category = ""
        else:
            product_main_category = id_category_name_dict.get(product_details.get("category_id"))[1]
            product_parent_category_key = int(product_details.get("category_id")/10)*10
            product_parent_category = id_category_name_dict.get(product_parent_category_key)[1]
        #Condition to verify if selected product is from an orphan category or a category with a parent one that need to also be displayed
        url_off = "https://fr.openfoodfacts.org/produit/%s" % product_details.get("code")
        #We create the url adress to the Open Food Facts website
        #clear()
        print("Descriptif du produit: \n\n", "\tNom :", product_details.get("product_name_fr"),"\n\n\tMarques :", product_details.get("brands"),"\n\n\tQuantité :\
", product_details.get("quantity"), "\n\n\tCode-barre :", product_details.get("code"), "\n\n\tCe produit est disponible dans les magasins suivants :\
", product_details.get("stores"), "\n\n\tNote nutritive :", product_details.get("nutrition_grade"), "\n\n\tCatégorie(s) :", product_main_category, "/\
", product_parent_category, "\n\n\tPage Open Food Facts :", url_off,"\n")



"""
def AfficherListeCategoriesInOrder():
    ordered_list = []
    for key in id_category_name_dict.keys():
        category_id = key
        ordered_list.append(category_id)
    ordered_list.sort()
    #Première boucle pour remettre dans l'ordre les clés du dico

    for key in ordered_list:
        category_tuple = id_category_name_dict.get(key)
        category_correct_name = category_tuple[1]
        category_id = key
        if key%10 == 0:
            #print(category_correct_name)
            pass
        else:
            print(category_id, "<=>", category_correct_name)
    #Seconde boucle pour donner la correspondance des clés avec leurs valeurs et les afficher
"""