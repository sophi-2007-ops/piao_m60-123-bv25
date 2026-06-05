import re
from typing import Optional

PersonData = tuple[int, str, str, int, str, str]

People: list[PersonData] = []

phone_mask = r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$"


def create_record(
    person_id: int,
    first_name: str,
    second_name: str,
    age: int,
    sex: str,
    phone_number: str,
) -> PersonData:
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")

    phone_number = phone_number.strip()

    if not re.match(phone_mask, phone_number):
        raise ValueError("Некорректный номер. Номер должен должен быть в формате с +7 (xxx) xxx-xx-xx")

    if any(record[0] == person_id for record in People):
        raise ValueError(f"Запись с id={person_id} уже существует")

    new_record: PersonData = (
        person_id,
        first_name.strip(),
        second_name.strip(),
        age,
        sex.strip(),
        phone_number.strip()
    )

    People.append(new_record)

    return new_record


def select_record(
    person_id: Optional[int] = None,
    first_name: Optional[str] = None,
    second_name: Optional[str] = None,
    age: Optional[int] = None,
    sex: Optional[str] = None,
    phone_number: Optional[str] = None,
) -> list[PersonData]:
    if (person_id is None and 
        first_name is None and 
        second_name is None and 
        age is None and 
        sex is None and 
        phone_number is None):
        return People.copy()
    result: list[PersonData] = []

    for record in People:
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


def update_record(person_id: int = None, **kwargs) -> bool:
    global People
    for i, record in enumerate(People):
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

            People = tuple(record_list)
            return True
    return False


def delete_record(person_id: int = None) -> bool:
    global People
    i_len = len(People)
    People = [r for r in People if r[0] != person_id]
    return len(People) < i_len


def clear_table() -> bool:
    People.clear()
    return True
