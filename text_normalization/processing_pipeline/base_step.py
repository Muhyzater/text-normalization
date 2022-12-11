from abc import ABC, abstractmethod

from . import Processed


class BaseStep(ABC):
    """
    Base step other steps must adhere to
    """

    _next_step = None

    @abstractmethod
    def process(self, request: dict, config: dict) -> Processed:
        """"""

        ...

    def set_next(self, step):
        """
        Chain next step in the chain
        args
        -------------
        step (BaseStep): the step to be added the end of the
        chain
        returns
        -------------
        step (BaseStep): the step at the end of the chain
        """

        self._next_step = step

        return step

    def process_next(self, request: dict, config: dict) -> Processed:
        """
        invoke next step if possible
        """

        if self._next_step:
            return self._next_step.process(request, config)
        else:
            # TODO: return correct response from last step
            return Processed(response=None, code=200, headers=None)
