class DomainException(Exception):
    pass

class InvalidTitle(DomainException):
    pass

class InvalidPrice(DomainException):
    pass

class InvalidDescription(DomainException):
    pass

class InvalidComposition(DomainException):
    pass

class InvalidCalories(DomainException):
    pass

class InvalidSuperPosition(DomainException):
    pass

class PositionNotFound(DomainException):
    pass

class PositionUnavailable(DomainException):
    pass

class CurrencyMismatch(DomainException):
    pass