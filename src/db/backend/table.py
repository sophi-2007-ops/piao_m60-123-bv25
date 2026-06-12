from typing import Any
from .errors import MissingColumnError, UnknownColumnError, DuplicateIDError, InvalidPhoneError, InvalidAgeError
import re

phone_mask = r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$"

class Table:

    def __init__(
        self, 
        columns: tuple[str, ...], 
        records: list[dict[str, Any]] | None = None,
    ) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []

        if records is not None:
            for record in records:
                self.insert_record(record)
    
    def validate_fields(self, data: dict[str, Any]) -> None:
        if "age" in data:
            try:
                if int(data["age"]) < 0:
                    raise InvalidAgeError("Возраст не может быть отрицательным")
            except ValueError:
                raise InvalidAgeError("Возраст должен быть числом")
            
        if "phone_number" in data:
            if not re.match(phone_mask,str(data["phone_number"]).strip()):
                raise InvalidPhoneError("Некорректный номер. Формат: +7 (xxx) xxx-xx-xx")

    def insert_record(self, record: dict[str, Any]) -> None:
        missing_columns = [column for column in self.columns if column not in record]
        if missing_columns:
            raise MissingColumnError(
                f"Отсутствует поле '{missing_columns[0]}' в записи."
            )

        extra_columns = [column for column in record if column not in self.columns]
        if extra_columns:
            raise UnknownColumnError(
                f"Поле '{extra_columns[0]}' не определено в структуре таблицы."
            )
        record_id = record.get(self.columns[0])
        if any(r.get(self.columns[0]) == record_id for r in self.records):
            raise DuplicateIDError(f"Запись с id={record_id} уже существует")
        self.validate_fields(record)
        self.records.append(record.copy())

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:
        unknown_filters = [key for key in filters if key not in self.columns]
        if unknown_filters:
            raise UnknownColumnError(
                f"Поле '{unknown_filters[0]}' не определено в структуре таблицы."
            )

        if not filters:
            return [record.copy() for record in self.records]

        result: list[dict[str, Any]] = []
        for record in self.records:
            if all(record.get(key) == value for key, value in filters.items()):
                result.append(record.copy())

        return result
    
    def update_record_with_id(self, record_id, **kwargs) -> bool:
        unknown_fields = [key for key in kwargs if key not in self.columns]
        if unknown_fields:
            raise UnknownColumnError(
                f"Поле '{unknown_fields[0]}' не определено в структуре таблицы."
            )
        self.validate_fields(kwargs)
        if self.columns[0] in kwargs:
            new_id = kwargs[self.columns[0]] == record_id
            if any(r.get(self.columns[0]) == new_id for r in self.records):
                raise DuplicateIDError(f"Запись с id={new_id} уже существует")
            
        for i, record in enumerate(self.records):
            if record.get(self.columns[0]) == record_id:
                updated = record.copy()
                for key, value in kwargs.items():
                    updated[key] = value
                self.records[i] = updated
                return True
        return False
    
    def delete_record(self, record_id) -> bool:
        i_len = len(self.records)
        self.records = [
            r for r in self.records
            if r.get(self.columns[0]) != record_id
        ]
        return len(self.records) < i_len
    
    def clear_all_table(self) -> bool:
        self.records.clear()
        return True
    