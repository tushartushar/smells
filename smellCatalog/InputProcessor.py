import re
from Smell import Smell
from SmellCategory import SmellCategory
from Reference import Reference

SMELL = "\[smell\]"
SMELL_ID = "\[smell-id\]"
SMELL_NAME = "\[smell-name\]"
SMELL_END = "\[smell-end\]"
SMELL_DES = "\[smell-description\]"
SMELL_AKA = "\[smell-aka\]"
SMELL_CATEGORY = "\[smell-category\]"
SMELL_SUBCATEGORY = "\[smell-subcategory\]"
SMELL_REF = "\[smell-ref\]"

SCAT = "\[define-smell-category\]"
SCAT_ID = "\[smell-category-id\]"
SCAT_NAME = "\[smell-category-name\]"
SCAT_PARENT = "\[smell-category-parent\]"
SCAT_END = "\[define-smell-category-end\]"

REF = "\[reference\]"
REF_ID = "\[ref-id\]"
REF_TEXT = "\[ref-text\]"
REF_IMAGE = "\[ref-image\]"
REF_URL = "\[ref-url\]"
REF_END = "\[ref-end\]"


class InputProcessor(object):
    def __init__(self, path):
        self.input_file_path = path
        self.smell_list = []

    def process(self):
        cur_smell_obj = None
        with open(self.input_file_path, "r", errors='ignore') as reader:
            for line in reader:
                line = line.strip()
                if (line == ""):
                    continue
                smell_pattern = re.compile(SMELL)
                id_pattern = re.compile(SMELL_ID)
                name_pattern = re.compile(SMELL_NAME)
                des_pattern = re.compile(SMELL_DES)
                aka_pattern = re.compile(SMELL_AKA)
                end_pattern = re.compile(SMELL_END)
                cat_pattern = re.compile(SMELL_CATEGORY)
                sub_pattern = re.compile(SMELL_SUBCATEGORY)
                ref_pattern = re.compile(SMELL_REF)

                if(re.search(smell_pattern, line) != None):
                    cur_smell_obj = Smell()
                elif (re.search(end_pattern, line)):
                    self.smell_list.append(cur_smell_obj)
                elif (re.search(id_pattern, line) != None):
                    cur_smell_obj.id = re.split(SMELL_ID, line)[1].strip()
                elif (re.search(name_pattern, line) != None):
                    cur_smell_obj.name = re.split(SMELL_NAME, line)[1].strip()
                elif (re.search(des_pattern, line) != None):
                    cur_smell_obj.description = re.split(SMELL_DES, line)[1].strip()
                elif (re.search(aka_pattern, line) != None):
                    cur_smell_obj.aka.append(re.split(SMELL_AKA, line)[1].strip())
                elif (re.search(cat_pattern, line) != None):
                    cur_smell_obj.category = re.split(SMELL_CATEGORY, line)[1].strip()
                elif (re.search(sub_pattern, line) != None):
                    cur_smell_obj.sub_category = re.split(SMELL_SUBCATEGORY, line)[1].strip()
                elif (re.search(ref_pattern, line) != None):
                    cur_smell_obj.reference = re.split(SMELL_REF, line)[1].strip()

        return self.smell_list

    def find_parent(self, parent_id, category_list):
        for cat in category_list:
            if (cat.id == parent_id):
                return cat
        return None

    def link_categories(self, category_list):
        for cat in category_list:
            cat.parent_obj = self.find_parent(cat.parent, category_list)

    def get_category_list(self, SMELL_CATEGORY_FILE_PATH):
        category_list = []
        cur_category_obj = None
        with open(SMELL_CATEGORY_FILE_PATH, "r", errors='ignore') as reader:
            for line in reader:
                line = line.strip()
                if (line == ""):
                    continue
                scat_pattern = re.compile(SCAT)
                scat_id_pattern = re.compile(SCAT_ID)
                scat_name_pattern = re.compile(SCAT_NAME)
                scat_parent_pattern = re.compile(SCAT_PARENT)
                scat_end_pattern = re.compile(SCAT_END)
                if(re.search(scat_pattern, line) != None):
                    cur_category_obj = SmellCategory()
                elif (re.search(scat_end_pattern, line)):
                    category_list.append(cur_category_obj)
                elif (re.search(scat_id_pattern, line) != None):
                    cur_category_obj.id = re.split(SCAT_ID, line)[1].strip()
                elif (re.search(scat_name_pattern, line) != None):
                    cur_category_obj.name = re.split(SCAT_NAME, line)[1].strip()
                elif (re.search(scat_parent_pattern, line) != None):
                    cur_category_obj.parent = re.split(SCAT_PARENT, line)[1].strip()

        self.link_categories(category_list)
        return category_list

    def get_ref_list(self, REF_FILE_PATH):
        cur_ref_obj = None
        ref_list = []
        with open(REF_FILE_PATH, "r", errors='ignore') as reader:
            for line in reader:
                line = line.strip()
                if (line == ""):
                    continue
                ref_pattern = re.compile(REF)
                ref_id_pattern = re.compile(REF_ID)
                ref_text_pattern = re.compile(REF_TEXT)
                ref_image_pattern = re.compile(REF_IMAGE)
                ref_url_pattern = re.compile(REF_URL)
                ref_end_pattern = re.compile(REF_END)
                if(re.search(ref_pattern, line) != None):
                    cur_ref_obj = Reference()
                elif (re.search(ref_end_pattern, line) != None):
                    ref_list.append(cur_ref_obj)
                elif (re.search(ref_id_pattern, line) != None):
                    cur_ref_obj.id = re.split(REF_ID, line)[1].strip()
                elif (re.search(ref_text_pattern, line) != None):
                    cur_ref_obj.text = re.split(REF_TEXT, line)[1].strip()
                elif (re.search(ref_url_pattern, line) != None):
                    cur_ref_obj.url = re.split(REF_URL, line)[1].strip()
                elif (re.search(ref_image_pattern, line) != None):
                    cur_ref_obj.image = re.split(REF_IMAGE, line)[1].strip()
        return ref_list

    def populate_aka_obj(self, smell_list):
        for smell in smell_list:
            for aka in smell.aka:
                if (aka != ''): # NErnst prevents empty AKA matches
                    smell_obj = self.find_smell_obj(aka, smell_list)
                    if smell_obj == None:
                        print("Related smell not found: " + aka)
                    else:
                        smell.aka_obj_list.append(smell_obj)

    def find_smell_obj(self, aka, smell_list):
        for smell in smell_list:
            if (smell.id == aka):
                return smell
        return None

