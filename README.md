# Project5OC
Repository for the 5th project of Open Classrooms (PYTHON) with OpenFood Facts.

Goal of this project is to have the user select a food product and the programm will find a replacement product with a higher nutritive score according to the French "Open Food Fact" database (https://fr.openfoodfacts.org/). The program also allow the user to save the result of the research to access it later on, even after the programm being previously closed. Code is written for Python 3.

Application is named "Pur Beurre Application".


# VERSION 1.2

At last the code is fully functionnal, all functionnalities required by the exercice are implemented.


# HOW TO LAUNCH THE APPLICATION :

To test the existing code, please follow these instructions :

1) create a mysql user named 'testp5', with the password '123456' and grant all privileges

2) create a database named 'testp5'

3) run the file : DB_PBA_initialization.py => This will create and fill the database for the project, you may change the number of products by categories in the constants.py file

5) run the file : PurBeurreApplication.py => This is the main file of the script. Once the database is created and filled with products (points 1) to 4)), only this script has to be launched everytime.


# NEW IN 1.2 :

1.2 is mainly focused on the code and note the usage :
- New file in replacement of two previous one for the initialization of the database
- Requirements.txt file added
- Adding of foreign keys on the database
- New folder utils with functions and classes
- PEP8 optimization
- Branch 1.2 in repository github


# FUTURE IMPROVEMENTS :

Although all functionnalities are to remain unchanged, many changes has to be made for the programm to be in complete accordance with the requirements for the exercice :

- PEP8 complete compliance (import * and lines too long to get rid off)
- Find a way to make the connection a function
- README guide for future dev purposes (naming convention for variables etc...)
- User experience : we can always improve user experience
