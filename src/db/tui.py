from src.db.backend.memory import MemoryDB, PersonData
from src.db.backend.errors import InvalidAgeError, InvalidPhoneError, DublicateIDError


class Interface:
    def __init__(self, repository: MemoryDB) -> None:
        self.repository = repository

    def _print_menu(self) -> None:
        print("\n=== База данных клиентов ===")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Поиск по фильтру")
        print("4. Обновить по фильтру")
        print("5. Удалить запись")
        print("6. Очистить всю таблицу")
        print("0. Выход")

    def _read_int(self, promt: str) -> int:
        while True:
            raw = input(promt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка! Пожалуйста, введите целое число")

    def _add_person(self) -> None:

        print("\nДобавление записи")

        person_id = self._read_int("id: ")
        first_name = input("first_name: ").strip()
        second_name = input("second_name: ").strip()
        age = self._read_int("age: ")
        sex = input("sex: ").strip()
        phone_number = input("phone_number: ").strip()

        new_data = (person_id, first_name, second_name, age, sex, phone_number)

        try:
            self.repository.create_record(
                person_id, first_name, second_name, age, sex, phone_number
            )
            print(f"Запись {new_data} успешно добавлена в таблицу people")
        except (InvalidPhoneError, InvalidAgeError, DublicateIDError) as exc:
            print(f"Ошибка: {exc}")

    def _print_records(self, records: list[PersonData]) -> None:
        if not records:
            print("Пока ничего нет")
            return
        for record in records:
            print(record)

    def _show_all_data(self) -> None:
        print("\nСписок записей:")
        self._print_records(self.repository.select_record())

    def _read_optional_int(self, promt: str) -> int | None:
        while True:
            raw = input(promt).strip()

            if raw == "":
                return None

            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым")

    def _find_person_by_filter(self) -> None:
        print("\nПоиск по фильтру (Enter = пропустить поле)")

        person_id = self._read_optional_int("id: ")
        first_name = input("first_name: ").strip() or None
        second_name = input("second_name: ").strip() or None
        age = self._read_optional_int("age: ")
        sex = input("sex: ").strip() or None
        phone_number = input("phone_number: ").strip() or None

        records = self.repository.select_record(
            person_id=person_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex,
            phone_number=phone_number,
        )
        self._print_records(records)

    def _update_record(self) -> None:
        print("\nОбновление записи")
        person_id_for_update = self._read_int("Введите id записи для обновления ")
        exists = self.repository.select_record(person_id=person_id_for_update)
        if not exists:
            print("Ошибка! Запись с таким id не найдена")
            return
        print("Введите новые данные или оставьте поле пустым, чтобы не менять")
        updates = {}
        new_first_name = input("Новое имя: ").strip() or None
        if new_first_name is not None:
            updates["first_name"] = new_first_name

        new_second_name = input("Новая фамилия: ").strip() or None
        if new_second_name is not None:
            updates["second_name"] = new_second_name

        new_age = self._read_optional_int("Новый возраст: ")
        if new_age is not None:
            updates["age"] = new_age

        new_sex = input("Изменить пол на: ").strip() or None
        if new_sex is not None:
            updates["sex"] = new_sex

        new_phone_number = input("Новый номер телефона: ").strip() or None
        if new_phone_number is not None:
            updates["phone_number"] = new_phone_number

        if updates:
            try:
                self.repository.update_record(person_id_for_update, **updates)
                print("Запись обновлена")
            except ValueError as exc:
                print(f"Ошибка при обновлении: {exc}")
        else:
            print("Изменений не внесено")

    def _delete_record(self) -> None:
        print("\nУдаление записи")
        person_id_for_delete = self._read_int("Введите id для удаления записи ")

        if self.repository.delete_record(person_id_for_delete):
            print(f"Запись {person_id_for_delete} успешно удалена")
        else:
            print("Ошибка! Запись не найдена")

    def _clear_all_data(self) -> None:
        print("\nУдалить всё")
        confirm = (
            input("Вы точно хотите удалить все данные??? (да/нет): ").strip().lower()
        )
        if confirm == "да":
            if self.repository.clear_table():
                print("Таблица полностью очищена")
            else:
                print("Ошибка! Таблица не найдена")
        else:
            print("Очистка отменена")

    def run(self) -> None:
        while True:
            self._print_menu()
            action = input("\nВыберите действие: ").strip()

            if action == "1":
                self._add_person()

            elif action == "2":
                self._show_all_data()

            elif action == "3":
                self._find_person_by_filter()

            elif action == "4":
                self._update_record()

            elif action == "5":
                self._delete_record()

            elif action == "6":
                self._clear_all_data()

            elif action == "0":
                print("Выход из программы...")
                break
            else:
                print("Неверный ввод. Попробуйте снова")


if __name__ == "__main__":
    my_db = MemoryDB()
    app = Interface(repository=my_db)
    app.run()
