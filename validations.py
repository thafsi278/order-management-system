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
    signup_is_valid = False
    # validations to check and set return string
    if username_length < 6 or username_length > 18:
        return_string = "Username must be greater than 6, and less than 18 characters."
    elif password_length < 6 or password_length > 18:
        return_string = "Password must greater than 6, and less than 18 characters."
    elif regex.search(password) == None:
        return_string = "Password must contain atleast one special character."
    elif not(has_numbers(password)):
        return_string = "Password must contain atleast one number."
    # if all checks are complete, set successful return string message and is valid to true
    else: 
        return_string = "User: " + username + " has been successfully registered!"
        signup_is_valid = True
    return_dict = dict(is_valid = signup_is_valid, validation_message = return_string)
    return return_dict

## Validates order data, entered by user. Returns dictionary with boolean and appropriate string message, based on conditions below.
def validate_order(input_data):
    return_string = ""
    order_number = input_data[0]
    order_date = input_data[1]
    customer_name = input_data[2]
    company = input_data[3]
    order_total = input_data[4]
    item_count = input_data[6]
    order_is_valid = False
    date_is_valid = False
    # validations to check and set return string
    try:
        datetime.strptime(order_date, "%Y-%m-%d").date()
        date_is_valid = True
    except:
        date_is_valid = False
    if (not(order_number.isnumeric())):
        return_string = "Order number must be numbers only."
    elif (not(date_is_valid)):
        return_string = "Date must be in ISO format e.g. 2042-12-23."
    elif (len(customer_name) < 3 or len(customer_name) > 13):
        return_string = "Name must be between 3, and 13 characters."
    elif (len(company) < 3 or len(company) > 13):
        return_string = "Company must be between 3, and 13 characters."
    elif (not(is_float(order_total))):
        return_string = "Total must be a number."
    elif (not(is_int(item_count))):
        return_string = "Item count must be a number."
    # if all checks are complete, set is valid to true
    else:
        order_is_valid = True
    return_dict = dict(is_valid = order_is_valid, validation_message = return_string)
    return return_dict