import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3 
from tkinter import messagebox
import datetime
from class_app import *


def connect_db():
    global mydb
    mydb = sqlite3.connect('data.db')
    create_query = '''CREATE TABLE IF NOT EXISTS products 
                    (productid INTEGER PRIMARY KEY AUTOINCREMENT, 
                    productName VARCHAR NOT NULL, 
                    category VARCHAR NOT NULL, 
                    quantity INTEGER NOT NULL, 
                    price INTEGER NOT NULL)
                    '''
    create_query1 = '''CREATE TABLE IF NOT EXISTS orders 
                    (orderid INTEGER PRIMARY KEY AUTOINCREMENT, 
                    item_list VARCHAR NOT NULL,
                    quantity INTEGER NOT NULL,
                    datetime DATETIME NOT NULL, 
                    total INTEGER NOT NULL)
                   '''
    create_query2 = '''CREATE TABLE IF NOT EXISTS admins 
                    (adminid INTEGER PRIMARY KEY AUTOINCREMENT, 
                    fullname  VARCHAR NOT NULL,
                    phonenumber INTEGER,
                    username INTEGER NOT NULL, 
                    password INTEGER NOT NULL)
                   '''
    cursor = mydb.cursor()
    mydb.execute(create_query)
    mydb.execute(create_query1)
    mydb.execute(create_query2)


def active_btn(btn):
    btn.configure(bg = "#006fff")
def clear():
    name.delete(0, "end")
    quantity.delete(0, "end")
    category.current()
    price.delete(0, "end")
def update(rows):
    tree.delete(*tree.get_children())
    for i in rows:
            tree.insert('','end',iid=i[0], value = i)
def load_data():
    query = "SELECT * FROM products "
    cursor = mydb.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)
def add_product():
    product_name = name.get()
    product_quantity = quantity.get()
    product_price = price.get()
    product_price = price.get()
    product_category = category.get()

    if product_name == "" or product_quantity =="" or product_price =="" or product_category=="":
        messagebox.showerror("Error!", "Please Enter name, quantity, price and category!")
    else:
        new_product = Products(product_name, int(product_quantity), int(product_price), product_category)
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO products(productName, quantity, price, category) VALUES (?, ?, ?, ?)", 
                       (new_product.product_name, new_product.quantity, new_product.price, new_product.category))
        mydb.commit()
        load_data()
        clear()
def del_product():
    if messagebox.askyesno("Confirm?", "Are you sure?"):
        selected = tree.selection()[0]
        query = 'DELETE FROM products WHERE productid = ?'
        values = (selected,)
        cursor = mydb.cursor()
        cursor.execute(query,values)
        mydb.commit()
        load_data()
    else:
        return True

def search_product():
    product_name_search = search_entry.get()
    query = "SELECT * FROM products WHERE productName LIKE '%"+product_name_search+"%'"
    cursor = mydb.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)
def show_all():
    load_data()
    clear()
    btn_save_update.configure(state = 'disable')
    btn_show_detail.configure(state = 'active')
def show_detail():
    item = tree.item(tree.focus())
    name.insert(0,item['values'][1])
    category.insert(0,item['values'][2])
    quantity.insert(0,item['values'][3])
    price.insert(0,item['values'][4])
    btn_save_update.configure(state = 'active')
    btn_show_detail.configure(state = 'disable')

def update_product():
    product_name = name.get()
    new_product_quantity = quantity.get()
    new_product_price = price.get()
    new_product_category = category.get()
    query = 'UPDATE products SET price = ?, quantity = ?, category = ? WHERE productName = ?'
    cursor = mydb.cursor()
    cursor.execute(query,(new_product_price, new_product_quantity, new_product_category, product_name))
    mydb.commit()
    load_data()
    clear()
    category.current()
    btn_save_update.configure(state = 'disable')
    btn_show_detail.configure(state = 'active')
    show_all()
#sale page    
def chose_item():
    item = tree.item(tree.focus())
    item_name.insert(0,item['values'][1])
def del_item():
    item_name.delete(0,"end")
    quantity_buy.delete(0,"end")
