import re
from typing import Optional
from src.db.backend.errors import InvalidAgeError, InvalidPhoneError, DublicateIDError

PersonData = tuple[int, str, str, int, str, str]


class MemoryDB:
    def __init__(self) -> None:
        self.people: list[PersonData] = []
        self.phone_mask = r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$"

    def create_record(
        self,
        person_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
        phone_number: str,
    ) -> PersonData:
        if age < 0:
            raise InvalidAgeError("Возраст не может быть отрицательным")

        phone_number = phone_number.strip()

        if not re.match(self.phone_mask, phone_number):
            raise InvalidPhoneError(
                "Некорректный номер. Номер должен должен быть в формате с +7 (xxx) xxx-xx-xx"
            )

        if any(record[0] == person_id for record in self.people):
            raise DublicateIDError(f"Запись с id={person_id} уже существует")

        new_record: PersonData = (
            person_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
            phone_number.strip(),
        )

        self.people.append(new_record)
        return new_record

    def select_record(
        self,
        person_id: Optional[int] = None,
        first_name: Optional[str] = None,
        second_name: Optional[str] = None,
        age: Optional[int] = None,
        sex: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> list[PersonData]:
        if (
            person_id is None
            and first_name is None
            and second_name is None
            and age is None
            and sex is None
            and phone_number is None
        ):
            return self.people.copy()
        result: list[PersonData] = []

        for record in self.people:
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

    def update_record(self, person_id: int, **kwargs) -> bool:
        if "age" in kwargs:
            age_val = int(kwargs["age"])
            if age_val < 0:
                raise InvalidAgeError("Возраст не может быть отрицательным.")

        if "phone_number" in kwargs:
            val_str = str(kwargs["phone_number"]).strip()
            if not re.match(self.phone_mask, val_str):
                raise InvalidPhoneError(
                    "Некорректный номер. Формат: +7 (xxx) xxx-xx-xx"
                )

        mapping = {
            "first_name": 1,
            "second_name": 2,
            "age": 3,
            "sex": 4,
            "phone_number": 5,
        }

        for i, record in enumerate(self.people):
            if record[0] == person_id:
                record_list = list(record)

                for key, value in kwargs.items():
                    if key in mapping:
                        if key == "age":
                            value = int(value)
                        record_list[mapping[key]] = value
                self.people[i] = tuple(record_list)
                return True
        return False

    def delete_record(self, person_id: int = None) -> bool:
        i_len = len(self.people)
        self.people = [r for r in self.people if r[0] != person_id]
        return len(self.people) < i_len

    def clear_table(self) -> bool:
        self.people.clear()
        return True
