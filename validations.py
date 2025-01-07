import re
from datetime import datetime

## Regex variable for special characters
regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

## Helper function to check if string contains a number
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

## Helper function to check if number is a float
def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

## Helper function to check if number is an integer
def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

## Validates sign up data, entered by user. Returns dictionary with boolean and appropriate string message, based on conditions below.
def validate_sign_up(input_data):
    return_string = ""
    username = input_data[0]
    password = input_data[1]
    username_length = len(username)
    password_length = len(password)
    type = input_data[2]
    is_valid = False
    if username_length < 6 or username_length > 18:
        return_string = "Username must be greater than 6, and less than 18 characters."
    elif password_length < 6 or password_length > 18:
        return_string = "Password must greater than 6, and less than 18 characters."
    elif regex.search(password) == None:
        return_string = "Password must contain atleast one special character."
    elif not(has_numbers(password)):
        return_string = "Password must contain atleast one number."
    else:
        return_string = "User: " + username + " has been successfully registered!"
        is_valid = True
    returnDict = dict(is_valid = is_valid, validation_message = return_string)
    return returnDict

## Validates order data, entered by user. Returns dictionary with boolean and appropriate string message, based on conditions below.
def validate_order(input_data):
    return_string = ""
    order_number = input_data[0]
    order_date = input_data[1]
    customer_name = input_data[2]
    company = input_data[3]
    order_total = input_data[4]
    item_count = input_data[6]
    is_valid = False
    is_valid_date = False
    try:
        datetime.strptime(order_date, "%Y-%m-%d").date()
        is_valid_date = True
    except:
        is_valid_date = False
    if (not(order_number.isnumeric())):
        return_string = "Order number must be numbers only."
    elif (not(is_valid_date)):
        return_string = "Date must be in ISO format e.g. 2042-12-23."
    elif (len(customer_name) < 3 or len(customer_name) > 13):
        return_string = "Name must be between 3, and 13 characters."
    elif (len(company) < 3 or len(company) > 7):
        return_string = "Company must be between 3, and 13 characters."
    elif (not(is_float(order_total))):
        return_string = "Total must be a number."
    elif (not(is_int(item_count))):
        return_string = "Item count must be a number."
    else:
        is_valid = True
    returnDict = dict(is_valid = is_valid, validation_message = return_string)
    return returnDict