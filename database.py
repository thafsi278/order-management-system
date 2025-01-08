import mysql.connector

# Creating connection to database in MySQL. 
database = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "mydb_new"
)

# Cursor initialization
mycursor = database.cursor(buffered=True)

# Retrieves all data from orders table, and returns as list.
def database_select_all_orders():
    query = "SELECT * FROM orders"
    mycursor.execute(query)
    return list(mycursor.fetchall())

# Adds new user with input data and returns boolean, if query is successful or not
def database_add_user(input_data):
    username = input_data[0]
    password = input_data[1]
    type = input_data[2]
    sub_query = "(SELECT user_type_id FROM user_type WHERE user_acc_type = UPPER('" + type + "'))"
    main_query = "INSERT INTO users (user_name, user_password, fk_user_type_id) VALUES ('" + username + "', '" + password + "', " + sub_query + ");"
    try:
        mycursor.execute(main_query)
        database.commit()
        return True
    except:
        return False

# Searches for user in users table and returns boolean, based on rowcount value.
def database_search_user(input_data):
    username = input_data[0]
    password = input_data[1]
    main_query = "SELECT user_name FROM users WHERE user_name = '" + username + "' AND user_password = '" + password + "';"
    try:
        mycursor.execute(main_query)
        if mycursor.rowcount != 0:
            return True
        else:
            return False
    except:
        return False

# Searches for user type and returns either value if query successful, or false if failed
def database_search_user_type(username):
    main_query = "SELECT user_acc_type FROM user_type INNER JOIN users ON users.fk_user_type_id = user_type.user_type_id WHERE users.user_name = '" + username + "';"
    try:
        mycursor.execute(main_query)
        return mycursor.fetchone()
    except:
        return False

# Searches for username in users table and returns boolean, based on rowcount value
def database_search_user_name(username):
    main_query = "SELECT user_name FROM users WHERE user_name = '" + username + "';"
    try:
        mycursor.execute(main_query)
        if mycursor.rowcount != 0:
            return True
        else:
            return False
    except:
        return False

# Retrieves order data for a specific row, using order id. Returns as list if successful, or as false
def database_get_order(order_id):
    main_query = "SELECT * FROM orders WHERE order_id ='" + order_id + "';"
    try:
        mycursor.execute(main_query)
        return list(mycursor.fetchone())
    except:
        return False
    
# Updates order data with input data and returns boolean, if query is successful or not
def database_edit_order(input_data):
    order_number = str(input_data[0])
    order_date = str(input_data[1])
    customer_name = str(input_data[2])
    company = str(input_data[3])
    order_total = str(input_data[4])
    order_status = str(input_data[5])
    item_count = str(input_data[6])
    main_query = "UPDATE orders SET order_id = '" + order_number + "', order_date = '" + order_date + "', order_customer_name = '" + customer_name + "', order_company = '" + company + "', order_total = '" + order_total + "', order_status = '" + order_status + "', order_item_count = '" + item_count + "' WHERE order_id = '" + order_number + "';"
    try:
        mycursor.execute(main_query)
        database.commit()
        return True
    except:
        return False

# Deletes order data and returns boolean, if query is successful or not
def database_delete_order(order_id):
    main_query = "DELETE FROM orders WHERE order_id = '" + order_id + "';"
    try:
        mycursor.execute(main_query)
        database.commit()
        return True
    except:
        return False
    
# Adds order data to table and returns boolean, if query is successful or not
def database_add_order(input_data):
    order_number = str(input_data[0])
    order_date = str(input_data[1])
    customer_name = str(input_data[2])
    company = str(input_data[3])
    order_total = str(input_data[4])
    order_status = str(input_data[5])
    item_count = str(input_data[6])
    main_query = "INSERT INTO orders (order_id, order_date, order_customer_name, order_company, order_total, order_status, order_item_count) VALUES ('" + order_number + "', '" + order_date + "', '" + customer_name + "', '" + company + "', '" + order_total + "', '" + order_status + "', '" + item_count + "');"
    try:
        mycursor.execute(main_query)
        database.commit()
        return True
    except:
        return False
