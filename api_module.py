
import abc
import inspect

# Setting this to True will cause all henceforth constructed ApiModules to use mock calls.
use_mocks = False


class ApiModule(abc.ABC):

    def __init__(self):
        """Maybe overridees call() with mocked_call(), checking signatures match."""
        mocked_call_sig = dict(inspect.signature(self.mocked_call).parameters)
        original_mocked_call_sig = dict(inspect.signature(ApiModule.mocked_call).parameters)
        del original_mocked_call_sig['self']

        if original_mocked_call_sig != mocked_call_sig:
            # We've overridden mocked_call()
            assert mocked_call_sig == inspect.signature(self.call).parameters

        if use_mocks:
            self.call = self.mocked_call

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        """Call to whatever expensive operations this ApiModule preforms."""
        pass

    def mocked_call(self, *args, **kwargs):
        """Optional mock implementation of call(), for use in testing.

        If defined, signature must match call().
        """
        pass
