cd text_normalization/grammar
antlr4 -Dlanguage=Python3 txtNorm.g4 -o ../generated_files
antlr4 -Dlanguage=Python3 Units.g4 -o ../generated_files
