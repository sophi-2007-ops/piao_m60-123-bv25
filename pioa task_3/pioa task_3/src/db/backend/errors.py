class RepositoryError(Exception):
    pass


class InvalidAgeError(RepositoryError):
    pass


class InvalidPhoneError(RepositoryError):
    pass


class DublicateIDError(RepositoryError):
    pass