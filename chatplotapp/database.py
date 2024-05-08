import mysql.connector
global sql

import mysql.connector
sql = mysql.connector.connect(
            host="localhost",
            user="root",
            password="desires",
            database="pradeep_j"
        )
        

def get_order(order_id):
    cursor=sql.cursor()
    query=("select status from pradeep_j.order_tracking where order_id=%s")
    params = (order_id,)
    cursor.execute(query, params)
    result=cursor.fetchone()
    cursor.close()
    
    
    if result is not None:
        return result[0]
    else :
        return None
    
def next_order_id():
    cursor = sql.cursor()

    # Executing the SQL query to get the next available order_id
    query = ("SELECT MAX(order_id) FROM orders")
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1
    
    
    
def insert_order_item(pharmacy_item, quantity, order_id):
    try:
        cursor = sql.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item',(pharmacy_item,quantity, order_id))

        # Committing the changes
        sql.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        sql.rollback()

        return 1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        sql.rollback()

        return 1


def total_order_price(order_id):
    cursor = sql.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result



def order_tracking(order_id, status):
    cursor = sql.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    sql.commit()

    # Closing the cursor
    cursor.close()

    
    
    

    
   