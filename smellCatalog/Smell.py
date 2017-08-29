class Smell(object):
    def __init__(self):
        self.id = None
        self.name = ""
        self.description = ""
        self.aka = []
        self.aka_obj_list = []
        self.reference = ""
        self.category = ""
        self.category_obj = None
        self.ref_obj = None
        self.tool_list = [] #ids of tools that supports detection of this smell
        self.example = ""

    def __repr__(self):
        return repr((self.id, self.name, self.description, self.aka, self.aka_obj_list, self.reference, self.category,
                     self.category_obj, self.ref_obj, self.tool_list, self.example))