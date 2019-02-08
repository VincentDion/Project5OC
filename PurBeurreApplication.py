# -*- coding: Utf-8 -*


import pymysql
from constants import *
from classes import *
import os


clear = lambda: os.system('cls')
#Formule pour le prompt chaque fois que j'écrirais clear(), j'ai pompé la formule, je n'y comprends rien au lambda, mais ça fonctionne

######## BUG A CORRIGER #############
# Le rendu de l'historique n'est pas affiché dans l'ordre, voir si y a pas un moyen de faire un SORT dès la requete
############

connection = pymysql.connect(host='localhost',
                             user='testp5',
                             password='123456',
                             db='testp5',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

#### Main menu ####
### ON VA D'ABORD FAIRE UN PEU LE TRI DANS MES FONCTIONS ###



def CreateHistory():
    cursor.execute("""
        SELECT History.id_research, Ps.product_name_fr AS search, Pr.product_name_fr AS result, History.code_results AS code
        FROM History
        INNER JOIN Products AS Ps
        ON History.code_research = Ps.code
        INNER JOIN Products AS Pr
        ON History.code_results = Pr.code
        ORDER BY History.id_research DESC""")
    history = cursor.fetchall()
    id_selection = 0
    while id_selection < len(history):
        sub_selection = history[id_selection]
        itera = id_selection + 1
        #itera étant le nombre affiché à gauche de la liste, qui commence à 1 et pas 0
        name_search = sub_selection.get("search")
        name_result = sub_selection.get("result")
        code_research = sub_selection.get("code")
        history_liste.append([itera, name_search, name_result, code_research])
        id_selection += 1
    return history_liste



def ShowHistory():
    i = 0
    global run_loop_history_selection
    if len(history_liste) == 0:
        print("\nVotre historique est vide, utilisez l'application de remplacement de produit et sauvegardez votre résultat pour remplir l'historique\n")
        run_loop_empty_history = 0
        #Initialisation de la variable pour retourner au menu lorsque l'historique est vide
        while run_loop_empty_history == 0:

            try:
                user_product_history_choice = input("Press the ENTER hotkey to go back to the main menu ")
                assert user_product_history_choice == "" or user_product_history_choice == "quit"

            except AssertionError:
                print("")
                run_loop_empty_history = 0

            else:
                if user_product_history_choice == "quit":
                    exit()
                elif user_product_history_choice == "":
                    run_loop_empty_history = 1

        run_loop_history_selection = 1
        return run_loop_history_selection
    else:
        while i < len(history_liste):
            print(history_liste[i][0], "<=>", history_liste[i][1], "remplacé par", history_liste[i][2])
            i += 1

def ResetHistory():
    cursor.execute("""DELETE FROM History""")
    print("Historique réinitialisé avec succès")
    connection.commit()



run_main_loop = 0
user_menu_choice = 0
while run_main_loop == 0:
    clear()
    print("Welcome to the main menu of Pur Beurre's application to improve nutritive quality of aliments.\n")
    user_menu_choice = input("You may access the functionnality of finding an alternative product by pressing 'p' or access the history of your researches by pressing 'h'\n \
Type 'p' or 'h' and press Enter to validate your choice => ")

    if user_menu_choice == "h":
        history_liste = []
        CreateHistory()
        user_history_selection = 0
        run_loop_history_selection = 0
        ShowHistory()
        while run_loop_history_selection == 0:
            user_history_selection = input("Rentrez le nombre associé à votre choix ou tapez RESET pour réinitialiser l'historique\
 \n(ATTENTION : Réinitialiser l'historique est une commande définitive) \n=> ")
            if user_history_selection == "RESET":
                ResetHistory()
                run_loop_history_selection = 1
            elif user_history_selection == "quit":
                exit()
            else:
                try:
                    user_history_selection = int(user_history_selection)
                    assert user_history_selection <= len(history_liste)
                    assert user_history_selection > 0

                except ValueError:
                    print("Veuillez rentrer le nombre correspondant")
                    run_loop_history_selection = 0

                except AssertionError:
                    print("Veuillez rentrer un nombre présent dans cette liste")
                    run_loop_history_selection = 0

                else:
                    #print("Vous avez choisi le numéro ",user_history_selection)
                    user_history_selection = int(user_history_selection)
                    user_history_selection -= 1
                    History_Product = Product(history_liste[user_history_selection][3])
                    History_Product.ShowDetailedProduct(history_liste[user_history_selection][3])

                    run_loop_final_history = 0
                    #Initialisation de la variable pour retourner au menu
                    while run_loop_final_history == 0:

                        try:
                            user_product_history_choice = input("Press the ENTER hotkey to go back to the main menu ")
                            assert user_product_history_choice == "" or user_product_history_choice == "quit"

                        except AssertionError:
                            print("")
                            run_loop_final_history = 0

                        else:
                            if user_product_history_choice == "quit":
                                exit()
                            elif user_product_history_choice == "":
                                run_loop_final_history = 1
                                run_loop_history_selection = 1



    elif user_menu_choice == "p":

        ##### AFFICHER LES CATEGORIES ######


        cursor.execute("""SELECT category_id, category_correct_name FROM Categories""")
        response = cursor.fetchall()

        choice = 0
        while choice < len(response):
            sub_choice = response[choice]
            id_cat = sub_choice.get("category_id")
            name_cat = sub_choice.get("category_correct_name")
            choice = choice + 1

        def AfficherListeCategoriesInOrder():
            clear()
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

        AfficherListeCategoriesInOrder()

        run_loop_categories = 0
        user_category_choice = 0
        while run_loop_categories == 0:
            user_category_choice = input("Tapez le code catégorie associé à votre choix et appuyez sur Entrée ==>  ")
            if user_category_choice == "quit":
                exit()
            else:
                try:
                    user_cat_choice = int(user_category_choice)
                    assert user_cat_choice in id_category_name_dict

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



        ###### AFFICHER LES PRODUITS #########

        sql_product_by_category_query = """SELECT code, product_name_fr, brands, quantity FROM Products WHERE category_id=%s"""
        cursor.execute(sql_product_by_category_query, user_cat_choice)
        response = cursor.fetchall()
        # On vient récupérer la liste complète des produits de la catégorie choisie.

        choice = 0
        liste = []
        while choice < len(response):
            sub_choice = response[choice]
            itera = choice + 1
            name_prod = sub_choice.get("product_name_fr")
            brands_prod = sub_choice.get("brands")
            code_prod = sub_choice.get("code")
            quantity_prod = sub_choice.get("quantity")
            liste.append([itera, name_prod, code_prod, brands_prod, quantity_prod])
            choice = choice + 1


        index_page = 1

        def AfficherProduitsParPage (nombre_produits_par_page, index_page):
            clear()
            start_compteur = (index_page - 1) * nombre_produits_par_page
            compteur = 0
            while compteur < nombre_produits_par_page and start_compteur <= len(response):
                try:
                    if start_compteur < len(liste):
                        print(liste[start_compteur][0],"<=>", liste[start_compteur][1], liste[start_compteur][4], "(marque(s) :",liste[start_compteur][3],")")
                        compteur +=1
                        start_compteur +=1
                    else:
                        compteur +=1
                        start_compteur +=1
                except UnicodeEncodeError:
                    compteur +=1
                    start_compteur +=1
            print("\n\t p <== Page Précédente /","page",index_page,"/ Page Suivante ==> s \n")


        AfficherProduitsParPage(nombre_produits_par_page, index_page)

        #FAUDRA FAIRE GAFFE QD JE VAIS TOUT METTRE EN FONCTIONS SI IL Y A BESOIN DE SE RECONNECTER A LA BASE A CHAQUE FOIS !!!!!

        # On parcours tous les produits et on crée une liste de ceux-ci, la liste sera composée d'autant de sous-listes que de produits
        # ces sous-liste contiendront un numéro d'attribution itera (qui sera le numéro que doit rentrer l'utilisateur pour accéder au produit) et le nom et code produit


        user_choice = 0
        run_boucle_produits = 0

        while run_boucle_produits == 0 :
            user_choice = input("Tapez le nombre ou la lettre associés à votre choix et appuyez sur Entrée ==>  ")
            if user_choice == "p":
                if index_page == 1:
                    print("Vous êtes déjà sur la première page\n")
                else:
                    index_page -= 1
                    AfficherProduitsParPage(nombre_produits_par_page, index_page)
            elif user_choice == "s":
                if index_page == int(len(response)/nombre_produits_par_page)+1:
                    print("Vous êtes sur la dernière page\n")
                else:
                    index_page += 1
                    AfficherProduitsParPage(nombre_produits_par_page, index_page)
            # On a vérifié ici si on était à la première page ou la dernière, afin que l'utilisateur ne puisse qu'avancer si il est à la premère, ou revenir en 
            # arrière si il est à la dernière.
            elif user_choice == "quit":
                exit()
            else:
                try:
                    check = int(user_choice)
                    assert check > nombre_produits_par_page * (index_page - 1)
                    assert check <= nombre_produits_par_page * (index_page)
                    assert check <= len(response)

                except ValueError:
                    print("Veuillez rentrer le chiffre correspondant ou la lettre de changement de page")
                    run_boucle_produits = 0

                except AssertionError:
                    print("Veuillez rentrer un chiffre présent dans cette page de produits")
                    run_boucle_produits = 0

                else:
                    print("Vous avez choisi le numéro ",user_choice)
                    user_choice = int(user_choice)
                    run_boucle_produits = 1


        index_choice = int(user_choice) - 1
        # Comme la liste commence à l'indice 0, il faut soustraire une unité
        result = liste[index_choice]
        # On crée la variable result qui comprend la sous-liste correspondant au produit voulu

        sql_select_query = """SELECT code, product_name_fr, brands, category_id, nutrition_grade, stores, quantity FROM Products WHERE code = %s"""
        cursor.execute(sql_select_query, result[2])
        # On réutilise le 3eme élément des sous-liste (le code) pour récupérer plus d'informations sur le produit sélectionné
        response = cursor.fetchall()
        print(response[0].get("product_name_fr"), response[0].get("nutrition_grade"))
        Chosen_Product = Product(response[0].get("code"))
        Chosen_Product.ShowDetailedProduct(response[0].get("code"))



        def RemplacerParMeilleurProduitMemeCategorie():
            global possible_replacement
            category_response = response[0].get("category_id")
            selected_product_grade = response[0].get("nutrition_grade")
            if selected_product_grade == "a":
                print("Ce produit possède dejà la meilleure note nutritive attribuable")
                possible_replacement = False

            else:
                grades_range = ["a","b","c","d","e"]
                # Cette liste pourra nous permettre de "transformer" les notes alphabétiques en note numériques grâce à leurs positions dans la liste
                # Ce qui permettra de mettre un opérateur de comparaison entre deux notes
                selected_product_grade_index = grades_range.index(selected_product_grade)
                # Si le produit a une note de d, cette variable aura pour valeur 3

                targeted_product_grade_index = 0
                while targeted_product_grade_index <= selected_product_grade_index:
                    # On lance une boucle qui va tenter de trouver un produit plus sain
                    targeted_product_grade = grades_range[targeted_product_grade_index]
                    tuple_for_query = (category_response, targeted_product_grade)
                    sql_select_query2 = """SELECT code, product_name_fr, brands, category_id, nutrition_grade, stores FROM `Products` WHERE category_id = %s AND nutrition_grade = %s"""
                    cursor.execute(sql_select_query2, tuple_for_query)
                    global remplacement
                    remplacement = cursor.fetchone()

                    if remplacement == None:
                        print("Cette catégorie ne contient aucun produit de note nutritive", targeted_product_grade, "dans la base de données actuelle")
                    else:
                        if targeted_product_grade_index == selected_product_grade_index :
                            print("Il n'y a pas de produit avec une meilleure note dans cette catégorie")
                            possible_replacement = False
                        else:
                            print("Le meilleur produit trouvé est le suivant :",remplacement.get("product_name_fr"), "avec la note nutritive", remplacement.get("nutrition_grade"))
                            targeted_product_grade_index = len(grades_range)
                            # Cette dernière ligne pour éviter qu'il check également les catégories supérieures. La boucle s'arrête au meilleur produit trouvé
                            possible_replacement = True

                            Better_Product = Product(remplacement.get("code"))
                            Better_Product.ShowDetailedProduct(remplacement.get("code"))

                    targeted_product_grade_index += 1


        def RemplacerParMeilleurProduitCategorieGenerale():
            global possible_replacement
            category_response = response[0].get("category_id")
            selected_product_grade = response[0].get("nutrition_grade")
            if selected_product_grade == "a":
                print("Ce produit possède dejà la meilleure note nutritive attribuable")
                possible_replacement = False
            else:
                grades_range = ["a","b","c","d","e"]
                # Cette liste pourra nous permettre de "transformer" les notes alphabétiques en note numériques grâce à leurs positions dans la liste
                # Ce qui permettra de mettre un opérateur de comparaison entre deux notes
                selected_product_grade_index = grades_range.index(selected_product_grade)
                # Si le produit a une note de d, cette variable aura pour valeur 3

                targeted_product_grade_index = 0
                while targeted_product_grade_index <= selected_product_grade_index:
                    # On lance une boucle qui va tenter de trouver un produit plus sain
                    targeted_product_grade = grades_range[targeted_product_grade_index]

                    parent_category_id = int(category_response/10)*10
                    # On veut retrouver la category_id de la catégory mère, on prend donc la division entière de l'id fille par 10 et on remultiplie par 10

                    next_category_id = parent_category_id + 10
                    tuple_for_query = (parent_category_id, next_category_id, targeted_product_grade)
                    sql_select_query2 = """SELECT code, product_name_fr, brands, category_id, nutrition_grade, stores FROM `Products` WHERE category_id > %s AND category_id < %s AND nutrition_grade = %s"""
                    cursor.execute(sql_select_query2, tuple_for_query)
                    global remplacement
                    remplacement = cursor.fetchone()

                    if remplacement == None:
                        print("Ces catégories ne contiennent aucun produit de note nutritive", targeted_product_grade, "dans la base de données actuelle")
                        possible_replacement = False
                    else:
                        if targeted_product_grade_index == selected_product_grade_index :
                            print("Il n'y a pas de produit avec une meilleure note dans ces catégories")
                        else:
                            print("Le meilleur produit trouvé est le suivant :",remplacement.get("product_name_fr"), "avec la note nutritive", remplacement.get("nutrition_grade"))
                            print("Le produit a été trouvé dans la catégorie :", id_category_name_dict.get(remplacement.get("category_id"))[1])
                            possible_replacement = True
                            targeted_product_grade_index = len(grades_range)
                            # Cette dernière ligne pour éviter qu'il check également les catégories supérieures. La boucle s'arrête au meilleur produit trouvé
                            Better_Product = Product(remplacement.get("code"))
                            Better_Product.ShowDetailedProduct(remplacement.get("code"))

                    targeted_product_grade_index += 1

        #### BELOW CODE POUR PROPOSER DE REMPLACER LE PRODUIT PAR UN PRODUIT DE LA MEME SOUS-CATEGORIE OU DE LA CATEGORIE MERE ####

        run_loop_replacement = 0

        while run_loop_replacement == 0:
            if response[0].get("category_id")%10 == 9:
                user_replacement_validation = input("The program will now find a replacement for this product in your selected categorie. Continue by pressing ENTER hotkey")
                if user_replacement_validation == "":
                    RemplacerParMeilleurProduitMemeCategorie()
                    run_loop_replacement = 1
                elif user_replacement_validation == "quit":
                    exit()
                else:
                    run_loop_replacement = 0
            else:
                user_replacement_choice = input("Would you like a replacement in the same category or a more global category ? \n\n \
Type s for same category or g for global => ")
                if user_replacement_choice == "s":
                    RemplacerParMeilleurProduitMemeCategorie()
                    run_loop_replacement = 1
                elif user_replacement_choice == "g":
                    RemplacerParMeilleurProduitCategorieGenerale()
                    run_loop_replacement = 1
                elif user_replacement_choice == "quit":
                    exit()
                else:
                    pass
        #Mettre un bloc try pour vérifier que seuls s et g sont fournis
        #Faire des print plus informatif, ou on dit à l'avance dans quelle catégorie générale on va chercher le produit de remplacement, on peut faire du INNER JOIN 
        # pour trouver des noms de catégory à partir des id de la table produit


        ### CODE FOR HISTORY TABLE TO FIND PREVIOUS RESEARCHES ###

        run_loop_history_save = 0

        while run_loop_history_save == 0:
            user_history_choice = input("Would you like to save the results of this research to be accessible quickly from the main menu ? \n\n \
Type s to save or m to go back to the main menu without saving => ")
            if user_history_choice == "s":
                sql_insert_history_query = """INSERT INTO History (code_research, code_results) VALUES (%s, %s)"""
                if possible_replacement == False:
                    tuple_history_insert = (response[0].get("code"), response[0].get("code"))
                    #Dans ce cas on met deux fois le meme code produit, parce qu'il n'y en a pas de meilleur
                    cursor.execute(sql_insert_history_query, tuple_history_insert)
                    connection.commit()
                    run_loop_history_save = 1
                elif possible_replacement == True:
                    tuple_history_insert = (response[0].get("code"), remplacement.get("code"))
                    #Dans ce cas on met le code du produit recherché et le code du produit qui peut le remplacer
                    cursor.execute(sql_insert_history_query, tuple_history_insert)
                    connection.commit()
                    run_loop_history_save = 1
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