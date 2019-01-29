import pymysql

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='testp5',
                             password='123456',
                             db='testp5',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS Products (
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
	CREATE TABLE IF NOT EXISTS Categories (
	category_id INT UNSIGNED PRIMARY KEY,
	category_url_name VARCHAR(100),
	category_correct_name VARCHAR(100)
	);
	""")

connection.commit()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS History (
	id_research INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	code_research BIGINT UNSIGNED NOT NULL,
	code_results BIGINT UNSIGNED NOT NULL
	);
	""")

connection.commit()

cursor.execute("""
	CREATE INDEX ind_code_research
	ON History(code_research);
	""")

connection.commit()

cursor.execute("""
	CREATE INDEX ind_code_results
	ON History(code_results);
	""")

connection.close()

