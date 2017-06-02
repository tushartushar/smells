from InputProcessor import InputProcessor
from HtmlGenerator import HtmlGenerator
import Validator

INPUT_FULE_PATH = "../data/smells.txt"
OUTPUT_PATH = "../smellCatalogHtml/"
SMELL_CATEGORY_FILE_PATH = "../data/smell-category.txt"
REF_FILE_PATH = "../data/references.txt"

input_processor = InputProcessor(INPUT_FULE_PATH)
smell_list = input_processor.process()

Validator.validate_id(smell_list)
input_processor.populate_aka_obj(smell_list)

category_list = input_processor.get_category_list(SMELL_CATEGORY_FILE_PATH)
Validator.validate_category(category_list, smell_list)

ref_list = input_processor.get_ref_list(REF_FILE_PATH)
Validator.validate_references(ref_list, smell_list)

sorted_smell_list = sorted(smell_list, key=lambda smell: smell.name)

html_generator = HtmlGenerator(OUTPUT_PATH, sorted_smell_list, category_list)
html_generator.generate()
