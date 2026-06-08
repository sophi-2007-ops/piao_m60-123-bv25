import unittest
from unittest.mock import patch
from src.db.backend.memory import MemoryDB
from src.db.tui import Interface


class TestTui(unittest.TestCase):

    def setUp(self):
        self.repo = MemoryDB()
        self.app = Interface(repository=self.repo)
        self.valid_phone = "+7 (999) 111-22-33"

    def test_read_int_invalid_input(self):
        with patch("builtins.input", side_effect=["abc", "1"]):
            with patch("builtins.print"):
                result = self.app._read_int("Введите число: ")
                self.assertEqual(result, 1)

    def test_add_person(self):
        inputs = ["1", "Иван", "Иванов", "20", "М", "+7 (999) 999-99-99"]
        with patch("builtins.input", side_effect=inputs):
            self.app._add_person()
        records = self.repo.select_record()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1], "Иван")

    def test_print_records(self):
        with patch("builtins.print") as mock_print:
            self.app._print_records([])
            mock_print.assert_any_call("Пока ничего нет")
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", self.valid_phone)
        records = self.repo.select_record()
        self.app._print_records(records)

    def test_find_person_by_filter(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", self.valid_phone)
        inputs = ["1", "", "", "", "", ""]
        with patch("builtins.input", side_effect=inputs):
            self.app._find_person_by_filter()

    def test_update_record_success(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", self.valid_phone)
        inputs = ["1", "Петр", "", "", "", ""]
        with patch("builtins.input", side_effect=inputs):
            self.app._update_record()
        records = self.repo.select_record()
        self.assertEqual(records[0][1], "Петр")

    def test_update_record_not_found(self):
        with patch("builtins.input", return_value="999"):
            self.app._update_record()

    def test_update_record_scenarios(self):
        with patch("builtins.input", return_value="999"):
            self.app._update_record()
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", self.valid_phone)
        new_data = ["1", "Петр", "Петров", "25", "М", self.valid_phone]
        with patch("builtins.input", side_effect=new_data):
            self.app._update_record()
        records = self.repo.select_record()
        self.assertEqual(records[0][1], "Петр")
        self.assertEqual(records[0][3], 25)

    def test_update_record_value_error(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", self.valid_phone)
        with patch.object(
            self.repo, "update_record", side_effect=ValueError("Ошибка базы")
        ):
            inputs = ["1", "Петр", "", "", "", ""]
            with patch("builtins.input", side_effect=inputs):
                with patch("builtins.print") as mock_print:
                    self.app._update_record()
                    mock_print.assert_any_call("Ошибка при обновлении: Ошибка базы")

    def test_delete_person(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", "+7 (999) 999-99-99")
        with patch("builtins.input", return_value="1"):
            self.app._delete_record()
        self.assertEqual(len(self.repo.select_record()), 0)

    def test_delete_record_not_found(self):
        with patch.object(self.repo, "delete_record", return_value=False):
            with patch("builtins.input", return_value="999"):
                with patch("builtins.print") as mock_print:
                    self.app._delete_record()
                    mock_print.assert_any_call("Ошибка! Запись не найдена")

    def test_clear_all_data_da(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", "+7 (999) 999-99-99")
        with patch("builtins.input", return_value="да"):
            self.app._clear_all_data()
        self.assertEqual(len(self.repo.select_record()), 0)

    def test_clear_all_data_net(self):
        self.repo.create_record(1, "Иван", "Иванов", 20, "М", self.valid_phone)
        with patch("builtins.input", return_value="нет"):
            self.app._clear_all_data()
        self.assertEqual(len(self.repo.select_record()), 1)

    def test_run_menu_exit(self):
        with patch("builtins.input", return_value="0"):
            pass

    def test_run_menu_invalid_action(self):
        with patch("builtins.input", side_effect=["9", "0"]):
            self.app.run()

    def test_run_menu_cycle(self):
        with patch("builtins.input", side_effect=["9", "0"]):
            try:
                self.app.run()
            except SystemExit:
                pass
            except Exception as e:
                self.fail(f"Метод run упал, ошибка:{e}")

    def test_run_menu_all_branches(self):
        with patch(
            "builtins.input", side_effect=["1", "2", "2", "3", "4", "5", "6", "0"]
        ):
            with patch.object(self.app, "_add_person"), patch.object(
                self.app, "_show_all_data"
            ), patch.object(self.app, "_find_person_by_filter"), patch.object(
                self.app, "_update_record"
            ), patch.object(
                self.app, "_delete_record"
            ), patch.object(
                self.app, "_clear_all_data"
            ):
                self.app.run()
