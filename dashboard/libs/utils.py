import json
from django.apps import apps


class UserProfileHelper:

    def __init__(self):
        pass

    @staticmethod
    def get_split_user_address(full_address):
        """
        Splits a user address using the commas in the string
        :param full_address:
        :return: bool|mixed
        """
        print type(full_address)
        if type(full_address) == unicode:
            split_address = full_address.split(',')
            return split_address
        else:
            return False


class ErrorLogHelper:

    def __init__(self):
        self.name = "ErrorLog"

    @staticmethod
    def log_error(error_message, calling_function):
        try:
            error_log_model = apps.get_model(app_label='dashboard', model_name='ErrorLogModel')
            error_log = error_log_model()
            error_log.error_message = str(error_message)
            error_log.calling_function = str(calling_function) if calling_function is not None else None
            error_log.save()
        except Exception, e:
            print e

