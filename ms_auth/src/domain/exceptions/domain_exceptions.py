class DomainException(Exception):
    pass

class InvalidPhoneNumber(DomainException):
    pass

class EmployeeNotFound(DomainException):
    pass

class EmployeeInactiveException(DomainException):
    pass

class OTPExpiredException(DomainException):
    pass

class OTPInvalidException(DomainException):
    pass

class OTPMaxAttemptsExceeded(DomainException):
    pass