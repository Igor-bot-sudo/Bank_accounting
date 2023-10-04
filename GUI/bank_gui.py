from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
import sqlite3


def hide_frames():
	[x.pack_forget() for x in frames]
	frame3.grid_forget()
	
def click_Home_btn():
	hide_frames()
	frame0.pack(padx = 5, pady = 5, fill = BOTH, expand = True)


rootwin = Tk()
rootwin.resizable(False, False)
screen_width = rootwin.winfo_screenwidth()
screen_height = rootwin.winfo_screenheight()
width, height = 675, 450
x = (screen_width//2) - (width//2)
y = (screen_height//2) - (height//2)
rootwin.geometry(f'{width}x{height}+{x}+{y}')
rootwin.title('XYZ Bank')

############################## FRAME0 ################################

def show_AddCustomer_frame():
	hide_frames()
	frame1.pack(padx = 5, pady = 5, fill = BOTH, expand = True)

def show_OpenAccount_frame():
	hide_frames()
	frame2.pack(padx = 5, pady = 5, fill = BOTH, expand = True)

def show_Customers_frame():
	hide_frames()

	with sqlite3.connect("accounts.db") as con:	
		cur = con.cursor()
		res = cur.execute(		 
			"SELECT accounts.customer_name, clients.post_code,\
			accounts.id, accounts.currency, accounts.amount\
			FROM accounts JOIN clients WHERE accounts.customer_id = clients.id;"
		).fetchall()
	total_rows = len(res)

	header = ('Customer name', 'Post code', 'ID', 'Currency', 'Amount')
	for i in range(len(header)):
		l = Label(frame3, width = 15, fg = '#00008b', borderwidth = 2,\
				relief = GROOVE,font = ('Calibri', 12, 'bold'))		
		l.grid(row = 1, column = i)
		l['text'] = header[i]

	for i in range(total_rows):
		for j in range(5):
			c = 255 - 30 * (i % 2)
			bg_color = f'#{c:02x}{c:02x}{c:02x}'
			l = Label(frame3, width = 15, fg = '#006400', bg = bg_color,\
			  borderwidth = 2,relief = GROOVE, anchor='w',\
			  font = ('Calibri', 12, 'bold'))			
			l.grid(row = i + 2, column = j)
			l['text'] = res[i][j]
	frame3.grid(padx = 5, pady = 5)

frame0 = ttk.Frame(borderwidth = 2, relief = SOLID,\
				 padding = [10, 10])
btn1 = ttk.Button(frame0, text = "Add Customer", width = 15,
				 command = show_AddCustomer_frame)
btn2 = ttk.Button(frame0, text = "Open Account", width = 15,
				 command = show_OpenAccount_frame)
btn3 = ttk.Button(frame0, text = "Customers", width = 15,
				 command = show_Customers_frame)
for i in (btn1, btn2, btn3):
	i.pack(side = LEFT, fill = X, expand = True, padx = 5, anchor = N)

############################## FRAME1 ################################

def click_AddCustomer_btn():
	first_name = first_name_var.get()
	last_name = last_name_var.get()
	post_code = post_code_var.get()
	first_name_var.set(value = '')
	last_name_var.set(value = '')
	post_code_var.set(value = '')
	
	with sqlite3.connect("accounts.db") as con:
		cur = con.cursor()
		cur.execute(
			"INSERT INTO clients (customer_name, post_code) VALUES\
			(?, ?);", (f'{last_name} {first_name}', post_code)
		)
	showinfo('', f'Данные клиента {first_name} {last_name} добавлены')


frame1 = ttk.Frame(borderwidth = 1, relief = SOLID,
					padding = [10, 10])

home_btn = ttk.Button(frame1, text = "Home",
					 command = click_Home_btn)
home_btn.pack(anchor = NW)

addCustomer_label = ttk.Label(frame1, text = "Add Customer",
							 font = ('Calibri', 18, 'bold'))
addCustomer_label.pack()

firstName_label = ttk.Label(frame1, text = " First Name:",
							 font = ( 'Calibri', 12, 'bold'))
firstName_label.pack(anchor = NW)

first_name_var = StringVar()
firstName_entry = ttk.Entry(frame1, font = ('Calibri', 12, 'bold'),
							 textvariable = first_name_var)
firstName_entry.pack(side = TOP, fill = X, anchor = NW)

lastName_label = ttk.Label(frame1, text = " Last Name:",
							font = ('Calibri', 12, 'bold'))
lastName_label.pack(anchor = NW)

last_name_var = StringVar()
lastName_entry = ttk.Entry(frame1, font = ('Calibri', 12, 'bold'),
							textvariable = last_name_var)
lastName_entry.pack(side = TOP, fill = X, anchor = NW)

postCode_label = ttk.Label(frame1, text = " Post Code:",
							font = ( 'Calibri', 12, 'bold'))
postCode_label.pack(anchor = NW)
post_code_var = StringVar()
postCode_entry = ttk.Entry(frame1, font = ('Calibri', 12, 'bold'),
							textvariable = post_code_var)
postCode_entry.pack(side = TOP, fill = X, anchor = NW)

addCustomer_btn = ttk.Button(frame1, text = "Add Customer",
							 command = click_AddCustomer_btn)
addCustomer_btn.pack(anchor = NW, pady = 10)

############################## FRAME2 ################################

def click_Process_btn():
	first_name = first_name_var2.get()
	last_name = last_name_var2.get()
	currency = currency_var.get()
	amount = amount_var.get()
	first_name_var2.set(value = '')
	last_name_var2.set(value = '')
	amount_var.set(value = '')

	customer_name = f'{last_name} {first_name}'
	with sqlite3.connect("accounts.db") as con:
		cur = con.cursor()
	# Get client ID
		try:
			customer_id = int(cur.execute(
 	 		    "SELECT id FROM clients WHERE customer_name = (?);",\
 	 		(customer_name,)).fetchone()[0])
		except:
			showerror('Предупреждение', 'Сначала нужно открыть счет!')
			return			

		cur.execute(
			"INSERT INTO accounts (customer_name, currency,\
			amount, customer_id) VALUES (?, ?, ?, ?);",\
	 	 	(customer_name, currency, amount, customer_id)
		)
	showinfo('', f'На счет клиента {last_name} {first_name} внесено {amount} {currency}')
	

frame2 = ttk.Frame(borderwidth = 1, relief = SOLID,
				 padding = [10, 10])

home_btn2 = ttk.Button(frame2, text = "Home",
						command = click_Home_btn)
home_btn2.pack(anchor = NW)

openAccount_label = ttk.Label(frame2, text = "Open account",
							 font = ( 'Calibri', 18))
openAccount_label.pack()

firstName_label2 = ttk.Label(frame2, text = " First Name:",
							 font = ('Calibri', 12, 'bold'))
firstName_label2.pack(anchor = NW)
first_name_var2 = StringVar()
firstName_entry2 = ttk.Entry(frame2, font = ('Calibri', 12, 'bold'),
							 textvariable = first_name_var2)
firstName_entry2.pack(side = TOP, fill = X, anchor = NW)

lastName_label2 = ttk.Label(frame2, text = " Last Name:",
							font = ( 'Calibri', 12, 'bold'))
lastName_label2.pack(anchor = NW)
last_name_var2 = StringVar()
lastName_entry2 = ttk.Entry(frame2, font = ('Calibri', 12, 'bold'),
							textvariable = last_name_var2)
lastName_entry2.pack(side = TOP, fill = X, anchor = NW)

currencies = ('Dollar', 'Pound', 'Rupee')

currency_label = ttk.Label(frame2, text = " Currency:",
							font = ('Calibri', 12, 'bold'))
currency_label.pack(anchor = NW)
currency_var = StringVar(value = currencies[0])
currency_combobox = ttk.Combobox(frame2, font = ('Calibri', 12, 'bold'),
					values = currencies, textvariable = currency_var)
currency_combobox.pack(side = TOP, fill = X, anchor = NW)

amount_label = ttk.Label(frame2, text = " Amount:",
							font = ('Calibri', 12, 'bold'))
amount_label.pack(anchor = NW)
amount_var = IntVar()
amount_entry = ttk.Entry(frame2, font = ('Calibri', 12, 'bold'),
							textvariable = amount_var)
amount_entry.pack(side = TOP, fill = X, anchor = NW)

process_btn = ttk.Button(frame2, text = "Process", command = click_Process_btn)
process_btn.pack(anchor = NW, pady = 10)

############################## FRAME3 ################################

frame3 = ttk.Frame(padding = [10, 10])
home_btn3 = ttk.Button(frame3, text = "Home",
						command = click_Home_btn)
home_btn3.grid(row = 0, column = 0, pady = 10)

######################################################################

frames = (frame0, frame1, frame2)
frame0.pack(padx = 5, pady = 5, fill = BOTH, expand = True)

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

rootwin.mainloop()
