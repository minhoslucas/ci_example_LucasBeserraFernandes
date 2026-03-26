import unittest
from app.user_management import set_db, create_user, get_user, \
    list_users, delete_user
from app.db.db_mock import MockDB


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDB()
        set_db(self.mock_db)

    def test_create_user_success(self):
        data = create_user("Example", "example@domain.com",
                           "StrongP@ssw0rd", "1990-01-01")
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Example")

    def test_create_user_invalid_name(self):
        with self.assertRaises(ValueError):
            create_user("Alex", "alex@domain.com",
                        "StrongP@ssw0rd", "1990-01-01")

    def test_create_user_invalid_email(self):
        with self.assertRaises(ValueError):
            create_user("Example", "invalid-email",
                        "StrongP@ssw0rd", "1990-01-01")

    def test_create_user_invalid_dob(self):
        with self.assertRaises(ValueError):
            create_user("Example", "example@domain.com",
                        "StrongP@ssw0rd", "31-12-1990")

    def test_create_user_weak_password(self):
        with self.assertRaises(ValueError):
            create_user("Example", "example@domain.com",
                        "weak", "1990-01-01")

    def test_get_user_after_create(self):
        user = create_user("Example", "example@domain.com",
                           "StrongP@ssw0rd", "1990-01-01")
        self.assertEqual(get_user(user["id"])["email"], "example@domain.com")

    def test_list_users_after_create(self):
        create_user("Example", "example@domain.com",
                    "StrongP@ssw0rd", "1990-01-01")
        self.assertEqual(len(list_users()), 1)

    def test_delete_user(self):
        user = create_user("Example", "example@domain.com",
                           "StrongP@ssw0rd", "1990-01-01")
        self.assertTrue(delete_user(user["id"]))
        self.assertIsNone(get_user(user["id"]))

    def test_is_sorted(self):
        user1 = create_user("Example", "example@domain.com",
                           "StrongP@ssw0rd", "1990-01-01")
        user2 = create_user("Example", "axample@domain.com",
                           "StrongP@ssw0rd", "1990-01-01")
        user3 = create_user("Example", "bxample@domain.com",
                           "StrongP@ssw0rd", "1990-01-01")
        
        self.assertTrue(list_users() == sorted(list_users(), key= lambda d: d['email']))
if __name__ == "__main__":
    unittest.main()
