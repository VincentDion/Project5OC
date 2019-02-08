# Project5OC
Repository for the 5th project of Open Classrooms (PYTHON) with OpenFood Facts

Goal of this project is to have the user select a food product and the programm will find a replacement product with a higher nutritive score according to the French "Open Food Fact" database (https://fr.openfoodfacts.org/). The program also allow the user to save the result of the research to access it later on, even after the programm being previously closed. Code is written for Python 3.


VERSION 1.0

At last the code is fully functionnal, all functionnalities required by the exercice are implemented.


HOW TO LAUNCH THE APPLICATION :

To test the existing code, please follow these instructions :

1) create a mysql user named 'testp5', with the password '123456' and grant all privileges

2) create a database named 'testp5'

3) run the file : P5createDB.py => This file will create the tables in the database you have created just before.

4) run the file : FinalLectureJSON.py => This file will fill the tables with information from the Open Food Fact Frenc database. For the purpose of the exercice, I have limited the number of categories, those are displayed in the constants.py file. Also, around 50 products will be added by categories, this number may be changed in the constants.py file by changing the value of the variable 'number_of_collected_products_by_category'

5) run the file : PurBeurreApplication.py => This is the main file of the script. Once the database is created and filled with products (points 1) to 4)), only this script has to be launched.


FUTURE IMPROVEMENTS :

Although all functionnalities are to remain unchanged, many changes has to be made for the programm to be in complete accordance with the requirements for the exercice :

- Translate everything in English
- Add the commentaries (so far the code is a big pile of mess)
- PEP8 compliance
- Virtual environment to be created
- README guide for future dev purposes (naming convention for variables etc...)


NO OOP SCHEDULED :

Code could be using a lot more of Object Oriented Programming methods, but I feel I have enough of it so far, it's been too long I'm stuck on it, better move on and go back at it another time.