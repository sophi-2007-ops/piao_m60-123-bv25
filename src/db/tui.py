from src.db.backend.memory import (
    create_record,
    select_record,
    update_record,
    delete_record,
    PersonData,
    clear_table,
)


def _print_menu() -> None:
    print("\n=== База данных клиентов ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Поиск по фильтру")
    print("4. Обновить по фильтру")
    print("5. Удалить запись")
    print("6. Очистить всю таблицу")
    print("0. Выход")


def _read_int(promt: str) -> int:
    while True:
        raw = input(promt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка! Пожалуйста, введите целое число")


def _add_person() -> None:
    
    print("\nДобавление записи")
    
    person_id = _read_int("id: ")
    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_int("age: ")
    sex = input("sex: ").strip()
    phone_number = input("phone_number: ").strip()
    
    new_data = (person_id, first_name, second_name, age, sex, phone_number)

    try:
        create_record(person_id, first_name, second_name, age, sex, phone_number)
        print(f"Запись {new_data} успешно добавлена в таблицу People")
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def _print_records(records: list[PersonData]) -> None:
    if not records:
        print("Пока ничего нет")
        return
    for record in records:
        print(record)


def _show_all_data() -> None:
    print("\nСписок записей:")
    _print_records(select_record())


def _read_optional_int(promt: str) -> int | None:
    while True:
        raw = input(promt).strip()

        if raw == "":
            return None

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым")


def _find_person_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    person_id = _read_optional_int("id: ")
    first_name = input("first_name: ").strip() or None
    second_name = input("second_name: ").strip() or None
    age = _read_optional_int("age: ")
    sex = input("sex: ").strip() or None
    phone_number = input("phone_number: ").strip() or None

    records = select_record(
        person_id=person_id,
        first_name=first_name,
        second_name=second_name,
        age=age,
        sex=sex,
        phone_number=phone_number,
    )
    _print_records(records)


def _update_record() -> None:
    print("\nОбновление записи")
    person_id_for_update = _read_int("Введите id записи для обновления ")
    exists = select_record(person_id=person_id_for_update)
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

    new_age = _read_optional_int("Новый возраст: ")
    if new_age is not None:
        updates["age"] = new_age

    new_sex = input("Изменить пол на: ").strip() or None
    if new_sex is not None:
        updates["sex"] = new_sex

    new_phone_number = input("Новый номер телефона: ").strip() or None
    if new_phone_number is not None:
        updates["phone_number"] = new_phone_number

    if updates:
        update_record(person_id_for_update, **updates)
        print("Запись обновлена")
    else:
        print("Изменений не внесено")


def _delete_record() -> None:
    print("\nУдаление записи")
    person_id_for_delete = _read_int("Введите id для удаления записи ")

    if delete_record(person_id_for_delete):
        print(f"Запись {person_id_for_delete} успешно удалена")
    else:
        print("Ошибка! Запись не найдена")


def _clear_all_data() -> None:
    print("\nУдалить всё")
    confirm = input("Вы точно хотите удалить все данные??? (да/нет): ").strip().lower()
    if confirm == "да":
        if clear_table("People"):
            print("Таблица полностью очищена")
        else:
            print("Ошибка! Таблица не найдена")
    else:
        print("Очистка отменена")


def run() -> None:
    while True:
        _print_menu()
        action = input("\nВыберите действие: ").strip()

        if action == "1":
            _add_person()

        elif action == "2":
            _show_all_data()

        elif action == "3":
            _find_person_by_filter()

        elif action == "4":
            _update_record()

        elif action == "5":
            _delete_record()

        elif action == "6":
            _clear_all_data()

        elif action == "0":
            print("Выход из программы...")
            break
        else:
            print("Неверный ввод. Попробуйте снова")
