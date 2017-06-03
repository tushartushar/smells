#Every smell must have a unique id
#because we use smell id to generate files specific to each smell and link with others
def validate_id(smell_list):
    list = set()
    for smell in smell_list:
        if (smell.id in list):
            print ("Every smell must have a unique id. Duplicate " + smell.id)
            exit(1)
        elif smell.id == "":
            print ("Empty smell id for " + smell.name)
            exit(3)
        else:
            list.add(smell.id)

def find_category_object(category, category_list):
    for cat in category_list:
        if(cat.id == category):
            return cat
    return None

#Each smell category must be unique, and
#Each smell must have a valid smell category assigned
def validate_category(category_list, smell_list):
    list = set()
    for cat in category_list:
        if(cat.id in list):
            print ("Every smell category must have a unique id. Duplicate " + cat.id)
            exit(1)
        else:
            list.add(cat.id)

    for smell in smell_list:
        obj = find_category_object(smell.category, category_list)
        if(obj!= None):
            smell.category_obj = obj
        else:
            print ("Invalid category specified for smell: " + smell.name)
            exit(2)

def find_ref_object(reference, ref_list):
    for ref in ref_list:
        if(ref.id == reference):
            return ref
    return None

#Each reference must be unique, and
#Each reference present in the smell list must be present in the ref list
def validate_references(ref_list, smell_list):
    list = set()
    for ref in ref_list:
        if(ref.id in list):
            print ("Every reference must have a unique id; duplicate: " + ref.id)
            exit(1)
        else:
            list.add(ref.id)

    for smell in smell_list:
        obj = find_ref_object(smell.reference, ref_list)
        if(obj!= None):
            smell.ref_obj = obj
        else:
            print ("Reference specified for smell is not present: " + smell.reference)
            exit(2)

#Every tool must have a unique id
def validate_tools_id(tools_list):
    list = set()
    for tool in tools_list:
        if (tool.id in list):
            print ("Every tool must have a unique id. Duplicate " + tool.id)
            exit(1)
        elif tool.id == "":
            print ("Empty tool id for " + tool.name)
            exit(3)
        else:
            list.add(tool.id)


def validate_tool_id_in_smells(tools_list, smell_list):
    tool_id_list = get_tool_id_list(tools_list)
    for smell in smell_list:
        for tool in smell.tool_list:
            if (tool not in tool_id_list):
                print ("Every specified tool id in a smell definition must be defined. Unknown tool id: " + tool.id)
                exit(4)

def get_tool_id_list(tools_list):
    list = set()
    for tool in tools_list:
        list.add(tool.id)
    return list

def get_smell_id_list(smell_list):
    list = set()
    for smell in smell_list:
        list.add(smell.id)
    return list

def validate_smell_id_in_smells(tools_list, smell_list):
    smell_id_list = get_smell_id_list(smell_list)
    for tool in tools_list:
        for smell in tool.supported_smells:
            if (smell.id not in smell_id_list):
                print ("Every specified smell id in a tool definition must be defined. Unknown smell id: " + smell.id)
                exit(4)


def validate_tool_info(tools_list):
    for tool in tools_list:
        if tool.name == "":
            print ("Error: Tool name missing for tool_id " + tool.id)
            exit(5)
        if tool.supported_langs == "":
            print ("Error: Tool doesn't support any language.")
            exit(5)
        if tool.url == "":
            print ("Error: Tool URL cannot be empty.")
            exit(5)


def validateAll(tools_list, smell_list, category_list, ref_list):
    validate_tools_id(tools_list)
    validate_tool_info(tools_list)
    validate_id(smell_list)
    validate_tool_id_in_smells(tools_list, smell_list)
    #validate_smell_id_in_smells(tools_list, smell_list)
    validate_category(category_list, smell_list)
    validate_references(ref_list, smell_list)