from abc import ABC

from text_normalization.generated_files.txtNormParser import ParserRuleContext

from . import HandlerValidationException, NotEmpty


class BaseHandler(ABC):
    """
    Base handler for all exit statues coming from teh listener
    """

    def handle(self, ctx, *args: tuple, **kwargs: dict) -> str:
        """apply logic on context data to reach the normlized equivalent

        Args:
            ctx (object): context data
            args (tuple): positional arguments to pass
            kwargs (dict): key-word arguments to pass

        Returns:
            str: normalization result
        """
        if isinstance(ctx, ParserRuleContext):
            ctx = self._get_ctx_data(ctx)

        if not kwargs.get("in_listener", False):
            self._validate(ctx)

        if "in_listener" in kwargs:
            del kwargs["in_listener"]

        if hasattr(self, "_process_ctx_data"):
            ctx = self._process_ctx_data(ctx)

        return self._handle(ctx, *args, **kwargs)

    def _handle(self, text: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def _get_ctx_data(ctx) -> str:
        """retrieves data needed from context

        Args:
            ctx (object): context data

        Returns:
            str: parsed data
        """
        return ctx.getText()

    @staticmethod
    def _format(data: str) -> str:
        return data

    @staticmethod
    def _restore_seprartor(formatted_text, separator):
        return formatted_text + separator

    @staticmethod
    def _validate(text: str) -> None:
        """validate handler input

        Args:
            text (str): input text
        """
        NotEmpty(text)
