from enum import Enum

class EmployeeRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"
    CLIENT = "client"
