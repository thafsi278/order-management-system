from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import *
from validations import *

views = Blueprint(__name__, "views")

# Function that checks if user in session exists i.e. user is currently logged in 
def check_session_exists():
    if "user" in session:
        return True
    else:
        return False

# View and function that renders home page. If not signed in, redirects to sign-in page
@views.route("/index")
def home():
    if (check_session_exists()):
        return render_template("index.html", logged_in = True, logged_in_user = session["user"], user_type = session["type"])
    else:
        return redirect(url_for("views.sign_in"))

# View and function that renders orders page. If not signed in, redirect and call home function
@views.route("/orders")
def orders():
    if (check_session_exists()):
        orders_list = database_select_all_orders()
        return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"], user_type = session["type"])
    else:
        return redirect(url_for("views.home"))

# View and function that handles the edit order functionality
@views.route("/orders/edit/<order_id>", methods=["POST", "GET"])
def edit_order(order_id):
    if (check_session_exists()): # Check is user is logged in
        orders_list = database_select_all_orders() # Retrieve all orders from data table
        if request.method == "POST": # Handles post request
            # Retrieves all form data
            order_number = request.form.get("ordernumber", "")
            order_date = request.form.get("orderdate", "")
            customer_name = request.form.get("customername", "")
            company = request.form.get("company", "")
            order_total = request.form.get("ordertotal", "")
            order_status = request.form.get("orderstatus", "").title()
            item_count = request.form.get("itemcount", "")
            input_data = [order_number, order_date, customer_name, company, order_total, order_status, item_count]
            validation_dict = validate_order(input_data) # Dictionary set with values returned from validate_order
            is_valid = validation_dict["is_valid"] # Boolean value from dictionary. True if all data is valid, false if atleast one is invalid
            validation_message = validation_dict["validation_message"] # Appropriate message returned, based on success or specific error 
            # If validation is true, call edit order with input data and redirect to views order if successful. Else render orders table with current orders list
            if (is_valid):
                if database_edit_order(input_data):
                    return redirect(url_for("views.orders"))
                else:
                    return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"])
            # Else condition when validation check fails. Flash set for error with appropriate message for failed validation. Rediects to edit order view
            else: 
                flash(validation_message, category="error")
                return redirect(url_for("views.edit_order", id = order_id))
        # Else condition when not post request and is get request, render orders table with paramater values passed in
        else:
            return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"], edit_in_process = True, id = order_id)
    # If not logged in, redirect to home view
    else: 
        return redirect(url_for("views.home"))

# View and function that handles the delete order functionality
@views.route("/orders/delete/<order_id>", methods=["POST", "GET"])
def delete_order(order_id):
    if (check_session_exists()): # Check is user is logged in
        # If user is admin, allow and perform delete action and redirect to orders view
        if session["type"] == "Administrator":
            if database_delete_order(order_id):
                return redirect(url_for("views.orders"))
            else:
                return redirect(url_for("views.orders"))
        # Else flash set with error message and redirect to orders view
        else:
            message = "User: " + session["user"] + " is not authorised to perform this action. Please sign in as ADMIN."
            flash(message, category="error")
            return redirect(url_for("views.orders"))
    # If not logged in, redirect to home view
    else:
        return redirect(url_for("views.home"))


# View and function that handles the add order functionality
@views.route("/orders/add", methods=["POST", "GET"])
def add_order():
    if (check_session_exists()): # Check is user is logged in
        orders_list = database_select_all_orders() # Get current order data
        if request.method == "POST":
            # Retrieves all form data
            order_number = request.form.get("ordernumber", "")
            order_date = request.form.get("orderdate", "")
            customer_name = request.form.get("customername", "")
            company = request.form.get("company", "")
            order_total = request.form.get("ordertotal", "")
            order_status = request.form.get("orderstatus", "").title()
            item_count = request.form.get("itemcount", "")
            input_data = [order_number, order_date, customer_name, company, order_total, order_status, item_count]
            validation_dict = validate_order(input_data) # Dictionary set with values returned from validate_order
            is_valid = validation_dict["is_valid"] # Boolean value from dictionary. True if all data is valid, false if atleast one is invalid
            validation_message = validation_dict["validation_message"] # Appropriate message returned, based on success or specific error 
            # If valid, add order to table and redirect to orders view. Else if fail, redirect to add order
            if (is_valid):
                if database_add_order(input_data):
                    return redirect(url_for("views.orders"))
                else:
                    return redirect(url_for("views.add_order"))
            # Else flash set with error message and redirected to add order
            else:
                flash(validation_message, category="error")
                return redirect(url_for("views.add_order"))
        # Else condition when not post request and is get request, render orders table with paramater values passed in
        else:
            return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"], add_in_process = True)
    # If not logged in, redirect to home view
    else:
        return redirect(url_for("views.home"))

# View and function that renders contact-us page. If not signed in, redirects to home page
@views.route("/contact-us")
def contact_us():
    if (check_session_exists()):
        return render_template("contact-us.html", logged_in = True, logged_in_user = session["user"], user_type = session["type"])
    else:
        return redirect(url_for("views.home"))

# View and function that handles the sign-in functionality
@views.route("/sign-in", methods=["POST", "GET"])
def sign_in():
    if (not(check_session_exists())): # Check if user is not logged in
        # Handle post request
        if request.method == "POST":
            username = request.form.get("signin-username", "")
            password= request.form.get("signin-password", "")
            input_data = [username, password]
            # If user exists in data table, set session and redirect to home
            if (database_search_user(input_data)):
                session["user"] = username
                session["type"] = database_search_user_type(username)[0]
                session.permanent = True
                return redirect(url_for("views.home"))
            # Else set flash with error message and render sign in 
            else:
                message = "Username or password is incorrect. Please try again"
                flash(message, category="error")
                return render_template("sign-in.html")
        return render_template("sign-in.html")
    # If not logged in, redirect to home view
    else:
        return redirect(url_for("views.home"))

# View and function that handles the sign-up functionality
@views.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if (not(check_session_exists())): # Check if user is not logged in
        # Handle post request
        if request.method == "POST":
            # Retrieves all form data
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            type = request.form.get("user_type", "regular")
            input_data = [username, password, type]
            validation_dict = validate_sign_up(input_data) # Dictionary set with values returned from validate_order
            is_valid = validation_dict["is_valid"] # Boolean value from dictionary. True if all data is valid, false if atleast one is invalid
            validation_message = validation_dict["validation_message"] # Appropriate message returned, based on success or specific error 
            userExists = database_search_user_name(username) # Check if user exists in data table

            # If data is valid, then check if user does not exist
            if (is_valid):
                if (not(userExists)): # If user does not exist, then add to database and set flash with success message and render sign in
                    if (database_add_user(input_data)):
                        flash(validation_message, category="success")
                        return render_template("sign-in.html")
                # Else if user exists, set flash error message and render sign up
                else:
                    flash("Username: " + username + " already exists.", category="error")
                    return render_template("sign-up.html")
            # Else set flash with error message and render sign in 
            else:
                flash(validation_message, category="error")
                return render_template("sign-up.html")
        # Handles get request
        else:
            return render_template("sign-up.html")
    # If not logged in, redirect to home view
    else:
        return redirect(url_for("views.home"))

# View and function that deletes current session if logged in and redirects to sign-in page. If not logged in, redirect to home page
@views.route("/sign-out")
def signOut():
    # If user is logged in, delete current session and redirect to sign view
    if (check_session_exists()):
        session.pop("user", None)
        return redirect(url_for("views.sign_in"))
    # If not logged in, redirect to home view
    else:
        return redirect(url_for("views.home"))
    
