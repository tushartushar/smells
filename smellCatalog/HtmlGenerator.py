from yattag import Doc
import os

class HtmlGenerator(object):
    #def __init__(self, output_path, smell_list, category_list, index_url, base_url):
    def __init__(self, output_path, smell_list, category_list):
        self.smell_list = smell_list
        self.out_path = output_path
        self.category_list = category_list
        #self.index_url = index_url
        #self.base_url = base_url

    def generate(self):
        self.generate_index()
        self.generate_categories()
        for smell in self.smell_list:
            self.generate_html(smell)

    def generate_categories(self):
        for cat in self.category_list:
            self.generate_category(cat)

    def get_child_categories(self, category):
        result = []
        for cat in self.category_list:
            if (cat.parent_obj == category):
                result.append(cat)
        return result

    def generate_category(self, category):
        doc, tag, text, line = Doc().ttl()
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text(category.name)
            with tag('body'):
                with tag('h2'):
                    text(category.name)
                child_categories = self.get_child_categories(category)
                if (len(child_categories)>0):
                    with tag('h3'):
                        text("(Sub)-categories")
                    for cat in child_categories:
                        with tag('ul'):
                            with tag('a', href=cat.id+".html"):
                            #with tag('a', href=self.getURL(cat.name)):
                                text(cat.name)
                else:
                    with tag('h3'):
                        text("Smells")
                    i = 1
                    with tag('ul'):
                        for smell in self.smell_list:
                            if (smell.category==category.id):
                                with tag('li'):
                                    with tag('a', href=smell.id+".html"):
                                    #with tag('a', href=self.getURL(smell.name)):
                                        text(str(i) + ". " + smell.name)
                                        i += 1
                with tag('hr'):
                    pass
                with tag('h4'):
                    #with tag('a', href=self.index_url):
                    with tag('a', href="index.html"):
                        text("Go to Home")
        path = os.path.join(self.out_path, category.id+".html")
        self.writeFile(path, doc.getvalue())

    def generate_index(self):
        doc, tag, text, line = Doc().ttl()
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text("A Taxonomy of Software Smells")
            with tag('body'):
                with tag('h1'):
                    text("A Taxonomy of Software Smells")
                with tag('p'):
                    text("Kent Beck coined the term \"code smell\" in the popular Refactoring book by Martin Fowler and defined it informally as certain "+
                         "structures in the code that suggest (sometimes they scream for) the possibility of refactoring. " +
                         "Since then, various smells have been reported that impair software quality in one or more ways. " +
                         "In this attempt, I present all the smell definitions present in existing literature with their references.")
                cat_list = sorted(self.category_list, key=lambda cat: cat.name)
                with tag('ul'):
                    for cat in cat_list:
                        if (cat.parent_obj == None):
                            with tag('li'):
                                with tag('h3'):
                                    with tag('a', href=cat.id+".html"):
                                    #with tag('a', href=self.getURL(cat.name)):
                                        count = self.get_smell_count_in_category(cat)
                                        text(cat.name + " (" + str(count) + ")")
                with tag('p'):
                    with tag('b'):
                        text ("Total documented smells: " + str(len(self.smell_list)))
        path = os.path.join(self.out_path, "index.html")
        self.writeFile(path, doc.getvalue())

    def writeFile(self, fileName, text):
        with open(fileName, "w", errors='ignore') as f:
            f.write(text)

    def generate_html(self, smell):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text(smell.name)
            with tag('body'):
                with tag('h3'):
                    text(smell.name)
                with tag('p'):
                    text(smell.description)
                with tag('p'):
                    text("Related smells: ")
                    for aka in smell.aka_obj_list:
                        with tag('a', href=aka.id + ".html"):
                        #with tag('a', href=self.getURL(aka.name)):
                            text(aka.name)
                        with tag('b'):
                            text (" ")
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
                    #with tag('a', href=self.getURL(smell.category_obj.name)):
                        text("Go to " + smell.category_obj.name)
                with tag('h4'):
                    #with tag('a', href=self.index_url):
                    with tag('a', href="index.html"):
                        text("Go to Home")

        path = os.path.join(self.out_path, smell.id + ".html")
        self.writeFile(path, doc.getvalue())

    def get_smell_count_in_category(self, cat):
        count = 0
        for smell in self.smell_list:
            if smell.category_obj == cat:
                count += 1
        return count

    #def getURL(self, name):
    #    temp = str.replace(str.lower(name)," ", "-")
    #    temp2 = str.replace(temp, "(", "")
    #    temp3 = str.replace(temp2, ")", "")
    #    return self.base_url + temp3 + "/"