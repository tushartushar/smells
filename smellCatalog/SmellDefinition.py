class SmellDefinition(object):
    def __init__(self):
        self.id = None
        self.definition = ""
        self.ref = ""
        self.ref_obj = None

    def __repr__(self):
        return repr((self.id, self.definition, self.ref,
                    self.ref_obj))