def add_to_bill():
    item_chose = []
    item = tree.item(tree.focus())
    product_name = item['values'][1]
    product_price =  item['values'][4]
    quantity_item_select = quantity_buy.get()
    
    tt_quantity = int(total_quantity.get()) + int(quantity_item_select)
    sum_item_price = int(product_price) * int(quantity_item_select)
    tt_price = sum_item_price + int(total_price.get())
    
    total_quantity.delete(0,"end")
    total_price.delete(0,"end")
    
    total_quantity.insert(0,tt_quantity)
    total_price.insert(0,tt_price) 
    product_item = (product_name, product_price, quantity_item_select, sum_item_price)
    #ADD TO TREEVIEW
    item_chose.append(product_item)
    for i in item_chose:
        tree_order.insert('','end',iid=i[0], value = i)
        
    product_name = item['values'][1]
    quantity_item_select = quantity_buy.get()
    new_quantity = item['values'][3] - int(quantity_item_select)
    query = 'UPDATE products SET quantity = ? WHERE productName = ?'
    cursor = mydb.cursor()
    cursor.execute(query,(new_quantity, product_name))
    mydb.commit()
    load_data()
    
    item_name.delete(0,"end")
    quantity_buy.delete(0,"end")
def return_to_list():
    item = tree_order.item(tree_order.focus())
    product_name = item['values'][0]
    quantity_on_bill = item['values'][2] 
    sum_item_price = item['values'][3] 
    cursor = mydb.cursor()
    cursor.execute("SELECT quantity FROM products WHERE productName = ?", (product_name,))
    result = cursor.fetchone()
    quantity_org = result[0]
    update_quantity = quantity_on_bill + quantity_org
    update_query = 'UPDATE products SET quantity = ? WHERE productName = ?'
    cursor.execute(update_query,(update_quantity, product_name) )
    mydb.commit()
    load_data()
    
    selected_item = tree_order.selection()[0]
    tree_order.delete(selected_item)
    tt_quantity = int(total_quantity.get()) - int(quantity_on_bill)
    tt_price =  int(total_price.get()) - sum_item_price 
    
    total_quantity.delete(0,"end")
    total_price.delete(0,"end")
    
    total_quantity.insert(0,tt_quantity)
    total_price.insert(0,tt_price) 
def create_order():
    product_name_list = []
    current_time = str(datetime.datetime.now())
    tt_quantity = total_quantity.get()
    tt_price = total_price.get()
    
    data = [tree_order.item(child)["values"] for child in tree_order.get_children()]
    for row in data:
        product_name_list.append(row[0])
    new_order = Orders(product_name_list,tt_quantity, current_time, tt_price)
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO orders(item_list, quantity, datetime, total) VALUES (?, ?, ?, ?)", 
                   (str(new_order.item), new_order.quantity, new_order.datetime, new_order.total))
    mydb.commit()
    messagebox.showinfo("Success!", "New order is created!. Check it in order page")
    for child in tree_order.get_children():
        tree_order.delete(child)
    total_quantity.delete(0,"end")
    total_price.delete(0,"end")
    total_quantity.insert(0,"0")
    total_price.insert(0,"0")
#add user page
def register():
    full_name = fullname.get()
    phone_number = phonenumber.get()
    user_name = username.get()
    user_password = password.get()
    user_re_password = repassword.get()
    
    if full_name =="" or user_name =="" or user_password == "":
        messagebox.showerror("Register failed!", "Please enter fullname, username and password")
    else:
        if user_re_password == user_password:
            new_admin = Admins(full_name, phone_number, user_name, user_password)
            cursor = mydb.cursor()
            cursor.execute('''INSERT INTO admins(fullname, phonenumber, username, password) 
                                VALUES(?, ?, ?, ?)''',
                           (new_admin.full_name, new_admin.phone_number, new_admin.username, new_admin.password))
            mydb.commit()
            query = "SELECT * FROM admins"
            cursor = mydb.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            user_tree.delete(*user_tree.get_children())
            for i in rows:
                user_tree.insert('','end',iid=i[0], value = i)
            messagebox.showinfo("Register success!", "New admin account is created!")
            register_page.destroy()
        else:
            messagebox.showerror("Register failed!", "repassword do not match password!")
def del_admin():
    if messagebox.askyesno("Confirm?", "Are you sure?"):
        selected = user_tree.selection()[0]
        query = 'DELETE FROM admins WHERE adminid = ?'
        values = (selected,)
        cursor = mydb.cursor()
        cursor.execute(query,values)
        mydb.commit()
        query = "SELECT * FROM admins"
        cursor = mydb.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        user_tree.delete(*user_tree.get_children())
        for i in rows:
                user_tree.insert('','end',iid=i[0], value = i)   
    else:
        return True

