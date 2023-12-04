import os

from src.tehtotktranslator.translator import GenericTranslator

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
test_filename = "Boss.txt"
input_file = f"{os.getcwd()}/{INPUT_FOLDER}/Boss.txt"
output_file = f"{os.getcwd()}/{OUTPUT_FOLDER}/Boss.txt"

t = GenericTranslator(input_file, output_file)

t.mass_translate()
