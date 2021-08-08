import sqlite3


def create():
    connection = sqlite3.connect("./contacts_database.db")
    curr = connection.cursor()
    curr.execute("""
    CREATE TABLE IF NOT EXISTS Contacts (
    Id INTEGER PRIMARY KEY,
    Name VARCHAR,
    Phone_number VARCHAR,
    Email VARCHAR)
    """)
    connection.commit()
    connection.close()


def add(name,phone,email):
    connection = sqlite3.connect("./contacts_database.db")
    curr = connection.cursor()
    curr.execute("INSERT INTO Contacts VALUES (NULL,?,?,?)",(name, phone,email))
    connection.commit()
    connection.close()


def delete(name):
    connection = sqlite3.connect("./contacts_database.db")
    curr = connection.cursor()
    curr.execute("DELETE FROM Contacts WHERE Name=?",(name,))
    connection.commit()
    connection.close()


def edit(id,name,phone,email):
    connection = sqlite3.connect("./contacts_database.db")
    curr = connection.cursor()
    curr.execute("UPDATE Contacts SET Name=?, Phone_number=?, Email=? WHERE Id=?",(name,phone,email,id))
    connection.commit()
    connection.close()


def search(name):
    connection = sqlite3.connect("./contacts_database.db")
    curr = connection.cursor()
    curr.execute("""SELECT * FROM Contacts WHERE Name LIKE ? """,(f"%{name}%",))
    rows = curr.fetchall()
    connection.close()
    return rows


def view():
    connection = sqlite3.connect("./contacts_database.db")
    curr = connection.cursor()
    curr.execute("""SELECT * FROM Contacts  """)
    rows = curr.fetchall()
    connection.close()
    return rows


def export(name,phone,email):
    with open(f"./{name}.txt","w") as file:
        file.write(f"{name}\n{phone}\n{email}")


create()
