class Tool(object):
    def __init__(self):
        self.id = None
        self.name = ""
        self.description = ""
        self.url=""
        self.img=""
        #self.supported_smells = [] #all the smells that can be detected by the tool (list of smell ids)
        self.supported_langs = ""