def login():
    mydb = sqlite3.connect('data.db')
    username = username_entry.get()
    password = password_entry.get()
    global current_user
    
    if username != "" or password != "":
        if username == "admin" and password == "12345":
            current_user = "admin"
            main_app()
        else:
            cursor = mydb.cursor()
            cursor.execute( "SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            if result:
                current_user = result[1]
                main_app()
            else:
                messagebox.showerror("Login failed!", "Username or password is incorrect!")
    else:
        messagebox.showerror("Login failed!", "Please, enter username and password !")
        
def logout():
    app.destroy()
    login_page()
def add_number(number):
    quantity_buy.insert(tk.END, str(number))
def delete_number():
    quantity_buy.delete(len(quantity_buy.get())-1)


def login_page():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x250+550+200")
    login_window.iconbitmap('myIcon.ico')
    login_window.resizable(width=False, height=False)
    

    global username_entry
    global password_entry
    
    login_frame = tk.Frame(login_window, padx = 30, pady=15)
    lbl_login = tk.Label(login_frame, text = "LOGIN",font=("", 15, "bold"))
    
    username_label = tk.Label(login_frame, text="Username:", font=("", 10, "bold"))
    username_entry = tk.Entry(login_frame)
    password_label = tk.Label(login_frame, text="Password:", font=("", 10,"bold"))
    password_entry = tk.Entry(login_frame, show="*")
    login_button = tk.Button(login_frame, text="Login", bd=0, bg = '#7FB3D5',
                             height = 2, width = 15, command=login)

    lbl_noitify = tk.Label(login_frame, text="Account default: admin - 12345", font=("", 8,"bold"))
    login_frame.grid(row = 0, column = 0)
    lbl_login.grid(row =1, column = 1, columnspan = 2)
    username_label.grid(row = 2, column = 1)
    username_entry.grid(row = 2, column = 2)
    password_label.grid(row = 3, column = 1)
    password_entry.grid(row = 3, column = 2)
    login_button.grid(row = 4, column = 1, columnspan = 2)
    lbl_noitify.grid(row = 5, column =1, columnspan = 2)
    for w in login_frame.winfo_children():
        w.grid_configure(padx = 7, pady = 10)
    login_window.mainloop()

def main_app():
    connect_db()
    login_window.destroy()
    global app
    app = tk.Tk()
    app.iconbitmap('myIcon.ico')
    app.resizable(width=False, height=False)

    def remove_widget():
        for w in app.winfo_children():
            w.destroy()
    def sale_page():
        remove_widget()
        app.title("Sale page")
        app.geometry("1400x600+50+100")
        global tree
        global tree_order
        global total_quantity
        global total_price
        global item_name
        global quantity_buy
        #nav
        nav = tk.Frame(app, bg = '#023047')
        nav.pack(side = tk.TOP, fill="both")
        nav.pack_propagate(False)
        nav.config(width = 1400, height = 60)
        #btn
        btn_sale_page = tk.Button(nav, text ="Sale", bd = 0, height = 2, width = 15,
                                  command = sale_page)
        btn_product_page = tk.Button(nav, text ="Product",bd = 0, height = 2, width = 15, 
                                     command = product_page)
        btn_order_page = tk.Button(nav, text ="ORDER", bd=0, height = 2, width = 15, 
                                   command = order_page)
        btn_user_page = tk.Button(nav, text ="USERS", bd=0, height = 2, width = 15, 
                                           command = user_page)
        hello_lbl = tk.Label(nav, text = f"Hello {current_user}", bd=0, height = 2, width = 15, pady = 3)
        btn_logout = tk.Button(nav, text ="Logout", bd=0, height = 2, width = 15, command = logout)
        #place
        btn_sale_page.place(x = 20, y = 10)
        btn_product_page.place(x = 200, y = 10)
        btn_order_page.place(x = 380, y = 10)
        btn_user_page.place(x = 560, y = 10)
        hello_lbl.place(x = 1150, y = 10)
        btn_logout.place(x = 1280, y = 10)
        
        #main
        main_frame = tk.Frame(app, padx = 30)
        main_frame.pack( fill="both", expand="yes")
        main_frame.pack_propagate(False)
        main_frame.config(width = 1400, height = 540)
        #right frame
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side =tk.RIGHT, fill="both", expand="yes")
        right_frame.pack_propagate(False)
        right_frame.config(width = 700, height = 540)
        #left frame
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side = tk.LEFT, fill="both", expand="yes")
        left_frame.pack_propagate(False)
        left_frame.config(width = 700, height = 540)

        columns = ('product_id', 'product_name', 'category', 'quantity', 'price')
        tree = ttk.Treeview(left_frame, columns = columns, show = 'headings', height = 12)
        #tree column
        tree.column("#0", width=300)
        tree.column("product_id", width=100)
        tree.column("product_name", width=250)
        tree.column("#3", width=0, stretch=False)
        tree.column("quantity", width=130)
        tree.column("price", width=150)
        #tree headings
        tree.heading('product_id', text = 'ID')
        tree.heading('product_name', text = 'Product Name')
        tree.heading('category', text = 'Category')
        tree.heading('quantity', text = 'Quantity')
        tree.heading('price', text = 'Price')
        for i in range(1, 6):
            tree.column("#"+str(i), anchor=tk.CENTER)
        load_data()
        #bottom_frame
        bottom_frame = tk.Frame(left_frame)
        bottom_frame.pack(side = tk.BOTTOM, fill="both", expand="yes")
        bottom_frame.pack_propagate(False)
        bottom_frame.config(width = 700)
        #widget
        info_frame = tk.LabelFrame(bottom_frame,text = "INFO ITEM")
        lbl_item_name = tk.Label(info_frame, text="Item: ")
        item_name = tk.Entry(info_frame,bd=0, bg="#E9E9E9",width=12 , font=("", 15, "bold"))
        lbl_quantity_buy = tk.Label(info_frame, text = "quantity")
        quantity_buy = tk.Entry(info_frame)
        number_pad_frame = tk.Frame(bottom_frame)
        delete_button = tk.Button(info_frame, text="X", bd=0, bg = '#C74331', 
                                  height = 1, width = 4, command=delete_number)
        btn_del_item= tk.Button(bottom_frame, text ="DELETE ITEM", bd=0, bg = '#C74331', 
                             height = 2, width = 14, command = del_item)
        btn_chose= tk.Button(bottom_frame, text ="CHOSE ITEM", bd=0, bg = '#FFC000', 
                             height = 2, width = 14, command = chose_item)
        btn_add_bill= tk.Button(bottom_frame, text ="ADD BILL", bd=0, bg = '#0070C0', 
                                height = 2, width = 14, command = add_to_bill)
        #create button 0-9
        for i in range(1, 11):
            if i == 10:
                k = i -10
                button = tk.Button(number_pad_frame, text=str(k), bd=0,bg = '#6296b7', font=("",10,"bold"),
                               height = 2, width = 20, command=lambda k=k: add_number(k))
                button.grid(row=(i-1)//3, column=(i)%3)
            else:
                button = tk.Button(number_pad_frame, text=str(i), bd=0,bg = '#6296b7', font=("",10,"bold"),
                                   height = 2, width = 20, command=lambda i=i: add_number(i))
                button.grid(row=(i-1)//3, column=(i-1)%3)
        #treeview
        columns = ('product_name', 'price', 'quantity', "total")
        tree_order = ttk.Treeview(right_frame, columns = columns, show = 'headings', height = 12)
        #tree column
        tree_order.column("#0", width=300)
        tree_order.column("product_name", width=200)
        tree_order.column("price", width=150)
        tree_order.column("quantity", width=130)
        tree_order.column("total", width=130)
        #tree headings
        tree_order.heading('product_name', text = 'Product Name')
        tree_order.heading('price', text = 'Price')
        tree_order.heading('quantity', text = 'Quantity')
        tree_order.heading('total', text = 'Total')
        for i in range(1, 5):
            tree_order.column("#"+str(i), anchor=tk.CENTER)
            
        btm_right_frame = tk.Frame(right_frame)
        btm_right_frame.pack(side = tk.BOTTOM, fill="both", expand="yes")
        btm_right_frame.pack_propagate(False)
        btm_right_frame.config(width = 700)
        total_bill = tk.LabelFrame(btm_right_frame, text ="TOTAL INFO")
        total_quantity_lbl = tk.Label(total_bill, text = "Total Quantity") 
        total_quantity = tk.Entry(total_bill,bd=0, bg="#E9E9E9",width=15 , font=("", 15, "bold")) 
        total_quantity.insert(0,"0")
        total_price_lbl = tk.Label(total_bill, text = "Total Price") 
        total_price = tk.Entry(total_bill,bd=0, bg="#E9E9E9",width=15 , font=("", 15, "bold")) 
        total_price.insert(0,"0")
        btn_create_order = tk.Button(btm_right_frame, text ="CREATE ORDER", bd=0, bg ='#00971f',height = 2, width = 15,
                            command = create_order)
        btn_return = tk.Button(btm_right_frame, text ="RETURN ITEM", bd=0, bg ='#C74331',height = 2, width = 15,
                            command = return_to_list)
        #grid left-frame
        tree.grid(padx = 15, pady = 15, row =1, column =1, columnspan = 5)
        bottom_frame.grid(row = 6, column = 1, columnspan = 5, sticky="nsew")
        info_frame.grid(row = 1, column =1, rowspan = 4)
        number_pad_frame.grid(row = 5, column = 1, columnspan = 3, sticky ="w")
        btn_del_item.grid(row = 3, column=2, columnspan =3, sticky = "e")
        btn_chose.grid( row = 4, column = 2, columnspan = 3, sticky ="e")
        btn_add_bill.grid( row= 5, column = 2, columnspan = 3, sticky ="e")
        for widget in info_frame.winfo_children():
            widget.grid_configure(padx = 11, pady = 8, ipady=4)    
        for widget in bottom_frame.winfo_children():
            widget.grid_configure(padx = 10, ipadx=5)  
        #grid right-frame
        lbl_item_name.grid(row = 1, column=1)
        item_name.grid(row = 1, column = 2)
        lbl_quantity_buy.grid(row = 1, column = 3)
        quantity_buy.grid(row = 1, column = 4)
        delete_button.grid(row=1, column=5)     
        tree_order.grid(padx = 15, pady = 15, row =1, column =1, columnspan = 5)
        btm_right_frame.grid(row = 6, column = 1, columnspan = 5,padx = 10, ipady = 15, sticky="nsew")
        total_bill.grid(row=1, column =1, rowspan = 3)
        for widget in total_bill.winfo_children():
            widget.grid_configure(padx = 10, pady = 10, ipady=5)    
        
        total_quantity_lbl.grid(row=1, column = 1)
        total_quantity.grid(row = 1, column = 2)
        total_price_lbl.grid(row=1, column = 3)
        total_price.grid(row = 1, column = 4)
        
        btn_create_order.grid(row=4, column = 1, sticky ="w")
        btn_return.grid(row=5, column = 1, sticky ="w")
        
    def product_page():
        remove_widget()
        app.title("Product page")
        app.geometry("1400x600")
        global name
        global quantity
        global price
        global category
        global btn_save_update
        global btn_show_detail
        global search_entry
        global tree
        
        #nav
        nav = tk.Frame(app, bg = '#023047')
        nav.pack(side = tk.TOP, fill="both")
        nav.pack_propagate(False)
        nav.config(width = 1400, height = 60)
        
        btn_sale_page = tk.Button(nav, text ="Sale", bd = 0, height = 2, width = 15,
                                  command = sale_page)
        btn_product_page = tk.Button(nav, text ="Product",bd = 0, height = 2, width = 15, 
                                     command = product_page)
        btn_order_page = tk.Button(nav, text ="ORDER", bd=0, height = 2, width = 15, 
                                   command = order_page)
        btn_user_page = tk.Button(nav, text ="USERS", bd=0, height = 2, width = 15, 
                                           command = user_page)
        hello_lbl = tk.Label(nav, text = f"Hello {current_user}", bd=0, height = 2, width = 15, pady = 3)
        btn_logout = tk.Button(nav, text ="Logout", bd=0, height = 2, width = 15, 
                                           command = logout)
        btn_sale_page.place(x = 20, y = 10)
        btn_product_page.place(x = 200, y = 10)
        btn_order_page.place(x = 380, y = 10)
        btn_user_page.place(x = 560, y = 10)
        hello_lbl.place(x = 1150, y = 10)
        btn_logout.place(x = 1280, y = 10)
        
        #main
        main_frame = tk.Frame(app, padx = 30, pady = 20)
        main_frame.pack( fill="both", expand="yes")
        main_frame.pack_propagate(False)
        main_frame.config(width = 1400, height = 540)
        #left frame
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side = tk.LEFT, fill="both", expand="yes")
        left_frame.pack_propagate(False)
        left_frame.config(width = 500, height = 540)
        #right frame
        right_frame = tk.Frame(main_frame, pady = 10)
        right_frame.pack(side =tk.RIGHT, fill="both", expand="yes")
        right_frame.pack_propagate(False)
        right_frame.config(width = 1000, height = 540)
        
        #product-page
        wrapper = tk.LabelFrame(left_frame, text="INFOMATION", height = 400, width = 20, pady = 10)
        lbl_name = tk.Label(wrapper, text ="Product Name")
        lbl_quantity = tk.Label(wrapper, text ="Quantity")
        lbl_price = tk.Label(wrapper, text = "Price")
        lbl_category = tk.Label(wrapper, text = "Category")
        name = tk.Entry(wrapper)
        quantity = tk.Entry(wrapper)
        price = tk.Entry(wrapper)
        n = tk.StringVar()
        category = ttk.Combobox(wrapper, width = 27, textvariable = n)
        # Adding combobox drop down list
        category['values'] = (' Drinks ', ' Flour', ' Desserts', ' Snacks',
                              ' Ingredient (oil, soy sauce, fish sauce) ',
                              ' Sugar & salt ','Dry food'
                             )
        

        wrapper_btn = tk.LabelFrame( left_frame, text="ACTION ", height = 200, width = 500,
                                    bd =5,bg='#F7F7F7', pady = 25 )
        btn_add = tk.Button( wrapper_btn, text ="ADD NEW", bd=0, bg = '#6296b7',height = 2, width = 15, 
                            command = add_product)
        btn_del = tk.Button( wrapper_btn, text ="DELETE", bd=0, bg = '#d24a46', height = 2, width = 15, 
                            command = del_product )
        
        btn_save_update = tk.Button( wrapper_btn, text ="SAVE UPDATE", bd=0, bg = '#7FB3D5', 
                                    height = 2, width = 15, state = "disabled", 
                                    command = update_product )
        btn_show_detail = tk.Button( wrapper_btn, text = "DETAILS", bd=0, bg = '#7FB3D5',
                                    height = 2, width = 15, 
                                    command = show_detail )
        btn_all = tk.Button( wrapper_btn, text = "ALL", bd=0, bg = '#7FB3D5',height = 2, width = 5, 
                            command = show_all)
        
        #top frame
        top_frame = tk.Frame(right_frame, padx = 20)
        
        btn_search = tk.Button(top_frame, text = "SEARCH", bd=0, bg = '#7FB3D5', height = 2, width = 15, 
                               command = search_product )
        search_entry = tk.Entry(top_frame, width = 50)
    
        #treeview
        columns = ('product_id', 'product_name','category', 'quantity', 'price')
        tree = ttk.Treeview(right_frame, columns = columns, show = 'headings', height = 20)
        #tree column
        tree.column("#0", width=300)
        tree.column("product_id", width=50)
        tree.column("product_name", width=280)
        tree.column("category", width=230)
        tree.column("quantity", width=130)
        tree.column("price", width=150)
        #tree hêadings
        tree.heading('product_id', text = 'ID')
        tree.heading('product_name', text = 'Product Name')
        tree.heading('category', text = 'Category')
        tree.heading('quantity', text = 'Quantity')
        tree.heading('price', text = 'Price')
        for i in range(1, 6):
            tree.column("#"+str(i), anchor=tk.CENTER)
        load_data()
        #grid widget
        #left-frame
        wrapper.grid(row =1, column =1, sticky ='ew')
        lbl_name.grid( row = 2, column = 1, sticky = "w")
        name.grid( row = 3, column = 1)
        lbl_quantity.grid( row = 4, column = 1, sticky = "w")
        quantity.grid( row = 5, column = 1)
        lbl_category.grid( row = 2, column = 2, sticky = "w")
        category.grid( row = 3, column = 2)
        lbl_price.grid( row = 4, column = 2, sticky = "w")
        price.grid( row = 5, column = 2, sticky = "w")
        for widget in wrapper.winfo_children():
            widget.grid_configure(padx = 10, pady = 5, ipady=2)    
            
        wrapper_btn.grid(pady = 10, row =2, column =1,  sticky ='ew')    
        btn_add.grid(row =1, column =1)
        btn_del.grid(row =2, column =1)
        btn_all.grid(row =3, column =1) 
        btn_save_update.grid(row =2, column =2)
        btn_show_detail.grid(row =3, column =2)
        for widget in wrapper_btn.winfo_children():
            widget.grid_configure(padx = 50, pady=20)
        #right_frame
        top_frame.grid(row =1, column = 1)
        btn_search.grid(row =1, column =1)
        search_entry.grid(row = 1, column = 2, ipady = 6)
        tree.grid(padx = 15, pady = 15, row =2, column =1, columnspan = 30)

    def order_page():
        remove_widget()
        app.title("Order page")
        app.geometry("1400x600")
        

        nav = tk.Frame(app, bg = '#023047')
        nav.pack(side = tk.TOP, fill="both")
        nav.pack_propagate(False)
        nav.config(width = 1400, height = 60)
        
        btn_sale_page = tk.Button(nav, text ="Sale", bd = 0, height = 2, width = 15,
                                  command = sale_page)
        btn_product_page = tk.Button(nav, text ="Product",bd = 0, height = 2, width = 15, 
                                     command = product_page)
        btn_order_page = tk.Button(nav, text ="ORDER", bd=0, height = 2, width = 15, 
                                   command = order_page)
        btn_user_page = tk.Button(nav, text ="USERS", bd=0, height = 2, width = 15, 
                                           command = user_page)
        hello_lbl = tk.Label(nav, text = f"Hello {current_user}", bd=0, height = 2, width = 15, pady = 3)
        btn_logout = tk.Button(nav, text ="Logout", bd=0, height = 2, width = 15, 
                                           command = logout)
        btn_sale_page.place(x = 20, y = 10)
        btn_product_page.place(x = 200, y = 10)
        btn_order_page.place(x = 380, y = 10)
        btn_user_page.place(x = 560, y = 10)
        hello_lbl.place(x = 1150, y =10)
        btn_logout.place(x = 1280, y =10)
        
        #main
        main_frame = tk.Frame(app, padx = 20, pady = 15)
        main_frame.pack( fill="both", expand="yes")
        main_frame.pack_propagate(False)
        main_frame.config(width = 1400, height = 540)
        #line chart
        mydb = sqlite3.connect('data.db')
        cursor = mydb.cursor()
        cursor.execute("SELECT date(datetime), COUNT(orderid) FROM orders GROUP BY date(datetime)")
        data = cursor.fetchall()
        x = [row[0] for row in data]
        y = [row[1] for row in data]
        fig = plt.Figure(figsize=(5,2))
        ax = fig.add_subplot(111)
        ax.set_ylabel('quantity order')
        ax.set_yticks(range(0, max(y)+1))
        ax.plot(x, y)
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        cursor.execute('SELECT total FROM orders')
        rows = cursor.fetchall()
        total = sum(int(row[0]) for row in rows)
        #revenue card
        card_1 = tk.Frame(main_frame, highlightbackground="#24613b",highlightthickness =5, width = 250, height = 200)
        title_card_1 = tk.Label(card_1, text = "Revenue", fg ="#24613b",font = ("", 15, "bold"))  
        text_card_1 = tk.Label(card_1, text = f"{total}",fg= "#24613b",font = ("", 25, "bold"))  
        canvas.get_tk_widget().grid(row=1, column=1)
        card_1.grid(row = 1, column = 2, padx = 10)
        title_card_1.place(x = 20, y =20)
        text_card_1.place(x = 70, y = 80)
        #treeview
        global tree
        columns = ('order_id','item_list', 'quantity_item', 'datetime', 'total')
        tree = ttk.Treeview(main_frame, columns = columns, show = 'headings', height = 10)
        #tree column
        tree.column("#0", width=300)
        tree.column("order_id", width=350)
        tree.column("item_list", width=200)
        tree.column("quantity_item", width=200)
        tree.column("datetime", width=350)
        tree.column("total", width=200)
        #tree headings
        tree.heading('order_id', text = 'Order ID')
        tree.heading('item_list', text = 'Item List')
        tree.heading('quantity_item', text = 'Quantity Item')
        tree.heading('datetime', text = 'DateTime')
        tree.heading('total', text = 'Total Price')
        #set align center
        for i in range(1, 6):
            tree.column("#"+str(i), anchor=tk.CENTER)
        query = "SELECT * FROM orders"
        cursor = mydb.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        update(rows)
        tree.grid(padx = 15, pady = 15, row =2, column =1, columnspan = 30, sticky = "nsew")
        
    def register_page():
        global register_page
        register_page = tk.Tk()
        register_page.title("Add User")
        register_page.geometry("400x300+500+200")
        global fullname
        global phonenumber
        global username
        global password
        global repassword
        lbl_register = tk.Label(register_page, text = "REGISTER", font=("", 15, "bold"))
        regiter_frame = tk.Frame(register_page)
        lbl_fullname = tk.Label(regiter_frame, text="Fullname:")
        fullname = tk.Entry(regiter_frame)
        lbl_phonenumber = tk.Label(regiter_frame, text="Phone number:")
        phonenumber = tk.Entry(regiter_frame)     
        username_label = tk.Label(regiter_frame, text="Username:")
        username = tk.Entry(regiter_frame)
        password_label = tk.Label(regiter_frame, text="Password:")
        password = tk.Entry(regiter_frame, show="*")
        repassword_label = tk.Label(regiter_frame, text="Enter password again:")
        repassword = tk.Entry(regiter_frame, show="*")
        register_button = tk.Button(regiter_frame, text="Register", bd=0, bg = '#7FB3D5',
                                    height = 2, width = 15, command=register)
        #grid
        lbl_register.grid(row =1, column =1, columnspan = 2)
        regiter_frame.grid(row = 2, column = 2, ipadx = 15)
        lbl_fullname.grid(row = 1, column =1)
        fullname.grid(row = 1, column =2)
        lbl_phonenumber.grid(row = 2, column =1)
        phonenumber.grid(row = 2, column =2)
        username_label.grid(row = 3, column =1)
        username.grid(row = 3, column =2)
        password_label.grid(row = 4, column =1)
        password.grid(row = 4, column =2)
        repassword_label.grid(row = 5, column =1)
        repassword.grid(row = 5, column =2)
        register_button.grid(row = 6, column =1, columnspan = 2)
        for w in regiter_frame.winfo_children():
            w.grid_configure(padx = 30, pady =10)
        register_page.mainloop()    
    def user_page():
        remove_widget()
        app.title("User page")
        app.geometry("1400x600")
        nav = tk.Frame(app, bg = '#023047')
        nav.pack(side = tk.TOP, fill="both")
        nav.pack_propagate(False)
        nav.config(width = 1400, height = 60)
        
        btn_sale_page = tk.Button(nav, text ="Sale", bd = 0, height = 2, width = 15,
                                  command = sale_page)
        btn_product_page = tk.Button(nav, text ="Product",bd = 0, height = 2, width = 15, 
                                     command = product_page)
        btn_order_page = tk.Button(nav, text ="ORDER", bd=0, height = 2, width = 15, 
                                   command = order_page)
        btn_user_page = tk.Button(nav, text ="USERS", bd=0, height = 2, width = 15, 
                                   command = user_page)
        hello_lbl = tk.Label(nav, text = f"Hello {current_user}", bd=0, height = 2, width = 15, pady = 3)
        btn_logout = tk.Button(nav, text ="Logout", bd=0, height = 2, width = 15, 
                                                   command = logout)
        btn_sale_page.place(x = 20, y = 10)
        btn_product_page.place(x = 200, y = 10)
        btn_order_page.place(x = 380, y = 10)
        btn_user_page.place(x = 560, y = 10)
        hello_lbl.place(x = 1150, y = 10)
        btn_logout.place(x = 1280, y = 10)
        #main
        main_frame = tk.Frame(app, pady = 10)
        main_frame.pack( fill="both", expand="yes")
        main_frame.pack_propagate(False)
        main_frame.config(width = 1400, height = 540)
        #top frame
        top_frame = tk.Frame(main_frame, padx = 20)
        
        tbn_add_user = tk.Button(top_frame, text = "ADD USER",bd=0, bg = '#7FB3D5', 
                                 height = 2, width = 15, command = register_page)
        tbn_view_user = tk.Button(top_frame, text = "VIEW USER",bd=0, bg = '#FFC000', 
                                  height = 2, width = 15, state ="disabled")
        tbn_delete_user = tk.Button(top_frame, text = "DELETE USER",bd=0, bg = '#C74331', 
                                    height = 2, width = 15, command = del_admin)
        
        top_frame.grid(row =1, column = 1, columnspan = 3)
        tbn_add_user.grid(row = 1, column = 1)
        tbn_view_user.grid(row = 1, column = 2)
        tbn_delete_user.grid(row = 1, column = 3)
        
        columns = ('user_id','name', 'phone_number', 'username', 'password')
        global user_tree
        user_tree = ttk.Treeview(main_frame, columns = columns, show = 'headings', height = 10)
        #tree column
        user_tree.column("#0", width=300)
        user_tree.column("user_id", width=100)
        user_tree.column("name", width=200)
        user_tree.column("phone_number", width=200)
        user_tree.column("username", width=200)
        user_tree.column("password", width=200)
        #tree headings
        user_tree.heading('user_id', text = 'User ID')
        user_tree.heading('name', text = 'Name')
        user_tree.heading('phone_number', text = 'Phone number')
        user_tree.heading('username', text = 'Username')
        user_tree.heading('password', text = 'Password')
        #set align center
        for i in range(1, 5):
            user_tree.column("#"+str(i), anchor=tk.CENTER)
        query = "SELECT * FROM admins"
        cursor = mydb.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        user_tree.delete(*user_tree.get_children())
        for i in rows:
            user_tree.insert('','end',iid=i[0], value = i)
        user_tree.grid(padx = 15, pady = 15, row =2, column =2, columnspan = 30)
        
    sale_page()
    app.mainloop()    
login_page()