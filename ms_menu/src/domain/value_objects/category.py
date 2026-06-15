from enum import Enum

class Category(str, Enum):
    SALAD = 'salad'
    SOUP = 'soup'
    MAIN = 'main'
    DESSERT = 'dessert'
    DRINK = 'drink'
    SNACK = 'snack'