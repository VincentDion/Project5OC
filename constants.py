# -*- coding: Utf-8 -*

nombre_produits_par_page = 5
id_category_name_dict = {19: ("fromages-a-tartiner", "fromages à tartiner"), 20: ("jus-de-fruits", "jus de fruits"), 21: ("jus-d-orange", "jus d'orange"), \
22: ("jus-de-pamplemousse", "jus de pamplemousse"), 23: ("jus-de-raisin", "jus de raisin"), 24: ("jus-de-pomme", "jus de pomme"), \
25: ("jus-multifruits", "jus multifruits"), 39: ("cremes-fraiches", "crèmes fraiches"), 49: ("biscuits-aperitifs", "biscuits apéritifs"), \
50: ("produits-a-tartiner-sucres", "produits à tartiner sucrés"), 51: ("confitures-d-abricot", "confitures d'abricot"), \
52: ("confitures-de-fruits-rouges", "confitures de fruits rouges"), 53: ("pates-a-tartiner-au-chocolat", "pâtes à tartiner au chocolat"), \
69: ("beurres", "beurres"), 79: ("huiles-d-olive", "huile d'olive")}
#Si la catégorie n'a pas de sous-catégories, son chiffre final est 9, les catégories ayant des sous-catégories sont multiples de 10

number_of_collected_products_by_category = 10

"""
print(id_category_name_dict)

a = id_category_name_dict.get(10)

print(a[1])
"""