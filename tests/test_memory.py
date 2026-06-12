import unittest
from src.db.backend.memory import MemoryDB
from src.db.backend.errors import InvalidAgeError, InvalidPhoneError, DuplicateIDError, TableNotFoundError


class TestMemoryDB(unittest.TestCase):

    def setUp(self):
        self.repo = MemoryDB()
        self.repo.create_table(
            "people",
            ("id", "first_name", "second_name", "age", "sex", "phone_number")
        )

    def test_create_record_ok(self):
        self.repo.insert_record("people", {
            "id": 1, "first_name": "Иван", "second_name": "Иванов",
            "age": 20, "sex": "M", "phone_number": "+7 (999) 111-22-33"
        })
        records = self.repo.select_records("people", id=1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["first_name"], "Иван")

    def test_create_record_duplicate_id(self):
        self.repo.insert_record("people", {
            "id": 1, "first_name": "Иван", "second_name": "Иванов",
            "age": 20, "sex": "M", "phone_number": "+7 (999) 111-22-33"
        })
        with self.assertRaises(DuplicateIDError):
            self.repo.insert_record("people", {
                "id": 1, "first_name": "Пётр", "second_name": "Петров",
                "age": 14, "sex": "M", "phone_number": "+7 (991) 111-22-33"
            })

    def test_create_record_invalid_age(self):
        with self.assertRaises(InvalidAgeError):
            self.repo.insert_record("people", {
                "id": 2, "first_name": "Анастасия", "second_name": "Сидорова",
                "age": -5, "sex": "Ж", "phone_number": "+7 (999) 788-99-44"
            })

    def test_create_record_invalid_phone(self):
        invalid_phones = ["89997775544", "+7(999)2223344", "123", "+7 (999) 22-44-55"]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                with self.assertRaises(InvalidPhoneError):
                    self.repo.insert_record("people", {
                        "id": 3, "first_name": "Андрей", "second_name": "Алексеев",
                        "age": 30, "sex": "М", "phone_number": phone
                    })

    def test_select_record_with_filters(self):
        self.repo.insert_record("people", {
            "id": 1, "first_name": "Иван", "second_name": "Иванов",
            "age": 20, "sex": "М", "phone_number": "+7 (999) 111-22-33"
        })
        self.repo.insert_record("people", {
            "id": 2, "first_name": "Анна", "second_name": "Петрова",
            "age": 22, "sex": "Ж", "phone_number": "+7 (999) 222-33-44"
        })
        self.assertEqual(len(self.repo.select_records("people", id=1)), 1)
        self.assertEqual(len(self.repo.select_records("people", first_name="Анна")), 1)
        self.assertEqual(len(self.repo.select_records("people", second_name="Иванов")), 1)
        self.assertEqual(len(self.repo.select_records("people", age=20)), 1)
        self.assertEqual(len(self.repo.select_records("people", sex="Ж")), 1)

    def test_update_record_success(self):
        self.repo.insert_record("people", {
            "id": 1, "first_name": "Иван", "second_name": "Иванов",
            "age": 20, "sex": "М", "phone_number": "+7 (999) 111-22-33"
        })
        updated = self.repo.update_record_with_id("people", 1, first_name="Ваня", age=21)
        self.assertTrue(updated)
        record = self.repo.select_records("people", id=1)[0]
        self.assertEqual(record["first_name"], "Ваня")
        self.assertEqual(record["age"], 21)

    def test_update_record_not_found(self):
        updated = self.repo.update_record_with_id("people", 999, first_name="Никто")
        self.assertFalse(updated)

    def test_update_record_validation(self):
        self.repo.insert_record("people", {
            "id": 1, "first_name": "Иван", "second_name": "Иванов",
            "age": 20, "sex": "М", "phone_number": "+7 (999) 111-22-33"
        })
        with self.assertRaises(InvalidAgeError):
            self.repo.update_record_with_id("people", 1, age=-10)
        with self.assertRaises(InvalidPhoneError):
            self.repo.update_record_with_id("people", 1, phone_number="не_телефон")

    def test_delete_record(self):
        self.repo.insert_record("people", {
            "id": 1, "first_name": "Иван", "second_name": "Иванов",
            "age": 20, "sex": "М", "phone_number": "+7 (999) 111-22-33"
        })
        self.assertTrue(self.repo.delete_record("people", 1))
        self.assertEqual(len(self.repo.select_records("people")), 0)
        self.assertFalse(self.repo.delete_record("people", 1))

    def test_clear_all_records(self):
        self.repo.insert_record("people", {
            "id": 1, "first_name": "Иван", "second_name": "Иванов",
            "age": 20, "sex": "М", "phone_number": "+7 (999) 111-22-33"
        })
        self.repo.insert_record("people", {
            "id": 2, "first_name": "Анна", "second_name": "Петрова",
            "age": 22, "sex": "Ж", "phone_number": "+7 (999) 222-33-44"
        })
        self.repo.clear_all_table("people")
        self.assertEqual(len(self.repo.select_records("people")), 0)

    def test_load_table_not_found(self):
        with self.assertRaises(TableNotFoundError):
            self.repo.select_records("Таблицы не существует")
