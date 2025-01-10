import unittest
import validations

class TestDatabase(unittest.TestCase):

    # Test helper function that checks if contains number
    def test_has_numbers(self):
        pass_result = validations.has_numbers("test1")
        fail_result = validations.has_numbers("test")
        self.assertEqual(pass_result, True)
        self.assertEqual(fail_result, False)
    
    # Test helper function that checks if float
    def test_is_float(self):
        pass_result = validations.is_float(15.50)
        fail_result = validations.is_float("test")
        self.assertEqual(pass_result, True)
        self.assertEqual(fail_result, False)

    # Test helper function that checks if int 
    def test_is_int(self):
        pass_result = validations.is_int(15)
        fail_result = validations.is_int("test")
        self.assertEqual(pass_result, True)
        self.assertEqual(fail_result, False)

    # Test sign up validation and each scenario with return message and boolean
    def test_sign_up(self):
        # Success validation test
        pass_result = validations.validate_sign_up(["testusername", "testpassword1!", 1])
        pass_result_is_valid = pass_result["is_valid"]
        pass_result_message = pass_result["validation_message"]
        self.assertEqual(pass_result_is_valid, True)
        self.assertEqual(pass_result_message, "User: testusername has been successfully registered!")

        # Username length validation test
        fail_result1 = validations.validate_sign_up(["test", "testpassword1!", 1])
        fail_result1_is_valid = fail_result1["is_valid"]
        fail_result1_message = fail_result1["validation_message"]
        self.assertEqual(fail_result1_is_valid, False)
        self.assertEqual(fail_result1_message, "Username must be greater than 6, and less than 18 characters.")

        # Password length validation test
        fail_result2 = validations.validate_sign_up(["testusername", "test", 1])
        fail_result2_is_valid = fail_result2["is_valid"]
        fail_result2_message = fail_result2["validation_message"]
        self.assertEqual(fail_result2_is_valid, False)
        self.assertEqual(fail_result2_message, "Password must greater than 6, and less than 18 characters.")

        # Password special character validation test 
        fail_result3 = validations.validate_sign_up(["testusername", "testpassword1", 1])
        fail_result3_is_valid = fail_result3["is_valid"]
        fail_result3_message = fail_result3["validation_message"]
        self.assertEqual(fail_result3_is_valid, False)
        self.assertEqual(fail_result3_message, "Password must contain atleast one special character.")

        # Password number validation test
        fail_result4 = validations.validate_sign_up(["testusername", "testpassword!", 1])
        fail_result4_is_valid = fail_result4["is_valid"]
        fail_result4_message = fail_result4["validation_message"]
        self.assertEqual(fail_result4_is_valid, False)
        self.assertEqual(fail_result4_message, "Password must contain atleast one number.")
    

    def test_order(self):
        # Success validation test
        pass_order_list = ["12", "2024-06-19", "test_name", "test_company", 52.99, "Paid", 8]
        pass_result = validations.validate_order(pass_order_list)
        pass_result_is_valid = pass_result["is_valid"]
        self.assertEqual(pass_result_is_valid, True)

        # Order number validation test
        pass_order_list = ["test", "2024-06-19", "test_name", "test_company", 52.99, "Paid", 8]
        fail_result1 = validations.validate_order(pass_order_list)
        fail_result1_is_valid = fail_result1["is_valid"]
        fail_result1_message = fail_result1["validation_message"]
        self.assertEqual(fail_result1_is_valid, False)
        self.assertEqual(fail_result1_message, "Order number must be numbers only.")

        # Order date validation test
        pass_order_list = ["12", "2024/06/19", "test_name", "test_company", 52.99, "Paid", 8]
        fail_result2 = validations.validate_order(pass_order_list)
        fail_result2_is_valid = fail_result2["is_valid"]
        fail_result2_message = fail_result2["validation_message"]
        self.assertEqual(fail_result2_is_valid, False)
        self.assertEqual(fail_result2_message, "Date must be in ISO format e.g. 2042-12-23.")

        # Order name validation test
        pass_order_list = ["12", "2024-06-19", "te", "test_company", 52.99, "Paid", 8]
        fail_result3 = validations.validate_order(pass_order_list)
        fail_result3_is_valid = fail_result3["is_valid"]
        fail_result3_message = fail_result3["validation_message"]
        self.assertEqual(fail_result3_is_valid, False)
        self.assertEqual(fail_result3_message, "Name must be between 3, and 13 characters.")

        # Order comapny validation test
        pass_order_list = ["12", "2024-06-19", "test_name", "te", 52.99, "Paid", 8]
        fail_result4 = validations.validate_order(pass_order_list)
        fail_result4_is_valid = fail_result4["is_valid"]
        fail_result4_message = fail_result4["validation_message"]
        self.assertEqual(fail_result4_is_valid, False)
        self.assertEqual(fail_result4_message, "Company must be between 3, and 13 characters.")

        # Order total validation test
        pass_order_list = ["12", "2024-06-19", "test_name", "test_company", "test_total", "Paid", 8]
        fail_result5 = validations.validate_order(pass_order_list)
        fail_result5_is_valid = fail_result5["is_valid"]
        fail_result5_message = fail_result5["validation_message"]
        self.assertEqual(fail_result5_is_valid, False)
        self.assertEqual(fail_result5_message, "Total must be a number.")

        # Order item count validation test
        pass_order_list = ["12", "2024-06-19", "test_name", "test_company", 52.99, "Paid", "test_item_count"]
        fail_result6 = validations.validate_order(pass_order_list)
        fail_result6_is_valid = fail_result6["is_valid"]
        fail_result6_message = fail_result6["validation_message"]
        self.assertEqual(fail_result6_is_valid, False)
        self.assertEqual(fail_result6_message, "Item count must be a number.")

if __name__ == '__main__':
    unittest.main()