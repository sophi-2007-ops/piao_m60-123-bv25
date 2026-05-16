PersonData = tuple[int, str, str, int, str, str]

Database: dict[str, list] = {"People": []}


def insert_into(table_name: str, data: tuple):
    if table_name not in Database:
        raise ValueError(f"Таблица {table_name} отсутствует")
    Database[table_name].append(data)


def create_record(
    person_id: int,
    first_name: str,
    second_name: str,
    age: int,
    sex: int,
    phone_number: str,
) -> PersonData:
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")

    if len(phone_number) != 12 and phone_number[:2] != "+7":
        raise ValueError("Некорректный номер. Номер должен начинаться с +7")

    if any(record[0] == person_id for record in Database["People"]):
        raise ValueError(f"Запись с id={person_id} уже существует")

    new_record: PersonData = (
        person_id,
        first_name.strip(),
        second_name.strip(),
        age,
        sex.strip(),
        phone_number.strip(),
    )

    Database["People"].append(new_record)

    return new_record


def select_record(
    table_name: str = "People",
    person_id: int | None = None,
    first_name: str | None = None,
    second_name: str | None = None,
    age: int | None = None,
    sex: int | None = None,
    phone_number: str | None = None,
) -> list[PersonData]:
    if (
        person_id is None
        and first_name is None
        and second_name is None
        and age is None
        and sex is None
        and phone_number is None
    ):
        return Database["People"].copy()
    result: list[PersonData] = []

    for record in Database["People"]:
        if person_id is not None and record[0] != person_id:
            continue
        if first_name is not None and record[1] != first_name:
            continue
        if second_name is not None and record[2] != second_name:
            continue
        if age is not None and record[3] != age:
            continue
        if sex is not None and record[4] != sex:
            continue
        if phone_number is not None and record[5] != phone_number:
            continue

        result.append(record)
    return result


def update_record(table_name: str = "People", person_id: int = None, **kwargs) -> bool:
    if table_name not in Database:
        return False
    for i, record in enumerate(Database[table_name]):
        if record[0] == person_id:
            record_list = list(record)

            mapping = {
                "first_name": 1,
                "second_name": 2,
                "age": 3,
                "sex": 4,
                "phone_number": 5,
            }

            for key, value in kwargs.items():
                if key in mapping:
                    record_list[mapping[key]] = value

            Database[table_name][i] = tuple(record_list)
            return True
    return False


def delete_record(table_name: str = "People", person_id: int = None) -> bool:
    if table_name not in Database:
        return False
    i_len = len(Database[table_name])
    Database[table_name] = [r for r in Database[table_name] if r[0] != person_id]
    return len(Database[table_name]) < i_len


def clear_table(table_name: str = "People") -> bool:
    if table_name not in Database:
        return False
    Database[table_name].clear()
    return True
