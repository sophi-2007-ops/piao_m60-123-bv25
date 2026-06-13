import unittest
from unittest.mock import patch
from src.db.tui import Interface


class TestTui(unittest.TestCase):

    def setUp(self):
        with patch("builtins.input", return_value="1"):
            self.app = Interface()
        self.valid_phone = "+7 (999) 111-22-33"

    def _add_record(self, person_id=1, first_name="Иван", second_name="Иванов",
                    age=20, sex="М", phone="+7 (999) 111-22-33"):
        self.app.database.insert_record("people", {
            "id": person_id, "first_name": first_name, "second_name": second_name,
            "age": age, "sex": sex, "phone_number": phone
        })

    def test_read_int_invalid_input(self):
        with patch("builtins.input", side_effect=["abc", "1"]):
            with patch("builtins.print"):
                result = self.app._read_int("Введите число: ")
                self.assertEqual(result, 1)

    def test_add_person(self):
        inputs = ["1", "Иван", "Иванов", "20", "М", "+7 (999) 999-99-99"]
        with patch("builtins.input", side_effect=inputs):
            self.app._add_person()
        records = self.app.database.select_records("people")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["first_name"], "Иван")

    def test_print_records_empty(self):
        with patch("builtins.print") as mock_print:
            self.app._print_records([])
            mock_print.assert_any_call("Пока ничего нет")

    def test_print_records(self):
        self._add_record()
        records = self.app.database.select_records("people")
        with patch("builtins.print") as mock_print:
            self.app._print_records(records)
            self.assertTrue(mock_print.called)

    def test_find_person_by_filter(self):
        self._add_record()
        inputs = ["1", "", "", "", "", ""]
        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print"):
                self.app._find_person_by_filter()

    def test_update_record_success(self):
        self._add_record()
        inputs = ["1", "Петр", "", "", "", ""]
        with patch("builtins.input", side_effect=inputs):
            self.app._update_record_with_id()
        records = self.app.database.select_records("people")
        self.assertEqual(records[0]["first_name"], "Петр")

    def test_update_record_not_found(self):
        with patch("builtins.input", return_value="999"):
            with patch("builtins.print") as mock_print:
                self.app._update_record_with_id()
                mock_print.assert_any_call("Ошибка! Запись с таким id не найдена")

    def test_update_record_validation(self):
        self._add_record()
        inputs = ["1", "", "", "-5", "", ""]
        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print") as mock_print:
                self.app._update_record_with_id()
                mock_print.assert_any_call("Ошибка при обновлении: Возраст не может быть отрицательным")
        record = self.app.database.select_records("people", id=1)[0]
        self.assertEqual(record["age"], 20)

    def test_delete_record(self):
        self._add_record()
        with patch("builtins.input", return_value="1"):
            self.app._delete_record()
        self.assertEqual(len(self.app.database.select_records("people")), 0)

    def test_delete_record_not_found(self):
        with patch("builtins.input", return_value="999"):
            with patch("builtins.print") as mock_print:
                self.app._delete_record()
                mock_print.assert_any_call("Ошибка! Запись не найдена")

    def test_clear_all_data_da(self):
        self._add_record()
        with patch("builtins.input", return_value="да"):
            self.app._clear_all_data()
        self.assertEqual(len(self.app.database.select_records("people")), 0)

    def test_clear_all_data_net(self):
        self._add_record()
        with patch("builtins.input", return_value="нет"):
            self.app._clear_all_data()
        self.assertEqual(len(self.app.database.select_records("people")), 1)

    def test_run_menu_invalid_action(self):
        with patch("builtins.input", side_effect=["9", "0"]):
            self.app.run()

    def test_run_menu_all_branches(self):
        with patch("builtins.input", side_effect=["1", "2", "3", "4", "5", "6", "0"]):
            with patch.object(self.app, "_add_person"), \
                 patch.object(self.app, "_show_all_data"), \
                 patch.object(self.app, "_find_person_by_filter"), \
                 patch.object(self.app, "_update_record_with_id"), \
                 patch.object(self.app, "_delete_record"), \
                 patch.object(self.app, "_clear_all_data"):
                self.app.run()
