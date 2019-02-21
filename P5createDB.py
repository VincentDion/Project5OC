import pymysql

"""
This file is for the creation of the database

Please read the README file for how to create the database
for the application

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

connection.close()
