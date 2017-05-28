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