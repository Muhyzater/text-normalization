from . import BaseStep, Sentence


class SplitText(BaseStep):
    """
    Splits the original text into sentences
    """

    def process(self, request: dict, config: dict):
        request["sentences"] = [Sentence(request["text"])]

        return self.process_next(request, config)
