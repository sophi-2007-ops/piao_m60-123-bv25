import unittest
from src.db.backend.memory import MemoryDB
from src.db.backend.errors import InvalidAgeError, InvalidPhoneError, DublicateIDError


class TestMemoryDB(unittest.TestCase):
 
 
    def setUp(self):
        self.repo = MemoryDB()


    def test_create_record_ok(self):
        record = self.repo.create_record(1, "Иван", "Иванов", 20, "M", "+7 (999) 111-22-33")
        self.assertEqual(record, (1, "Иван", "Иванов", 20, "M", "+7 (999) 111-22-33"))


    def test_create_record_deblicate_id(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "M", "+7 (999) 111-22-33")
        with self.assertRaises(DublicateIDError):
            self.repo.create_record(1, "Пётр", "Петров", 14, "M", "+7 (991) 111-22-33")


    def test_create_record_invalid_age(self):
        with self.assertRaises(InvalidAgeError):
            self.repo.create_record(2, "Анастасия", "Сидорова", -5, "Ж", "+7 (999) 788-99-44")


    def test_create_record_invalid_phone(self):
        invalid_phones = ["89997775544", "+7(999)2223344", "123", "+7 (999) 22-44-55"]
        for phone in invalid_phones:
            with self.subTest(phone = phone):
                with self.assertRaises(InvalidPhoneError):
                    self.repo.create_record(3, "Андрей", "Алексеев", 30, "М", phone)


    def test_select_record_with_filters(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", "+7 (999) 111-22-33")
        self.repo.create_record(2, "Анна", "Петрова", 22, "Ж", "+7 (999) 222-33-44")
        res_id = self.repo.select_record(person_id=1)
        self.assertEqual(len(res_id), 1)
        res_name = self.repo.select_record(first_name="Анна")
        self.assertEqual(len(res_name), 1)
        res_surname = self.repo.select_record(second_name="Иванов")
        self.assertEqual(len(res_surname), 1)
        res_age = self.repo.select_record(age=20)
        self.assertEqual(len(res_age), 1)
        res_sex = self.repo.select_record(sex="Ж")
        self.assertEqual(len(res_sex), 1)
        res_phone = self.repo.select_record(phone_number="+7 (999) 111-22-33")
        self.assertEqual(len(res_phone), 1)


    def test_update_record_success(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", "+7 (999) 111-22-33")
        updated = self.repo.update_record(1, first_name="Ваня", age=21)
        self.assertTrue(updated)
        record = self.repo.select_record(person_id=1)[0]
        self.assertEqual(record[1], "Ваня")
        self.assertEqual(record[3], 21)


    def test_update_record_not_found(self):
        updated = self.repo.update_record(999, first_name="Никто")
        self.assertFalse(updated)


    def test_update_record_validation(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", "+7 (999) 111-22-33")   
        with self.assertRaises(InvalidAgeError):
            self.repo.update_record(1, age=-10)
        with self.assertRaises(InvalidPhoneError):
            self.repo.update_record(1, phone_number="не_телефон")


    def test_delete_record(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", "+7 (999) 111-22-33")
        self.assertTrue(self.repo.delete_record(1))
        self.assertEqual(len(self.repo.select_record()), 0)
        self.assertFalse(self.repo.delete_record(1))


    def test_clear_all_records(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", "+7 (999) 111-22-33")
        self.repo.create_record(2, "Анна", "Петрова", 22, "Ж", "+7 (999) 222-33-44")
        self.repo.clear_table()
        self.assertEqual(len(self.repo.select_record()), 0)


if __name__ == "__main__":
    unittest.main()
