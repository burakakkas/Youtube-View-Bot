import sqlite3
import sys
import random

def db_creation():
    conn = sqlite3.connect('customers.db')
    print("Opened database successfully")
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE CUSTOMERS
         (ID            INTEGER         PRIMARY KEY AUTOINCREMENT,
         USERNAME       VARCHAR(50)     NOT NULL,
         TIME           TEXT            NOT NULL,
         ORDER_SIZE     INT             NOT NULL
         );''')
    cur.execute('''CREATE TABLE ORDERS
         (USER_ID       INT             NOT NULL,
         ORDER_ID       INTEGER         PRIMARY KEY AUTOINCREMENT,
         GOAL           INT             NOT NULL,
         REMAINED       INT             NOT NULL,
         STATUS         VARCHAR(20)     NOT NULL,
         TIME           TEXT            NOT NULL,
         URL            TEXT            NOT NULL,
         FOREIGN KEY(USER_ID) REFERENCES CUSTOMERS(ID)
         );''')                                              # Status can be 3 values, DAILY REPEAT NUMBER - FAIL - "-1"
    cur.execute("UPDATE sqlite_sequence SET seq = '88' WHERE name = 'ORDERS'")
    cur.execute('''CREATE TABLE HISTORY
         (USER_ID            INT             NOT NULL,
         ORDER_ID            INT             PRIMARY KEY NOT NULL,
         GOAL                INT             NOT NULL,
         START_TIME          TEXT            NOT NULL,
         FINISH_TIME         TEXT            NOT NULL,
         URL                 TEXT            NOT NULL,
         FOREIGN KEY(USER_ID) REFERENCES CUSTOMERS(ID)
         );''')

    conn.commit()
    conn.close()
    print("Table created successfully")
    
def db_add_customer(username):
    conn = sqlite3.connect('customers.db')
    print("Opened database successfully")
    cursor = conn.execute("SELECT ORDER_SIZE FROM CUSTOMERS WHERE USERNAME= ?", (username,))
    exist_or_not = cursor.fetchall()
    if len(exist_or_not) == 0:
        conn.execute(
            '''INSERT INTO CUSTOMERS(USERNAME, TIME, ORDER_SIZE)
            VALUES(?, datetime('now', 'localtime'), 1)''', (username,))
        cursor = conn.execute(
            "SELECT ID FROM CUSTOMERS WHERE USERNAME= ?", (username,))
        data = cursor.fetchall()
    else:
        for row in exist_or_not:
            order_size = row[0]
        order_size = order_size + 1
        k=1
        data = (order_size, username)
        print(str(order_size) + "-" + str(username))
        conn.execute(
            "UPDATE CUSTOMERS set ORDER_SIZE = ? WHERE USERNAME=?", (order_size, username))
        cursor = conn.execute(
            "SELECT ID FROM CUSTOMERS WHERE USERNAME = ?", (username,))
        data = cursor.fetchall()
    
    conn.commit()
    conn.close()
    print("User added successfully")
    user_id = data[0][0]
    return user_id

def db_preview(username):
    conn = sqlite3.connect('customers.db')
    print("Opened database successfully")

    cursor = conn.execute("SELECT * from CUSTOMERS WHERE USERNAME = ?", (username,))
    data = cursor.fetchall()
    if len(data) == 0:
        print("Username Not Exist!")
    else:
        for row in data:
           print("ID = ", row[0])
           print("USERNAME = ", row[1])
           print("TIME = ", row[2])
           print("ORDER_SIZE = ", row[3], "\n")
    conn.close()


def db_add_order(user_id, goal, url):
    conn = sqlite3.connect('customers.db')
    print("Opened database successfully") 
    data = (user_id, goal, goal, url)
    sql_command = '''INSERT INTO ORDERS (USER_ID, GOAL, REMAINED, STATUS ,TIME, URL) 
                    VALUES (?, ?, ?, '-1', datetime('now', 'localtime'), ?); '''
    conn.execute(sql_command, data)
    conn.commit()
    conn.close()

def morning_clean():
    conn = sqlite3.connect('customers.db')
    cursor = conn.execute(
        "UPDATE ORDERS SET STATUS = '0' WHERE STATUS != 'FAIL'")
    conn.commit()
    conn.close()

def watching_status():
    conn = sqlite3.connect('customers.db')
    cursor = conn.execute(
        "SELECT ORDER_ID, URL, STATUS, GOAL, REMAINED, USER_ID, TIME FROM ORDERS WHERE STATUS != 'FAIL'")
    data = cursor.fetchall()
    for row in data:
        if int(row[2]) != 10 and row[4] != 0 and row[2] != "-1":  # Daily Limit
            if row[3] == 1000 or row[3] == 10000 or row[3] == 50000 or row[3] == 100000: # Daily 5 Times
                if row[2] != 5:
                    print('1000 - 10k - 50k - 100k views')
                    print(str(row[0]) + ' - ' + str(row[1]) +
                          ' - ' + str(row[2]) + ' - ' + str(row[3]) + ' - ' +str(row[4]))
                    print("Python bot.py " + str(row[1]) + ' 1000')
                    status = int(row[2]) +1
                    remained = int(row[4]) - 1000
                    cursor = conn.execute(
                        "UPDATE ORDERS SET STATUS = ?, REMAINED = ? WHERE ORDER_ID = ?", (status, remained, row[0]))
                    conn.commit()
                else:
                    print("Daily 5 repeat limit exceed.")

            elif row[3] == 500000 or row[3] == 1000000:  # Daily 10 Times
                print('500k - 1m views')
                print(str(row[0]) + ' - ' + str(row[1]) +
                      ' - ' + str(row[2]) + ' - ' + str(row[3]) + ' - ' + str(row[4]))
                print("Python bot.py " + str(row[1]) + ' 1000')
                status = int(row[2]) + 1
                remained = int(row[4]) - 1000
                cursor = conn.execute(
                    "UPDATE ORDERS SET STATUS = ?, REMAINED = ? WHERE ORDER_ID = ?", (status, remained, row[0]))
                conn.commit()

            else:
                print('Not a valid goal')
        elif row[4] == 0:
            conn.execute("INSERT INTO HISTORY (USER_ID,ORDER_ID,GOAL,START_TIME,FINISH_TIME,URL) \
                VALUES (?, ?, ?, ?, datetime('now', 'localtime'), ? )", (row[5], row[0], row[3], row[6], row[1]))
            conn.execute("DELETE from ORDERS where REMAINED = ?", (row[4],))
            conn.commit()
        elif row[2] == "-1":
            print("Status is -1 and its not ready to watch, wait to clean.")
        else:
            print("Daily 10 repeat limit exceed.")
    conn.close()


def testview():
    print("this is test view")

def _1k():
    print("this is 1k view")

def _10k():
    print("this is 10k view")

def _50k():
    print("this is 50k view")

def _100k():
    print("this is 100k view")


def _500k():
    print("this is 500k view")


def _1m():
    print("this is 1m view")

def main():
    print("--WELCOME--")
    #db_creation()
    #db_preview("burakakkas")
    if len(sys.argv) == 4:                      # ORDER ADDING -- python system.py [username] [video-url] [view-number]
        username = sys.argv[1]
        url = sys.argv[2]
        view = sys.argv[3]

        user_id = db_add_customer(username)
        db_add_order(user_id, view, url)
        print("Order added successfully")

    elif len(sys.argv) == 1:                    # WATCHING -- python system.py
        watching_status()
        print("Working as a system.")
    
    elif len(sys.argv) == 2:                    # MORNING CLEAN -- python system.py clean
        morning_clean()
        print("Morning cleaning process.")

    elif len(sys.argv) == 3:                    # DATABASE CREATION -- python system.py create db
        db_creation()
        print("Morning cleaning process.")      

        

    else:
        print("Please run script with right parameters.\npython system.py [username] [video-url] [view-number]")


if __name__ == "__main__":
  main()
