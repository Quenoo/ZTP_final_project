from rest_framework.exceptions import APIException


class NoModelWithAtrubute(APIException):
    def __init__(self, model, atribute, value):
        self.status_code = 404
        self.detail = f'{model} with {atribute} = {value} does not exist'


class NoFieldInBody(APIException):
    def __init__(self, missing):
        self.status_code = 400
        self.detail = f'{missing} is missing from body'
