import unittest
import shutil
from src.db.backend.file_json import FileDatabase_JSON
from src.db.backend.file_csv import FileDatabase_CSV
from src.db.backend.errors import (
    InvalidAgeError, InvalidPhoneError, DuplicateIDError,
    TableAlreadyExistsError, TableNotFoundError
)

COLUMNS = ("id", "first_name", "second_name", "age", "sex", "phone_number")

VALID_RECORD = {
    "id": 1, "first_name": "Иван", "second_name": "Иванов",
    "age": 20, "sex": "М", "phone_number": "+7 (999) 111-22-33"
}

class BaseFileDatabaseTest:

    db_class = None
    test_dir = None

    def setUp(self):
        self.repo = self.db_class(self.test_dir)
        self.repo.create_table("people", COLUMNS)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_table_ok(self):
        self.repo.create_table("orders", ("id", "name"))
        self.assertTrue(self.repo._table_exists("orders"))

    def test_create_table_already_exists(self):
        with self.assertRaises(TableAlreadyExistsError):
            self.repo.create_table("people", COLUMNS)

    def test_load_table_not_found(self):
        with self.assertRaises(TableNotFoundError):
            self.repo._load_table("несуществующая")

    def test_insert_and_select(self):
        self.repo.insert_record("people", VALID_RECORD)
        records = self.repo.select_records("people")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["first_name"], "Иван")

    def test_insert_duplicate_id(self):
        self.repo.insert_record("people", VALID_RECORD)
        with self.assertRaises(DuplicateIDError):
            self.repo.insert_record("people", VALID_RECORD)

    def test_insert_invalid_age(self):
        record = {**VALID_RECORD, "id": 2, "age": -5}
        with self.assertRaises(InvalidAgeError):
            self.repo.insert_record("people", record)

    def test_insert_invalid_phone(self):
        invalid_phones = ["89997775544", "+7(999)2223344", "123"]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                with self.assertRaises(InvalidPhoneError):
                    self.repo.insert_record("people", {**VALID_RECORD, "id": 3, "phone_number": phone})

    def test_select_with_filters(self):
        self.repo.insert_record("people", VALID_RECORD)
        self.repo.insert_record("people", {
            "id": 2, "first_name": "Анна", "second_name": "Петрова",
            "age": 22, "sex": "Ж", "phone_number": "+7 (999) 222-33-44"
        })
        self.assertEqual(len(self.repo.select_records("people", id=1)), 1)
        self.assertEqual(len(self.repo.select_records("people", first_name="Анна")), 1)
        self.assertEqual(len(self.repo.select_records("people", sex="Ж")), 1)

    def test_update_record_success(self):
        self.repo.insert_record("people", VALID_RECORD)
        result = self.repo.update_record_with_id("people", 1, first_name="Ваня", age=25)
        self.assertTrue(result)
        record = self.repo.select_records("people", id=1)[0]
        self.assertEqual(record["first_name"], "Ваня")
        self.assertEqual(record["age"], 25)

    def test_update_record_not_found(self):
        result = self.repo.update_record_with_id("people", 999, first_name="Никто")
        self.assertFalse(result)

    def test_update_record_invalid_age(self):
        self.repo.insert_record("people", VALID_RECORD)
        with self.assertRaises(InvalidAgeError):
            self.repo.update_record_with_id("people", 1, age=-10)

    def test_update_record_invalid_phone(self):
        self.repo.insert_record("people", VALID_RECORD)
        with self.assertRaises(InvalidPhoneError):
            self.repo.update_record_with_id("people", 1, phone_number="не_телефон")

    def test_delete_record(self):
        self.repo.insert_record("people", VALID_RECORD)
        self.assertTrue(self.repo.delete_record("people", 1))
        self.assertEqual(len(self.repo.select_records("people")), 0)

    def test_delete_record_not_found(self):
        self.assertFalse(self.repo.delete_record("people", 999))

    def test_clear_all_table(self):
        self.repo.insert_record("people", VALID_RECORD)
        self.repo.insert_record("people", {
            **VALID_RECORD, "id": 2, "phone_number": "+7 (999) 222-33-44"
        })
        self.repo.clear_all_table("people")
        self.assertEqual(len(self.repo.select_records("people")), 0)

    def test_persistence(self):
        self.repo.insert_record("people", VALID_RECORD)
        repo2 = self.db_class(self.test_dir)
        records = repo2.select_records("people")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["first_name"], "Иван")
        self.assertEqual(records[0]["age"], 20) 

class TestFileDatabaseJSON(BaseFileDatabaseTest, unittest.TestCase):
    db_class = FileDatabase_JSON
    test_dir = "test_data_json"

class TestFileDatabaseCSV(BaseFileDatabaseTest, unittest.TestCase):
    db_class = FileDatabase_CSV
    test_dir = "test_data_csv"

if __name__ == "__main__":
    unittest.main()
    