class CustomException(Exception):
    def __init__(self, message):
        self.message = message


JsonAmountException = CustomException("More than one JSON file in a folder")
CategoryTypeException = CustomException("Category type in categories list is not string or tuple")
ItemMissingException= CustomException("Item searched by name does not exist")
