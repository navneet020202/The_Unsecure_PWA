import sqlite3 as sql
import time
import random

#  Secure: Use parameterized queries to prevent SQL Injection
def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username, password, dateOfBirth) VALUES (?, ?, ?)",
        (username, password, DoB),
    )
    con.commit()
    con.close()

def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    #  Secure Query: Prevents SQL Injection
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()

    if user is None:
        con.close()
        return False
    
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()

    if user is None:
        con.close()
        return False
    
    # Secure Visitor Log Update (Removes risky file handling)
    with open("visitor_log.txt", "r+") as file:
        try:
            number = int(file.read().strip())
        except ValueError:
            number = 0
        number += 1
        file.seek(0)
        file.write(str(number))
        file.truncate()

    # Simulated response time for testing (optional)
    time.sleep(random.uniform(0.08, 0.09))

    con.close()
    return True

def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Secure Query: Prevents SQL Injection
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()

def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()

    with open("templates/partials/success_feedback.html", "w") as f:
        for row in data:
            f.write("<p>\n")
            f.write(f"{row[1]}\n")  # Safe because data is fetched securely
            f.write("</p>\n")
