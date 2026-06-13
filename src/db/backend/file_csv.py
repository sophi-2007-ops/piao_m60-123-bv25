import csv
from pathlib import Path
from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError, DuplicateIDError
from .table import Table


class FileDatabase_CSV(Database):

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        table_path = self._get_table_path(table_name)
        if not table_path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")

        try:
            with table_path.open("r", encoding="utf-8") as file:
                reader = csv.reader(file)
                columns = tuple(next(reader))  
                type_row = next(reader)        
                types = dict(zip(columns, type_row))

                records = []
                for row in reader:
                    record = {}
                    for col, val in zip(columns, row):
                        record[col] = self.cast_value(val, types[col])
                    records.append(record)

        except (csv.Error, StopIteration) as error:
            raise InvalidStorageDataError(
                "Файл таблицы содержит некорректный CSV."
            ) from error

        return self._deserialize_table(columns, records)

    def _save_table(self, table_name: str, table: Table) -> None:
        table_path = self._get_table_path(table_name)
        try: 
            with table_path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(table.columns)  
                types ={
                    "id": "int",
                    "first_name": "str",
                    "second_name": "str",
                    "age": "int",
                    "sex": "str",
                    "phone_number": "str"
                }
                writer.writerow([types.get(col, "str") for col in table.columns])
                for record in table.records:
                    writer.writerow([record[col] for col in table.columns])
        except OSError:
            raise InvalidStorageDataError(f"Ошибка записи файла таблицы '{table_name}'")

    def cast_value(self, value: str, type_name: str):
        casters = {
            "int": int,
            "float": float,
            "bool": lambda v: v.lower() == "true",
            "str": str,
        }
        caster = casters.get(type_name, str)
        try:
            return caster(value)
        except (ValueError, TypeError) as error:
            raise InvalidStorageDataError(
                f"Не удалось конвертировать '{value}' в тип '{type_name}'."
            ) from error

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.csv"

    def _deserialize_table(self, columns: tuple, records: list) -> Table:
        table = Table(columns)
        ids = set()
        for record in records:
            record_id = record.get(columns[0])
            if record_id in ids:
                raise DuplicateIDError(f"Файл содержит дубликат id={record_id}")
            ids.add(record_id)
            table.records.append(record.copy())
        return table
