from yattag import Doc
import os

class HtmlGenerator(object):
    def __init__(self, output_path, smell_list, category_list):
        self.smell_list = smell_list
        self.out_path = output_path
        self.category_list = category_list

    def generate(self):
        self.generate_index()
        self.generate_categories()
        for smell in self.smell_list:
            self.generate_html(smell)

    def generate_categories(self):
        for cat in self.category_list:
            self.generate_category(cat)

    def generate_category(self, category):
        doc, tag, text, line = Doc().ttl()
        with tag('html'):
            with tag('body'):
                with tag('h2'):
                    text(category.name)
                with tag('h3'):
                    text("(Sub)-categories")
                for cat in self.category_list:
                    if (cat.parent_obj == category):
                        with tag('ul'):
                            with tag('a', href=cat.id+".html"):
                                text(cat.name)
                with tag('h3'):
                    text("Smells")
                i = 1
                for smell in self.smell_list:
                    if (smell.category==category.id):
                        with tag('ul'):
                            with tag('a', href=smell.id+".html"):
                                text(str(i) + ". " + smell.name)
                                i += 1
        path = os.path.join(self.out_path, category.id+".html")
        self.writeFile(path, doc.getvalue())

    def generate_index(self):
        doc, tag, text, line = Doc().ttl()
        with tag('html'):
            with tag('body'):
                with tag('h1'):
                    text("A Catalog of Software Smells")
                with tag('p'):
                    text("Kent Beck coined the term \"code smell\" [Fowler1999] and defined it informally as certain "+
                         "structures in the code that suggest (sometimes they scream for) the possibility of refactoring. " +
                         "Since then, various smells have been reported that impair software quality in one or more ways. " +
                         "Therefore, in this attempt, we are presenting all the smell definition and related information " +
                         "in the form a catalog.")
                for cat in self.category_list:
                    if (cat.parent_obj == None):
                        with tag('ul'):
                            with tag('a', href=cat.id+".html"):
                                text(cat.name)
        path = os.path.join(self.out_path, "index.html")
        self.writeFile(path, doc.getvalue())

    def writeFile(self, fileName, text):
        with open(fileName, "w", errors='ignore') as f:
            f.write(text)

    def generate_html(self, smell):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('h3'):
                    text(smell.name)
                with tag('p'):
                    text(smell.description)
                with tag('p'):
                    text(smell.aka)

                with tag('h4'):
                    text("Reference")
                with tag('p'):
                    if (smell.ref_obj!=None):
                        if(smell.ref_obj.url == ""):
                            text(smell.ref_obj.text)
                        else:
                            with tag('a', href=smell.ref_obj.url):
                                text(smell.ref_obj.text)
                with tag('hr'):
                    pass
                with tag('h4'):
                    with tag('a', href=smell.category_obj.id+".html"):
                        text("Go to " + smell.category_obj.name)
                with tag('h4'):
                    with tag('a', href="index.html"):
                        text("Go to Home")

        path = os.path.join(self.out_path, smell.id + ".html")
        self.writeFile(path, doc.getvalue())