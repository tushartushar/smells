from InputProcessor import InputProcessor
from HtmlGenerator import HtmlGenerator
import Validator

INPUT_FULE_PATH = "/Users/Tushar/Documents/Research/smells/smells.txt"
OUTPUT_PATH = "/Users/Tushar/Documents/Research/smells/smellCatalogHtml/"
SMELL_CATEGORY_FILE_PATH = "/Users/Tushar/Documents/Research/smells/smell-category.txt"
REF_FILE_PATH = "/Users/Tushar/Documents/Research/smells/references.txt"

def print_smell_list(smell_list):
    for smell in smell_list:
        print("id:" + smell.id)
        print("name:" + smell.name)
        print("desription:" + smell.description)
        print(("aka:" + smell.aka))
        print("category:" + smell.category)

input_processor = InputProcessor(INPUT_FULE_PATH)
smell_list = input_processor.process()
#print_smell_list(smell_list)
Validator.validate_id(smell_list)
input_processor.populate_aka_obj(smell_list)

category_list = input_processor.get_category_list(SMELL_CATEGORY_FILE_PATH)
Validator.validate_category(category_list, smell_list)

ref_list = input_processor.get_ref_list(REF_FILE_PATH)
Validator.validate_references(ref_list, smell_list)

sorted_smell_list = sorted(smell_list, key=lambda smell: smell.name)

html_generator = HtmlGenerator(OUTPUT_PATH, sorted_smell_list, category_list)
html_generator.generate()
