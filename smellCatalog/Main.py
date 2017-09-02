from InputProcessor import InputProcessor
from HtmlGenerator import HtmlGenerator
import Validator

INPUT_FILE_PATH = "../data/smells.txt"
OUTPUT_PATH = "../smellCatalogHtml/"
SMELL_CATEGORY_FILE_PATH = "../data/smell-category.txt"
REF_FILE_PATH = "../data/references.txt"
TOOL_FILE_PATH = "../data/tools.txt"
SMELL_DEF_FILE_PATH = "../data/smell-definitions.txt"

input_processor = InputProcessor(INPUT_FILE_PATH)
tools_list = input_processor.get_tools_list(TOOL_FILE_PATH)
smell_list = input_processor.get_smell_list()
input_processor.populate_aka_obj(smell_list)
category_list = input_processor.get_category_list(SMELL_CATEGORY_FILE_PATH)
ref_list = input_processor.get_ref_list(REF_FILE_PATH)
smell_definition_list = input_processor.get_smell_definition_list(SMELL_DEF_FILE_PATH)

Validator.validateAll(tools_list, smell_list, category_list, ref_list, smell_definition_list)

sorted_smell_list = sorted(smell_list, key=lambda smell: smell.name)

html_generator = HtmlGenerator(OUTPUT_PATH, sorted_smell_list, category_list, tools_list, smell_definition_list)
html_generator.generate()
