import sqlite3


def add_customer() -> None:
	print()
	data = {'Имя': '', 'Фамилия': '', 'Почтовый код': ''}
	for k in data.keys():
		data[k] = input(f'{k}: ')
		
	with sqlite3.connect("accounts.db") as con:
		cur = con.cursor()
		cur.execute(
			 "INSERT INTO clients (customer_name, post_code) VALUES\
			 (?, ?);", (f"{data['Фамилия']} {data['Имя']}", data['Почтовый код'])
		 )
	print(f"\033[32m\nДанные клиента {data['Фамилия']} {data['Имя']} добавлены\033[0m")


def delete_customer() -> None:
	print()
	data = {'Имя': '', 'Фамилия': ''}
	for k in data.keys():
		data[k] = input(f'{k}: ')
		
	with sqlite3.connect("accounts.db") as con:
		cur = con.cursor()
		
	# Get client ID
		try:
			customer_id = int(cur.execute(
 	 		    "SELECT id FROM clients WHERE customer_name = (?);",\
 	 		(f"{data['Фамилия']} {data['Имя']}",)).fetchone()[0])
		except:
			print(f"\033[31m\nПредупреждение: Учетной записи такого клиента нет!\033[0m")
			return	

		cur.execute("DELETE FROM clients WHERE customer_name = (?)\
				 AND id = (?);", (f"{data['Фамилия']} {data['Имя']}", customer_id))
		print(f"\033[32m\nДанные клиента {data['Фамилия']} {data['Имя']} удалены\033[0m")


def open_account() -> None:
	print()
	data = {'Имя': '', 'Фамилия': '', 'Валюта': '', 'Сумма взноса': ''}
	for k in data.keys():
		data[k] = input(f'{k}: ')
		
	with sqlite3.connect("accounts.db") as con:
		cur = con.cursor()
		
	# Get client ID
		try:
			customer_id = int(cur.execute(
 	 		    "SELECT id FROM clients WHERE customer_name = (?);",\
 	 		(f"{data['Фамилия']} {data['Имя']}",)).fetchone()[0])
		except:
			print(f"\033[31m\nПредупреждение: Сначала нужно открыть счет!\033[0m")
			return	
		
		cur.execute(
			 "INSERT INTO accounts (customer_name, currency,\
              amount, customer_id) VALUES\
			 (?, ?, ?, ?);", (f"{data['Фамилия']} {data['Имя']}",\
					  data['Валюта'], int(data['Сумма взноса']), customer_id)
		 )
	print(f"\033[32m\nНа счет клиента {data['Фамилия']} {data['Имя']}\
 внесено {data['Сумма взноса']} {data['Валюта']}\033[0m")


def show_accounts() -> None:
	print()
	with sqlite3.connect("accounts.db") as con:
		cur = con.cursor()
		res = cur.execute(		 
			"SELECT accounts.customer_name, clients.post_code,\
			accounts.id, accounts.currency, accounts.amount\
			FROM accounts JOIN clients WHERE\
			accounts.customer_id = clients.id;"
		).fetchall()
		[print(x) for x in res]


with sqlite3.connect("accounts.db") as con:
	cur = con.cursor()
	sqlite_query = '''
			CREATE TABLE IF NOT EXISTS clients (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			customer_name TEXT,
			post_code TEXT
			);
			
			CREATE TABLE IF NOT EXISTS accounts (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			customer_name TEXT,
			currency TEXT,
			amount INTEGER,
			customer_id INTEGER,
			FOREIGN KEY (customer_id) REFERENCES clients(id)
			);
		'''
	
	cur.executescript(sqlite_query)


while True:
	i = input('\n1 - Добавление пользователя\n2 - Открытие счета\
			   \n3 - Просмотр учетных записей\n4 - Удаление счета клиента\
			   \n5 - Выход из программы\n')
	if i == '5':
		break
	elif i == '1':
		add_customer()
	elif i == '2':
		open_account()
	elif i == '3':
		show_accounts()
	elif i == '4':
		delete_customer()
