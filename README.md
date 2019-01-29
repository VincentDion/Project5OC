# Project5OC
Repository for the 5th project of Open Classrooms (PYTHON) with OpenFood Facts

Goal of this project is to have the user select a food product and the programm will find a replacement product with a higher nutritive score according to the French "Open Food Fact" database (https://fr.openfoodfacts.org/). The program also allow the user to save the result of the research to access it later on, even after the programm being previously closed. Code is written for Python 3.

While beign functional, this repository contain a unoptimized version of the code, many functionalities as well as development architectures will be optimized in future versions.

To test the existing code, please follow these instructions :

1) create a mysql user named 'testp5', with the password '123456' and grant all privileges

2) create a database named 'testp5'

3) run the file : P5createDB.py => This file will create the tables in the database you have created just before.

4) run the file : FinalLectureJSON.py => This file will fill the tables with information from the Open Food Fact Frenc database. For the purpose of the exercice, I have limited the number of categories, those are displayed in the constants.py file. Also, around 50 products will be added by categories, this number may be changed in the constants.py file by changing the value of the variable 'number_of_collected_products_by_category'

5) run the file : 5BigtestScriptAppli.py => This is the main file of the script. Once the database is created and filled with products (points 1) to 4)), only this script has to be launched.


Once again, please consider this is a super early functional version.