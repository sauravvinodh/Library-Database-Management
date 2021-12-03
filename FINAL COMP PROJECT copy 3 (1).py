# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 15:28:53 2020

@author: sauravsoham
"""

"""BOOKSTORE MANAGEMENT SYSTEM IN PYTHON AND WITH MYSQL DATABASE
FOR: CBSE PROJECT 2020-21
BY: SAURAV VINODH AND SOHAM VAKANI
DATE: 25TH OCTOBER 2020  """


#IMPORTING THE TWO MAIN MODULES TKINTER(for gui) and MYSQL.CONNECTOR(for python-sql connectivity).

import tkinter as tk

import mysql.connector as sqlcon

#to create database BOOKSTORE IF IT DOESNT EXIST
mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql')
cursor=mycon.cursor()
st="create database bookstore if not exists"
cursor.execute(st)

#to create tables INVENTORY,PURCHASE,WISHLIST,BILL
mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql')
cursor=mycon.cursor()
table1="create table inventory if not exists (sno int not null auto_increment, book_name varchar(120) not null, author varchar(120) not null, stock int, price1_aed float not null, unique(book_name), primary key(sno));"
table2="create table purchase if not exists (pid int not null auto_increment, DOP date, book_name varchar(120) not null, quantity int not null default 1, price1_aed float, total_aed float, primary key(pid), foreign key (book_name) references inventory(book_name));"
table3="create table wishlist if not exists (ISBN bigint not null, book_name varchar(120) not null, author varchar(120) not null, primary key(ISBN));"
table4="create table bill if not exists(bid bigint not null auto_increment primary key, DOP datetime default CURRENT_TIMESTAMP, cname varchar(120) not null,quantity int default 1, totalprice int default 30, vat_5 float default 1.5) ;"
cursor.execute(table1)
cursor.execute(table2)
cursor.execute(table3)
cursor.execute(table4)

#to insert values into INVENTORY TABLE
mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql')
cursor=mycon.cursor()
insert1 ="insert into inventory values (1,'Computer Science', 'Sumita Arora',5,200); "
insert2 ="insert into inventory values(2,'Grade 12 Mathematics','RD Sharma',10,500);"
insert3 ="insert into inventory values(3, 'Grade 12 PhysicS', 'HC Verma',15,300);"
cursor.execute(insert1)
cursor.execute(insert2)
cursor.execute(insert3)


#FUNCTION TO INSERT VALUES INPUTTED BY ADMIN INTO INVENTORY TABLE

def inserttable1(name,author,stock,price):
    mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
    cursor=mycon.cursor()
    st="select * from inventory"
    cursor.execute(st)
    data=cursor.fetchall()
    for i in data:
        if i[1]==name:
            st="update inventory set stock=stock+{} where book_name='{}'".format(stock,name)
            print(st)
            cursor.execute(st)
            mycon.commit()
            break
    else:    
        st="insert into inventory(book_name,author,stock,price1_aed) values('{}','{}',{},{})".format(name,author,stock,price)
        cursor.execute(st)
    mycon.commit()

#FUNCTION THAT WORKS WITH PURCHASE TABLE AND PERFORMS VARIOUS FUNCTIONS
    
def inserttable2(bookname,quantity):
   
    mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
    cursor=mycon.cursor()
    st="insert into purchase(book_name,quantity)values('{}',{})".format(bookname,quantity)
    cursor.execute(st)
    mycon.commit()
    
    #Inserting the price of 1 book into the 'Purchase' table from our 'Inventory' table
    
    st="update purchase set price1_aed=(select price1_aed from inventory where inventory.book_name='{}')  where book_name='{}'".format(bookname,bookname)
    cursor.execute(st)
    mycon.commit()
    
    #Setting the date of insertion as a default value for the date of purchase(DOP) column
    
    st="update purchase set DOP=date(current_timestamp) where book_name='{}'".format(bookname)
    cursor.execute(st)
    mycon.commit()
    
    #Setting the total column as the product of price*quantity
    
    cursor.execute("select * from inventory")
    data=cursor.fetchall()
    for i in data:
        if i[1]==bookname:
            price_of_1=i[4]
    cursor.execute("select * from purchase")
    data=cursor.fetchall()
    pid=data[-1][0]
    st="update purchase set total_aed ={}*{} where pid={}".format(quantity,price_of_1,pid)
    cursor.execute(st)
    mycon.commit()
    
    #Updating the stock in the 'Inventory' table by subtracting the quantity of books sold from the stock
    
    cursor.execute("select * from inventory")
    data=cursor.fetchall()
    for i in data:
        if i[1]==bookname:
            stock=i[3]
    if (stock-quantity)>=0:
        st="update inventory set stock={}-{} where book_name='{}'".format(stock,quantity,bookname)
        cursor.execute(st)
        mycon.commit()
    else:
        print("You're claiming to have sold more books than you have currently stored in your inventory, There are", stock, bookname, "books in your inventory")

#Below are the functions available to the admin, this includes inputting data into a tables and viewing tables

def adminb(): 
   #FIRST WINDOW THAT IS DISPLAYED TO ADMIN. 
    
    window1 = tk.Tk()
    greeting = tk.Label(window1, text="Choose between inputting data between a table and viewing a table")     
    greeting.pack(side=tk.TOP)
    inputb=tk.Button(window1, text="Inputting Into Tables",command=insert1)##########
    inputb.pack(side=tk.LEFT)
    viewb=tk.Button(window1, text="Viewing Tables",command=viewadmin)
    viewb.pack(side=tk.RIGHT)
    window1.title("Bookstore Management System")
    window1["background"]="#18C3F8"

#You can input data into PURCHASE TABLE

def insert1(): #
    #WINDOW THAT DISPLAYS THE INPUTTING DATA TABLE

    window2=tk.Tk()
    greeting = tk.Label(window2, text="Choose between inputting data into the purchase table and the inventory table")     
    greeting.pack(side=tk.TOP)
    purchaseb=tk.Button(window2, text="Purchase Table",command=datapurchase)##########
    purchaseb.pack(side=tk.LEFT)
    inventoryb=tk.Button(window2, text="Inventory Table",command=datainventory)
    inventoryb.pack(side=tk.RIGHT)
    window2.title("Bookstore Management System")
    window2["background"]="#18C3F8"

#FUNCTION ALLOWING INPUTTING VALUES INTO INVENTORY

def datainventory():
    def submit():
        name=e1.get()
        author=e2.get()
        stock=int(e3.get())
        priceof1=int(e4.get()) 
        inserttable1(name,author,stock,priceof1)
        
      
    #BASIC WINDOW FOR INPUTTING VALUES INTO INVENTORY
    
    window3=tk.Tk()
    name1=tk.Label(window3, text="Name of the Book")
    name1.grid(row=0,column=0)
    author1=tk.Label(window3, text="Author")
    author1.grid(row=1,column=0)
    stock1=tk.Label(window3, text="Stock")
    stock1.grid(row=2,column=0)
    priceof1_=tk.Label(window3, text="Price of One Book")
    priceof1_.grid(row=3,column=0)
    e1=tk.Entry(master=window3)
    e1.grid(row=0,column=1)
    e2=tk.Entry(master=window3)
    e2.grid(row=1,column=1)
    e3=tk.Entry(master=window3)
    e3.grid(row=2,column=1)
    e4=tk.Entry(master=window3)
    e4.grid(row=3,column=1)
    get=tk.Button(window3, text="Submit", command=submit)
    get.grid(row=4,column=1)
    window3.title("Bookstore Management System")
    window3["background"]="#18C3F8"

#FUNCTION FOR INPUTTING VALUES INTO PURCHASE TABLE

def datapurchase():
    def submit():
        name=e1.get()
        qty=int(e2.get())
        inserttable2(name,qty)
   
    #BASIC WINDOW FOR PURCHASE WINDOW
    
    window4=tk.Tk()
    name1=tk.Label(window4, text="Name of the Book")
    name1.grid(row=0,column=0)
    qty=tk.Label(window4, text='Quantity of Books Bought')
    qty.grid(row=1,column=0)
    e1=tk.Entry(master=window4)
    e1.grid(row=0,column=1)
    e2=tk.Entry(master=window4)
    e2.grid(row=1,column=1)
    get=tk.Button(window4, text="Submit", command=submit)
    get.grid(row=2,column=1)
    window4.title("Bookstore Management System")
    window4["background"]="#18C3F8"

#The tables you can view as the admin are the purchase table, wishlist table and the wishlist table.
    
def viewadmin():
   #WINDOW THAT SHOWS VIEW TABLE FUNCTIONS FOR ADMIN
    
    window7=tk.Tk()
    purchase=tk.Button(window7, text="View the Purchase Table",command=viewpurchase)
    purchase.grid(row=0,column=0)
    inventory=tk.Button(window7, text="View the Inventory Table",command=viewinventory)
    inventory.grid(row=0, column=1)
    wishlist=tk.Button(window7, text="View the Wishlist Table", command=viewwishlist)
    wishlist.grid(row=0,column=2)
    window7.title("Bookstore Management System")
    window7["background"]="#18C3F8"

#The wishlist table exists so that as a admin you can check which all books are not in your inventory and then later add them.

def viewwishlist():
   #WINDOW THAT ALLOWS TO ADD BOOKS INTO WISHLIST OR VIEW WISHLIST
   
    window8=tk.Tk()
    mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
    cursor=mycon.cursor()
    cursor.execute("select * from wishlist")
    data=cursor.fetchall()
    rowcount=cursor.rowcount
    mycon.close()
    isbn=tk.Label(window8, text="ISBN")
    isbn.grid(row=0,column=0)
    name=tk.Label(window8, text="Name of the Book")
    name.grid(row=0,column=1)
    author=tk.Label(window8, text="Author")
    author.grid(row=0,column=2)
    window8.title("Bookstore Management System")
    window8["background"]="#18C3F8"
    for i in range(rowcount):
        for j in range(3):
            e=tk.Label(window8, text=str(data[i][j]))
            e.grid(row=i+1,column=j)

 #FUNCTION FOR VIEWING PURCHASE TABLE
   
def viewpurchase():
    # WINDOW THAT SHOWS BUTTON TO VIEW FROM PURCHASE TABLE
    
    window11=tk.Tk()
    mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
    cursor=mycon.cursor()
    cursor.execute("SELECT * FROM PURCHASE")
    data=cursor.fetchall()
    rowcount=cursor.rowcount
    mycon.close()
    pid=tk.Label(window11, text="PID")
    pid.grid(row=0, column=0)
    dop=tk.Label(window11, text="DOP")
    dop.grid(row=0, column=1)
    name=tk.Label(window11, text="Name of the Book")
    name.grid(row=0,column=2)
    qty=tk.Label(window11, text="Quantity")
    qty.grid(row=0,column=3)
    price=tk.Label(window11, text="Price of One")
    price.grid(row=0,column=4)
    total=tk.Label(window11, text="Total Price")
    total.grid(row=0,column=5)
    window11.title("Bookstore Management System")
    window11["background"]="#18C3F8"
    for i in range(rowcount):
        for j in range(6):
            e=tk.Label(window11, text=str(data[i][j]))
            e.grid(row=i+1,column=j)

#FUNCTION FOR VIEWING INVENTORY TABLE

def viewinventory():
   
    #WINDOW ALLOWS TO VIEW BOOKS FROM INVENTORY TABLE
    
    window12=tk.Tk()
    sno=tk.Label(window12,text="S.No.")
    sno.grid(row=0,column=0)
    bookname=tk.Label(window12, text="Name of the Book")
    bookname.grid(row=0,column=1)
    author=tk.Label(window12, text="Author")
    author.grid(row=0,column=2)
    stock=tk.Label(window12, text="Stock")
    stock.grid(row=0,column=3)
    price=tk.Label(window12, text="Price of One")
    price.grid(row=0,column=4)
    mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
    cursor=mycon.cursor()
    cursor.execute("SELECT * FROM INVENTORY")
    rows=cursor.fetchall()
    rowcount=cursor.rowcount
    mycon.close()
    window12.title("Bookstore Management System")
    window12["background"]="#18C3F8"
    for i in range(rowcount):
        for j in range(5):
            e=tk.Label(window12, text=str(rows[i][j]))
            e.grid(row=i+1,column=j)
    
#Below are the options available as the customer
 
#LABELS AND BUTTONS AVAILABLE TO CUSTOMER TO USE                     
def customerb():
    global L
    #FIRST WINDOW THAT DISPLAYS WHEN CUSTOMER ENTERS BOOKSTORE
    
    window5=tk.Tk()
    view=tk.Button(window5, text="Viewing Inventory",command=viewinventory)
    view.grid(row=0,column=0)
    wish=tk.Button(window5, text="Adding Books to Wishlist",command=wishlist)
    wish.grid(row=0,column=1)
    purchase1=tk.Button(window5, text="Make a Purchase",command=purchase)
    purchase1.grid(row=0,column=2)
    bill1=tk.Button(window5, text="View your Bill",command=bill)
    bill1.grid(row=0,column=3)
    search1=tk.Button(window5, text="Search",command=search)
    search1.grid(row=0,column=4)
    L=[]
    window5.title("Bookstore Management System")
    window5["background"]="#18C3F8"

#INSERT BOOKS INTO THE WISHLIST TABLE
def wishlist():
    def submit():
        isbn=int(e3.get())
        name=e1.get()
        author=e2.get()
        mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
        cursor=mycon.cursor()
        st="insert into wishlist(ISBN, book_name,author) values({},'{}','{}')".format(isbn,name,author)
        cursor.execute(st)
        mycon.commit()
    
   #WINDOW THAT ALLOWS TO ADD BOOKS TO WISHLIST
   
    window6=tk.Tk()
    title=tk.Label(window6, text="Add the book to your Wishlist")
    title.grid(row=0,column=1)
    name1=tk.Label(window6, text="Name of the Book")
    name1.grid(row=1,column=0)
    author=tk.Label(window6, text="Author")
    author.grid(row=2,column=0)
    isbn=tk.Label(window6, text="ISBN Number")
    isbn.grid(row=3,column=0)
    e1=tk.Entry(master=window6)
    e1.grid(row=1,column=1)
    e2=tk.Entry(master=window6)
    e2.grid(row=2,column=1)
    e3=tk.Entry(master=window6)
    e3.grid(row=3,column=1)
    get=tk.Button(window6, text="Submit", command=submit)
    get.grid(row=4,column=1)
    window6.title("Bookstore Management System")
    window6["background"]="#18C3F8"

# FUNCTION ALLOWING CUSTOMER TO MAKE A PURCHASE BY ENTERING BOOKNAME AND QUANTITY


def purchase():
    def submit():
        global L
        name=e1.get()
        qty=int(e2.get())
        inserttable2(name,qty)
        mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
        cursor=mycon.cursor()
        cursor.execute("select * from inventory")
        purrows=cursor.fetchall()
        for i in purrows:
            if i[1]==name:
                price_of_1=i[4]
        window10=tk.Tk()
        label=tk.Label(window10, text="The total price of your purchase is {}".format(qty*price_of_1))
        label.grid(row=1,column=1)
        L.append((name,qty,price_of_1,qty*price_of_1))
        window10.title("Bookstore Management System")
        window10["background"]="#18C3F8"
    # WINDOW THAT ALLOWS CUSTOMER TO PURCHASE BOOK
    
    window9=tk.Tk()
    name=tk.Label(window9, text="Name of the Book")
    name.grid(row=0,column=0)
    qty=tk.Label(window9, text="Quantity")
    qty.grid(row=1,column=0)
    e1=tk.Entry(master=window9)
    e1.grid(row=0,column=1)
    e2=tk.Entry(master=window9)
    e2.grid(row=1,column=1)
    get=tk.Button(window9, text="Submit", command=submit)
    get.grid(row=2,column=1)
    window9.title("Bookstore Management System")
    window9["background"]="#18C3F8"

#FUNCTION RESPONSIBLE FOR DISPLAYING CUSTOMERS BILL AFTER PURCHASE IS MADE

def bill():
    #WINDOW THAT SHOW THE TOTAL BILL
    
    window13=tk.Tk()
    global bill_id
    global L
    label3=tk.Label(window20, text="Bill ID: {}".format(bill_id))
    label3.pack()
    bill_id+=1
    total=0 
    for i in L:
        total+=i[3]
    for j in L:
        label=tk.Label(window13, text="'{}'                {}         {}".format(j[0],j[1], j[3]))
        label.pack()
    label2=tk.Label(window13, text="Your total comes out to {}".format(total))
    label2.pack()
    window13.title("Bookstore Management System")
    window13["background"]="#18C3F8"

#FUNCTION THAT SEARCHES FOR BOOKS BASED ON SNO/NAME/AUTHOR

def search():
    def submit():
        name=e1.get()
        sno=e2.get()
        author=e3.get()
        mycon=sqlcon.connect(host='127.0.0.1',user='root',passwd='mysql',database='bookstore')
        cursor=mycon.cursor()
        if sno and not name and not author:
            cursor.execute("SELECT * FROM inventory WHERE sno={}".format(sno))
            data=cursor.fetchall()
            row=cursor.rowcount

        elif name and not sno and not author:
            cursor.execute("SELECT * FROM inventory WHERE book_name='{}'".format(name))
            data=cursor.fetchall()
            row=cursor.rowcount

        elif author and not sno and not name:
            cursor.execute("SELECT * FROM inventory WHERE author='{}'".format(author))
            data=cursor.fetchall()
            row=cursor.rowcount

        else:
            cursor.execute("SELECT * FROM inventory WHERE sno='{}' AND book_name='{}' AND author='{}'".format(sno,name,author))
            data=cursor.fetchall()
            row=cursor.rowcount
        
        #WINDOW THAT ALLOWES TO SEARCH FOR BOOKS BASED ON CERTAIN CRITERIA
        
        window15=tk.Tk()
        sno=tk.Label(window15,text="S.No.")
        sno.grid(row=0,column=0)
        bookname=tk.Label(window15, text="Name of the Book")
        bookname.grid(row=0,column=1)
        author=tk.Label(window15, text="Author")
        author.grid(row=0,column=2)
        stock=tk.Label(window15, text="Stock")
        stock.grid(row=0,column=3)
        price=tk.Label(window15, text="Price of One")
        price.grid(row=0,column=4)
        window15.title("Bookstore Management System")
        window15["background"]="#18C3F8"
        for i in range(row):
            for j in range(5):
                e=tk.Label(window15, text=str(data[i][j]))
                e.grid(row=i+1,column=j)
                
   
    #WINDOW THAT ALLOWS TO INPUT BOOKS   
    window14=tk.Tk()
    name=tk.Label(window14, text="Name of the Book")
    name.grid(row=0,column=0)
    sno=tk.Label(window14,text="S.No.")
    sno.grid(row=1,column=0)
    author=tk.Label(window14, text="Author")
    author.grid(row=2,column=0)
    e1=tk.Entry(master=window14)
    e1.grid(row=0,column=1)
    e2=tk.Entry(master=window14)
    e2.grid(row=1,column=1)
    e3=tk.Entry(master=window14)
    e3.grid(row=2,column=1)
    get=tk.Button(window14, text="Submit",bg="red",command=submit)
    get.grid(row=3,column=1)
    window14.title("Bookstore Management System")
    window14["background"]="#18C3F8"
    
        

    
    
#FIRST WINDOW THAT DISPLAYS WHEN THE PROGRAM IS RUN


window = tk.Tk()  
window.geometry("500x250")
greeting = tk.Label(text="Welcome to our bookstore's database\n\nPlease select how you would like to proceed")     
greeting.pack(side=tk.TOP)
adminb1=tk.Button(text="Admin",command=adminb)##########
adminb1.pack(side=tk.LEFT)
customerb1=tk.Button(text="Customer",command=customerb)
customerb1.pack(side=tk.RIGHT)
window.title("Bookstore Management System")
window["background"]="#18C3F8"
window.mainloop() 
L=[]
bill_id= 1 




        
    
    
    


    
    
  

