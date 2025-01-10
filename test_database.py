import unittest
import database

class TestDatabase(unittest.TestCase):

    # Test retrieval of all orders data
    def test_select_all_order(self):
        result = database.database_select_all_orders()
        self.assertTrue(result) 

    # Test add user
    def test_add_user(self):
        pass_result = database.database_add_user(["test_regular_username", "test__regular_password", "Regular"])
        fail_result = database.database_add_user(["test_regular_username", "test__regular_password", "Reg"])
        self.assertEqual(pass_result, True)
        self.assertEqual(fail_result, False)

    # Test search user
    def test_search_user(self):
        pass_result = database.database_search_user(["testregular", "00000!"])
        fail_result = database.database_search_user(["testregular", "00000"])
        self.assertEqual(pass_result, True)
        self.assertEqual(fail_result, False)

    # Test search username
    def test_search_user_name(self):
        pass_result = database.database_search_user_name("testregular")
        fail_result = database.database_search_user_name("testregular1")
        self.assertEqual(pass_result, True)
        self.assertEqual(fail_result, False)

    # Test search user type
    def test_search_user_type(self):
        pass_result1 = database.database_search_user_type("testregular")
        pass_result2 = database.database_search_user_type("testadmin")
        fail_result1 = database.database_search_user_type("testregular1")
        fail_result2 = database.database_search_user_type("testregular1")
        self.assertIn("Regular", pass_result1)
        self.assertIn("Administrator", pass_result2)
        self.assertFalse(fail_result1)
        self.assertFalse(fail_result2)
    
    # Test retrieval of specific order
    def test_get_order(self):
        order_id = "1"
        pass_result = database.database_get_order(order_id)
        fail_result = database.database_get_order("test")
        self.assertEqual(str(pass_result[0]), order_id)
        self.assertEqual(fail_result, False)
    
    # Test add order
    def test_add_order(self):
        pass_order_list = [12, "2024-06-19", "test_name", "test_company", 52.99, "Paid", 8]
        fail_order_list = [11, "2024-06-1", 5, "test_company", "test_total", "Paid", 8] 
        pass_result = database.database_add_order(pass_order_list)
        fail_result = database.database_add_order(fail_order_list)
        self.assertTrue(pass_result)
        self.assertFalse(fail_result)
    
    # Test edit order
    def test_edit_order(self):
        pass_order_list = [1, "2023-05-19", "test_name_edited", "test_company_edited", 99.99, "Unpaid", 15]
        fail_order_list = [45, "2024-06-1", 5, "test_company", 42.99, "Yes", "test_item_count"]
        pass_result = database.database_add_order(pass_order_list)
        fail_result = database.database_add_order(fail_order_list)
        self.assertTrue(pass_result)
        self.assertFalse(fail_result) 
    
    # Test delete order
    def test_delete_order(self):
        pass_result = database.database_delete_order("1")
        fail_result = database.database_delete_order("test")
        self.assertEqual(pass_result, True)
        self.assertEqual(fail_result, False)

if __name__ == '__main__':
    unittest.main()