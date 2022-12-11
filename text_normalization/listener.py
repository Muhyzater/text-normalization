import text_normalization.handlers as handlers
from text_normalization.constants import punctuation
from text_normalization.generated_files.txtNormListener import txtNormListener


class Listener(txtNormListener):
    advanced = True

    def __init__(self):
        self.output = []
        self.numbers = []

    def exitDate(self, ctx):
        self.output.append(
            handlers.DateHandler.handle(ctx, self.output, in_listener=True)
        )

    def exitTime(self, ctx):
        self.output.append(handlers.TimeHandler.handle(ctx, in_listener=True))

    def exitWord(self, ctx):
        out = ctx.getText().strip()
        # restore punctuation placement as they are split by the grammar
        # into words
        if out[0] in punctuation:
            if self.output:
                last_token = self.output[-1]
                last_char = last_token[-1]
                if last_char.isdigit():
                    self.output.append(out)
                else:
                    self.output[-1] += out
            else:
                self.output.append(out)
        else:
            self.output.append(out)

    def exitCurrency(self, ctx):
        self.output.append(handlers.CurrencyHandler.handle(ctx, in_listener=True))

    def exitMeasurement(self, ctx):
        self.output.append(
            handlers.MeasuremenHandler.handle(ctx, self.output, in_listener=True)
        )

    def exitIban(self, ctx):
        self.output.append(handlers.IbanHandler.handle(ctx, in_listener=True))

    def exitAccount(self, ctx):
        self.output.append(handlers.AccountNumberHandler.handle(ctx))

    def exitSequence_of_digits(self, ctx):
        self.output.append(handlers.SequenceOfDigitsHandler.handle(ctx))

    def exitEmail(self, ctx):
        self.output.append(ctx.getText())

    def exitNumber(self, ctx):

        number, output = handlers.NumberHandler.handle(ctx, self.output, self.advanced)
        self.numbers.append(number)
        self.output.append(output)

    def exitFloating_num(self, ctx):
        self.output.append(handlers.FloatingPointHandler.handle(ctx))

    def exitPhone(self, ctx):
        self.output.append(handlers.PhoneHandler.handle(ctx, in_listener=True))

    def exitAr_acronym(self, ctx):
        self.output.append(handlers.ArabicAcronymHandler.handle(ctx))

    def exitEn_acronym(self, ctx):
        self.output.append(handlers.EnglishAcronymHandler.handle(ctx))

    def exitSymbol(self, ctx):
        self.output.append(handlers.SymbolHandler.handle(ctx))

    def __del__(self):
        self.numbers = []
        self.output = []
