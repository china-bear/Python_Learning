"""
https://github.com/rmotr-curriculum/advanced-python-programming-questions/issues/16
what does mean "exceptions must derive from BaseException"  无法捕获模拟异常，因为它不继承BaseException

When you use raise it must be given either a class that inherits from the Exception class, or an instance of one.
For example ValueError is a builtin exception class, you can raise a ValueError using either of these methods:
"""


class FormField(object):
    def __init__(self, title, help_text=None):
        self.title = title
        self.help_text = help_text

    def submit_answer(self, answer):
        self.answer = answer

    def get_answer(self):
        pass

    def is_valid(self):
        try:
            self.answer
        except NameError:
            # raise "WARNING! Raises NameError"
            # raise ValueError
            raise ValueError("I'm a fancy error message")
        except ValueError:
            # raise "WARNING! Raises ValueError"
            # raise ValueError
            raise ValueError("I'm a fancy error message")
        else:
            return True


class TextField(FormField):
    pass


class EmailField(FormField):
    pass


class URLField(FormField):
    pass


class MultipleChoiceField(FormField):
    def __init__(self, title, options, help_text=None):
        super().__init__(title, help_text)
        self.options = options

    # def is_valid(self):
    #    if self.answer is None:
    #       return False
    #    else :
    #        return True
