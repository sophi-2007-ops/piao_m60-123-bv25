class RepositoryError(Exception):
    pass


class InvalidAgeError(RepositoryError):
    pass


class InvalidPhoneError(RepositoryError):
    pass


class DuplicateIDError(RepositoryError):
    pass


class DatabaseError(Exception):
    pass


class TableAlreadyExistsError(DatabaseError):
    pass


class TableNotFoundError(DatabaseError):
    pass

class MissingColumnError(DatabaseError):
    pass


class UnknownColumnError(DatabaseError):
    pass


class InvalidStorageDataError(DatabaseError):
    pass
