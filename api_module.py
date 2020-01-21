
import inspect
import functools

# Setting this to True will cause all henceforth constructed ApiModules to use mock calls.
use_mocks = False

_MOCK_PREFIX = 'mocked_'


def register(func):
    """Decorator for a call to an expensive operation.

    For a decorated methdod `f`, the class must also define a method `mocked_f`.
    """
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if use_mocks:
            mocked_func = self.__class__.__dict__[_MOCK_PREFIX + func.__name__]
            assert inspect.signature(mocked_func).parameters == inspect.signature(func).parameters

            return mocked_func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)

    return wrap
