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
        return redirect(url_for("views.signIn"))

# View and function that renders orders page. If not signed in, redirect and call home function
@views.route("/orders")
def orders():
    if (check_session_exists()):
        orders_list = database_select_all_orders()
        return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"], user_type = session["type"])
    else:
        return redirect(url_for("views.home"))

# View and function that handles the edit order functionality
@views.route("/orders/edit/<orderId>", methods=["POST", "GET"])
def editOrder(orderId):
    if (check_session_exists()): # Check is user is logged in
        orders_list = database_select_all_orders() # Retrieve all orders from data table
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
            if (is_valid):
                if database_edit_order(input_data):
                    return redirect(url_for("views.orders"))
                else:
                    return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"])
            else:
                flash(validation_message, category="error")
                return redirect(url_for("views.editOrder", orderId = orderId))
        else:
            return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"], editInProcess = True, id = orderId)
    else:
        return redirect(url_for("views.home"))

# View and function that handles the delete order functionality
@views.route("/orders/delete/<orderId>", methods=["POST", "GET"])
def deleteOrder(orderId):
    if (check_session_exists()):
        if session["type"] == "Administrator":
            if database_delete_order(orderId):
                return redirect(url_for("views.orders"))
            else:
                return redirect(url_for("views.orders"))
        else:
            message = "User: " + session["user"] + " is not authorised to perform this action. Please sign in as ADMIN."
            flash(message, category="error")
            return redirect(url_for("views.orders"))
    else:
        return redirect(url_for("views.home"))


# View and function that handles the add order functionality
@views.route("/orders/add", methods=["POST", "GET"])
def addOrder():
    if (check_session_exists()):
        orders_list = database_select_all_orders()
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
            if (is_valid):
                if database_add_order(input_data):
                    return redirect(url_for("views.orders"))
                else:
                    return redirect(url_for("views.addOrder"))
            else:
                flash(validation_message, category="error")
                return redirect(url_for("views.addOrder"))
        else:
            return render_template("orders.html", data_list = orders_list, logged_in = True, logged_in_user = session["user"], addInProcess = True)
    else:
        return redirect(url_for("views.home"))

# View and function that renders contact-us page. If not signed in, redirects to home page
@views.route("/contact-us")
def contactUs():
    if (check_session_exists()):
        return render_template("contact-us.html", logged_in = True, logged_in_user = session["user"], user_type = session["type"])
    else:
        return redirect(url_for("views.home"))

# View and function that handles the sign-in functionality
@views.route("/sign-in", methods=["POST", "GET"])
def signIn():
    if (not(check_session_exists())):
        if request.method == "POST":
            username = request.form.get("signin-username", "")
            password= request.form.get("signin-password", "")
            input_data = [username, password]
            if (database_search_user(input_data)):
                session["user"] = username
                session["type"] = database_search_user_type(username)[0]
                session.permanent = True
                return redirect(url_for("views.home"))
            else:
                message = "Username or password is incorrect. Please try again"
                flash(message, category="error")
                return render_template("sign-in.html")
        return render_template("sign-in.html")
    else:
        return redirect(url_for("views.home"))

# View and function that handles the sign-up functionality
@views.route("/sign-up", methods=["POST", "GET"])
def signUp():
    if (not(check_session_exists())):
        if request.method == "POST":
            # Retrieves all form data
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            type = request.form.get("user_type", "regular")
            input_data = [username, password, type]
            validation_dict = validate_sign_up(input_data) # Dictionary set with values returned from validate_order
            is_valid = validation_dict["is_valid"] # Boolean value from dictionary. True if all data is valid, false if atleast one is invalid
            validation_message = validation_dict["validation_message"] # Appropriate message returned, based on success or specific error 
            userExists = database_search_user_name(username)
            if (is_valid):
                if (not(userExists)):
                    if (database_add_user(input_data)):
                        flash(validation_message, category="success")
                        return render_template("sign-in.html")
                else:
                    flash("Username: " + username + " already exists.", category="error")
                    return render_template("sign-up.html")
            else:
                flash(validation_message, category="error")
                return render_template("sign-up.html")
        else:
            return render_template("sign-up.html")
    else:
        return redirect(url_for("views.home"))

# View and function that deletes current session if logged in and redirects to sign-in page. If not logged in, redirect to home page
@views.route("/sign-out")
def signOut():
    if (check_session_exists()):
        session.pop("user", None)
        return redirect(url_for("views.signIn"))
    else:
        return redirect(url_for("views.home"))
    
