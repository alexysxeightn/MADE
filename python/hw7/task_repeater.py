"""verbose_context, verbose and repeater decorators"""
from contextlib import ContextDecorator
from functools import wraps

class verbose_context(ContextDecorator):
    """Decorator for defining behavior before and after function calls"""
    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            with self:
                return function(*args, **kwargs)
        return wrapper

    def __enter__(self):
        print('class: before function call')
        return self

    def __exit__(self, *exc):
        print('class: after function call')
        return False


def verbose(function):
    """Decorator for defining behavior before and after function calls"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        print('before function call')
        outcome = function(*args, **kwargs)
        print('after function call')
        return outcome
    return wrapper


def repeater(count: int):
    """Decorator that calls the function count times"""
    def repeater_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for _ in range(count):
                function(*args, **kwargs)
        return wrapper
    return repeater_decorator
