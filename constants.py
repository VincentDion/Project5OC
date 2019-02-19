# -*- coding: Utf-8 -*

NUMBER_PRODUCTS_PER_PAGE = 25
# Number of products that will be displayed for each page
# 25 seemed to me a reasonable amount

ID_CATEGORY_NAME_DICT = {19: ("fromages-a-tartiner", "fromages à tartiner"),
                         20: ("jus-de-fruits", "jus de fruits"),
                         21: ("jus-d-orange", "jus d'orange"),
                         22: ("jus-de-pamplemousse", "jus de pamplemousse"),
                         23: ("jus-de-raisin", "jus de raisin"),
                         24: ("jus-de-pomme", "jus de pomme"),
                         25: ("jus-multifruits", "jus multifruits"),
                         39: ("cremes-fraiches", "crèmes fraiches"),
                         49: ("biscuits-aperitifs", "biscuits apéritifs"),
                         50: ("produits-a-tartiner-sucres", "produits à tartiner sucrés"),
                         51: ("confitures-d-abricot", "confitures d'abricot"),
                         52: ("confitures-de-fruits-rouges", "confitures de fruits rouges"),
                         53: ("pates-a-tartiner-au-chocolat", "pâtes à tartiner au chocolat"),
                         69: ("beurres", "beurres"),
                         79: ("huiles-d-olive", "huile d'olive")}
# Values are written in French because we are extracting data from the French Open Food Facts website
# When a category key ends by a 9, it means there is no "child" category,
# When it ends by a 0, it means all the categories with the same decade are child categories
# It was an arbitrary choice to make code easier, please keep the same logic if adding categories
# First value is the URL name of the category, second the one which will be displayed

NUMBER_OF_COLLECTED_PRODUCTS_BY_CATEGORY = 500
# That makes approximatively 5000 products total
# Can easily be changed (for now, extraction takes around 1 minute)

GRADES_RANGE = ["a","b","c","d","e"]
# This list allows us to transform alphabetical grades in numerical grades thanks to their position in the list
# Numerical grades allow us to use operators