from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import *
from validations import *

views = Blueprint(__name__, "views")

def check_session_exists():
    if "user" in session:
        return True
    else:
        return False

@views.route("/index")
def home():
    if (check_session_exists()):
        return render_template("index.html", userIsLoggedIn = True, currentUser = session["user"], userType = session["type"])
    else:
        return redirect(url_for("views.signIn"))

@views.route("/orders")
def orders():
    if (check_session_exists()):
        ordersList = database_select_all_orders()
        return render_template("orders.html", dataList = ordersList, userIsLoggedIn = True, currentUser = session["user"], userType = session["type"])
    else:
        return redirect(url_for("views.home"))
    
@views.route("/orders/edit/<orderId>", methods=["POST", "GET"])
def editOrder(orderId):
    if (check_session_exists()):
        ordersList = database_select_all_orders()
        if request.method == "POST":
            orderNumber = request.form.get("ordernumber", "")
            orderDate = request.form.get("orderdate", "")
            customerName = request.form.get("customername", "")
            company = request.form.get("company", "")
            orderTotal = request.form.get("ordertotal", "")
            orderStatus = request.form.get("orderstatus", "").title()
            itemCount = request.form.get("itemcount", "")
            inputData = [orderNumber, orderDate, customerName, company, orderTotal, orderStatus, itemCount]
            dict = validate_order(inputData)
            isValid = dict["is_valid"]
            validationMessage = dict["validation_message"]
            if (isValid):
                if database_edit_order(inputData):
                    return redirect(url_for("views.orders"))
                else:
                    return render_template("orders.html", dataList = ordersList, userIsLoggedIn = True, currentUser = session["user"])
            else:
                flash(validationMessage, category="error")
                return redirect(url_for("views.editOrder", orderId = orderId))
        else:
            return render_template("orders.html", dataList = ordersList, userIsLoggedIn = True, currentUser = session["user"], editInProcess = True, id = orderId)
    else:
        return redirect(url_for("views.home"))

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

@views.route("/orders/add", methods=["POST", "GET"])
def addOrder():
    if (check_session_exists()):
        ordersList = database_select_all_orders()
        if request.method == "POST":
            orderNumber = request.form.get("ordernumber", "")
            orderDate = request.form.get("orderdate", "")
            customerName = request.form.get("customername", "")
            company = request.form.get("company", "")
            orderTotal = request.form.get("ordertotal", "")
            orderStatus = request.form.get("orderstatus", "").title()
            itemCount = request.form.get("itemcount", "")
            inputData = [orderNumber, orderDate, customerName, company, orderTotal, orderStatus, itemCount]
            dict = validate_order(inputData)
            isValid = dict["is_valid"]
            validationMessage = dict["validation_message"]
            if (isValid):
                if database_add_order(inputData):
                    return redirect(url_for("views.orders"))
                else:
                    return redirect(url_for("views.addOrder"))
            else:
                flash(validationMessage, category="error")
                return redirect(url_for("views.addOrder"))
        else:
            return render_template("orders.html", dataList = ordersList, userIsLoggedIn = True, currentUser = session["user"], addInProcess = True)
    else:
        return redirect(url_for("views.home"))


@views.route("/contact-us")
def contactUs():
    if (check_session_exists()):
        return render_template("contact-us.html", userIsLoggedIn = True, currentUser = session["user"], userType = session["type"])
    else:
        return redirect(url_for("views.home"))

@views.route("/sign-in", methods=["POST", "GET"])
def signIn():
    if (not(check_session_exists())):
        if request.method == "POST":
            username = request.form.get("signin-username", "")
            password= request.form.get("signin-password", "")
            inputData = [username, password]
            if (database_search_user(inputData)):
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

@views.route("/sign-up", methods=["POST", "GET"])
def signUp():
    if (not(check_session_exists())):
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            type = request.form.get("user_type", "regular")
            inputData = [username, password, type]
            dict = validate_sign_up(inputData)
            isValid = dict["is_valid"]
            validationMessage = dict["validation_message"]
            userExists = database_search_user_name(username)
            if (isValid):
                if (not(userExists)):
                    if (database_add_user(inputData)):
                        flash(validationMessage, category="success")
                        return render_template("sign-in.html")
                else:
                    flash("Username: " + username + " already exists.", category="error")
                    return render_template("sign-up.html")
            else:
                flash(validationMessage, category="error")
                return render_template("sign-up.html")
        else:
            return render_template("sign-up.html")
    else:
        return redirect(url_for("views.home"))


@views.route("/sign-out")
def signOut():
    if (check_session_exists()):
        session.pop("user", None)
        return redirect(url_for("views.signIn"))
    else:
        return redirect(url_for("views.home"))
    
