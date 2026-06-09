from enum import Enum


class Permission(str, Enum):
    CREATE_ORDER = "Create_order"
    VIEW_ORDER = "View_order"
    MANAGE_EMPLOYMENT = "Manage_employment"
