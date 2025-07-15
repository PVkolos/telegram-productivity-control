
class EmailError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'EmailError, {0} '.format(self.message)
        else:
            return 'Error to write E-mail. Check it.'


class Error(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Error, {0} '.format(self.message)
        else:
            return 'Error to write sms. Check it.'
