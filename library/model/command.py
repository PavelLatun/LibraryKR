from model.actions import Actions


class Command:
    def __init__(self, action: Actions, description: str):
        self.__action = action
        self.__description = description

    def __str__(self):
        return f'Введите \'{self.__action.value}\' - для {self.__description}'
        # return f'{self.__description} - {self.__action}'

    def to_string(self):
        return f'Введите \'{self.__action.value}\' - для {self.__description}'

    @property
    def action(self):
        return self.__action
