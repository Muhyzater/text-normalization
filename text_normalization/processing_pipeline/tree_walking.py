from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from text_normalization.generated_files.txtNormLexer import txtNormLexer
from text_normalization.generated_files.txtNormParser import txtNormParser
from text_normalization.listener import Listener

from . import BaseStep


class TreeWalking(BaseStep):
    """
    Processes the input using the ANTLR grammer files
    """

    def process(self, request: dict, config: dict):

        for sentence in request["sentences"]:

            data = sentence.text
            sentence.last_dot = len(data) - len(data.rstrip("."))

            # The grammar uses dots which causes conflicts,
            # we aren't splitting sentences anymore

            # if sentence.last_dot > 0:
            #    data = data[:-sentence.last_dot]

            lexer = txtNormLexer(InputStream(" " + data + " "))
            stream = CommonTokenStream(lexer)
            parser = txtNormParser(stream)
            tree = parser.text()
            listener = Listener()
            listener.advanced = request["advanced"]

            walker = ParseTreeWalker()
            walker.walk(listener, tree)

            sentence.text = " ".join(listener.output)
            sentence.numbers = listener.numbers

        return self.process_next(request, config)
