from os import system
import os
import sqlite3

#Create a variable for the script path and manufactures a path for a database
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')
db_path = os.path.join(data_dir, 'ebookstore.db')

#check if there is a database and creates one if not. 
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

else:
    print('hello')

#Creating the Link to  the Database
db = sqlite3.connect(db_path)
#Defining a reference to the cursor
cursor = db.cursor()

#Try exception to catch Database already exhists error
try:
    cursor.execute('CREATE TABLE book(id INTEGER PRIMARY KEY, title VARCHAR, author VARCHAR, qty INT)')
    cursor.execute('INSERT INTO book (id, title, author, qty) VALUES (3001, "A Tale of Two Cities", "Charles Dickens", 30)')
    cursor.execute('INSERT INTO book (id, title, author, qty) VALUES (3002, "Harry Potter and the Philosophers Stone", "J.K. Rowling", 40)')
    cursor.execute('INSERT INTO book (id, title, author, qty) VALUES (3003, "The Lion, the Witch and the Wardrobe", "C.S Lewis", 25)')
    cursor.execute('INSERT INTO book (id, title, author, qty) VALUES (3004, "The Lord of the Rings", "J.R.R Tolkien", 37)')
    cursor.execute('INSERT INTO book (id, title, author, qty) VALUES (3005, "Alice in Wonderland", "Lewis Carroll", 12)')
    print('Table book Cretaed')
    
except Exception as e:
    print(e)
finally:
    db.commit()

#A function to add a book  to  the DB    
def add_book():
    
    title = input('Book Title: ')
    author = input('author: ')
    quantity = int(input('quantity: '))
    
    cursor.execute('''INSERT INTO book(title, author, qty)
                   VALUES (?,?,?)''', (title, author, quantity))
    db.commit()
    id = cursor.lastrowid
    return  print(f'\nNew book {title} added with ID: {id}')

#A funtion  that lists all books in  the Databse
def list_all():
    print('\nBooks: \n')
    cursor.execute('SELECT * FROM book')
    for row in cursor:
        print(f'ID: {row[0]}  Name: {row[1]}  author: {row[2]}  Quantity: {row[3]}')

    return

#Delete a book in the database using its  ID
def delete_book():
    
    list_all()
    delete_id = int(input('ID of book to delete: '))
    cursor.execute('''SELECT * FROM book WHERE id = ?''',(delete_id, ))
    for row in cursor:
        print(f'ID: {row[0]}  Name: {row[1]}  author: {row[2]}  Quantity: {row[3]}')
    
    while True:
        delete_auth =  input('''Are you sure  you want to delete this entry?: 
              Y) Yes
              N) No
              Confirmation: ''')
        if delete_auth.upper() == 'Y':
            cursor.execute('''DELETE FROM book WHERE id = ?''',(delete_id,))
            return
        elif delete_auth.upper() == 'N':
            return
        else:
            print("Invalid input")
            

#Serach any book  in the database using a similar title or auther            
def search_book():
    search_key = input("Search: ")
    
    print("\nResults\n")
    cursor.execute('SELECT * FROM book WHERE title LIKE ? OR author LIKE ?',('%'+search_key+'%', '%'+search_key+'%'))
    for row in cursor:
        print(f'ID: {row[0]}  Title: {row[1]}  author: {row[2]}  Stock: {row[3]}')
        
    return


#update  the  values  of any book in  the DB
def update_book(num):
    
    b_id  = int(input("Book ID: "))
    
    if num == 1:
        n_title = input('New Title: ')
        cursor.execute('UPDATE book SET title = ? WHERE id = ?',(n_title, b_id))
        db.commit()
        
    elif num == 2:
        n_auther = input('New Auther: ')
        cursor.execute('UPDATE book SET auther = ? WHERE id = ?', (n_auther, b_id))
        db.commit()
        
    elif num  == 3:
        n_qty = int(input('New Quantity: '))
        cursor.execute('UPDATE book SET qty = ? WHERE id = ?', (n_qty,  b_id))
        db.commit()
        
    else:
        print("Invalit input.")
        return
    
    cursor.execute('SELECT * FROM book WHERE id = ?',(b_id, ))
    for row in cursor:
        print(f'''Book ID: {row[0]} Updated: 
Title: {row[1]}  
author: {row[2]}  
Stock: {row[3]}''')
 
    return

#Fetches the SUM of all qty's in the database
def total_qty():
    
    cursor.execute("SELECT SUM(qty) FROM book ")
    total = cursor.fetchone()

    #check to make sure the result is not Null
    if total and total[0] is not None:
        sum_qty = int(total[0])
        print(f"\nTotal Quantity on hand\nTotal: {sum_qty}\n")

    else:
        print("The total QTY is Null")


    return
            
#Start a loop for continues interactions on the DB
while True:
    
    menu = int(input("""Menu\n
What would you like to do: 
1) Enter Book
2) Update Book
3) Delete Book
4) Search Books
5) List all Books
6) Total QTY                    
0) Exit
Selection: """))
    
    if menu == 1:
        add_book()
        
        
    elif menu == 2:
        update_menu = int(input("""Whats would you like to update?: 
1) Book Tile
2) Auther
3) Quantity
Selection: """))
        update_book(update_menu)
        
    elif menu == 3:
        delete_book()
        
    elif menu == 4:
        search_book()
        
    elif menu == 5:
        list_all()

    elif menu == 6:
        total_qty()
    
    elif menu == 0:
        db.close()
        break
    
    else:
        print('Invalid input.')