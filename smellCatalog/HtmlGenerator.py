import os
import datetime
import FixedText

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

    def get_child_categories(self, category):
        result = []
        for cat in self.category_list:
            if (cat.parent_obj == category):
                result.append(cat)
        return result

    def generate_category(self, category):
        path = os.path.join(self.out_path, category.id + ".html")
        self.writeFile(path, FixedText.TOP_TEXT)
        self.appendFile(path, FixedText.BODY_TOP_PART)
        self.appendFile(path, FixedText.BODY_INDEX)
        cat_list = sorted(self.category_list, key=lambda cat: cat.name)
        for cat in cat_list:
            if (cat.parent_obj == None):
                text = "<a href=\"" + cat.id + ".html\" class=\"w3-bar-item w3-button w3-hover-white\">" + cat.name + "</a>"
                self.appendFile(path, text)
        self.appendFile(path, FixedText.BODY_LOW_PART)
        self.appendFile(path, FixedText.BODY_MAIN_TOP)
        child_categories = self.get_child_categories(category)
        if (len(child_categories)>0):
            self.appendFile(path, "<h2>(Sub-)Categories</h2>")
            self.appendFile(path, "<ul>")
            for cat in child_categories:
                sub_text = "<li><a href=\"" + cat.id + ".html\"><h4>" + cat.name + "</h4></a></li>"
                self.appendFile(path, sub_text)
            self.appendFile(path, "</ul>")
        else:
            self.appendFile(path, "<h2>" + category.name + "</h2>")
            self.appendFile(path, "<ol>")
            for smell in self.smell_list:
                if (smell.category==category.id):
                    smell_text = "<li><a href=\"" + smell.id + ".html\">" + smell.name + "</a></li>"
                    self.appendFile(path, smell_text)
            self.appendFile(path, "</ol>")
        self.appendFile(path, "<hr>")
        self.appendFile(path, "<a href=\"index.html\"><h3>Home</h3></a>")
        self.appendFile(path, "</div>")
        self.appendFile(path, FixedText.ATTRIBUTION_TEXT)
        self.appendFile(path, FixedText.TRACKING_TEXT)
        self.appendFile(path, FixedText.SOCIAL_TEXT)
        self.appendFile(path, FixedText.HTML_END_TEXT)

    def generate_index(self):
        path = os.path.join(self.out_path, "index.html")
        self.writeFile(path, FixedText.TOP_TEXT)
        self.appendFile(path, FixedText.BODY_TOP_PART)
        self.appendFile(path, FixedText.BODY_INDEX)
        cat_list = sorted(self.category_list, key=lambda cat: cat.name)
        for cat in cat_list:
            if (cat.parent_obj == None):
                text = "<a href=\"" + cat.id + ".html\" class=\"w3-bar-item w3-button w3-hover-white\">" + cat.name + "</a>"
                self.appendFile(path, text)
        self.appendFile(path, FixedText.BODY_LOW_PART)
        self.appendFile(path, FixedText.BODY_MAIN_TOP)
        self.appendFile(path, FixedText.INTRO_TEXT)
        self.appendFile(path, "<ul>")
        for cat in cat_list:
            if (cat.parent_obj == None):
                if(self.total_sub_categories(cat) > 0 ):
                    text = "<li><h4><a href=\"" + cat.id + ".html\">" + cat.name + "</a></h4></li>"
                else:
                    count = self.get_smell_count_in_category(cat)
                    text = "<li><h4><a href=\"" + cat.id + ".html\">" + cat.name + " (" + str(count) + ")</a></h4></li>"
                self.appendFile(path, text)
                self.appendFile(path, "<ul>")
                for subCat in cat_list:
                    if self.is_sub_category(subCat, cat):
                        count = self.get_smell_count_in_category(subCat)
                        sub_text = "<li><h5><a href=\"" + subCat.id + ".html\">" + subCat.name + " (" + str(count) + ")</a></h5></li>"
                        self.appendFile(path, sub_text)
                self.appendFile(path, "</ul>")
        self.appendFile(path, "</ul>")
        total_text = "<p><b>Total documented smells: " + str(len(self.smell_list)) + "</b></p>"
        self.appendFile(path, total_text)
        self.appendFile(path, FixedText.HOW_TEXT)
        self.appendFile(path, FixedText.ADDITIONAL_TEXT)
        self.appendFile(path, FixedText.ACKOWLEDGEMENTS)
        today = datetime.datetime.today()
        self.appendFile(path, "<hr><p>Last updated: " + str(today.strftime("%B %d, %Y")) + "</p>")
        self.appendFile(path, "</div>")
        self.appendFile(path, FixedText.ATTRIBUTION_TEXT)
        self.appendFile(path, FixedText.TRACKING_TEXT)
        self.appendFile(path, FixedText.SOCIAL_TEXT)
        self.appendFile(path, FixedText.HTML_END_TEXT)

    def writeFile(self, fileName, text):
        file = os.path.abspath(fileName)
        with open(file, "w", errors='ignore') as f:
            f.write(text)

    def appendFile(self, fileName, text):
        file = os.path.abspath(fileName)
        with open(file, "a", errors='ignore') as f:
            f.write(text)

    def generate_html(self, smell):
        path = os.path.join(self.out_path, smell.id + ".html")
        self.writeFile(path, FixedText.TOP_TEXT)
        self.appendFile(path, FixedText.BODY_TOP_PART)
        self.appendFile(path, FixedText.BODY_INDEX)
        cat_list = sorted(self.category_list, key=lambda cat: cat.name)
        for cat in cat_list:
            if (cat.parent_obj == None):
                text = "<a href=\"" + cat.id + ".html\" class=\"w3-bar-item w3-button w3-hover-white\">" + cat.name + "</a>"
                self.appendFile(path, text)
        self.appendFile(path, FixedText.BODY_LOW_PART)
        self.appendFile(path, FixedText.BODY_MAIN_TOP)
        smell_name = "<h3>" + smell.name + "</h3>"
        self.appendFile(path, smell_name)
        smell_description = "<p>" + smell.description + "</p>"
        self.appendFile(path, smell_description)
        if(len(smell.aka_obj_list)>0):
            aka_text = "<p>Related smells: "
            for aka in smell.aka_obj_list:
                aka_text += "<a href=\"" + aka.id + ".html\">" + aka.name + "</a> "
            aka_text += "</p>"
            self.appendFile(path, aka_text)
        if smell.ref_obj != None:
            self.appendFile(path, "<h4>Reference</h4>")
            if smell.ref_obj.url == "":
                self.appendFile(path, "<p>" + smell.ref_obj.text + "</p>")
            else:
                self.appendFile(path, "<p><a href=\"" + smell.ref_obj.url + "\">" + smell.ref_obj.text + "</a></p>")
        self.appendFile(path, "<hr>")
        self.appendFile(path, "<a href=\"" + smell.category_obj.id + ".html\"><h4>" + smell.category_obj.name + "</h4></a>")
        self.appendFile(path, "<a href=\"index.html\"><h3>Home</h3></a>")
        self.appendFile(path, "</div>")
        self.appendFile(path, FixedText.ATTRIBUTION_TEXT)
        self.appendFile(path, FixedText.TRACKING_TEXT)
        self.appendFile(path, FixedText.SOCIAL_TEXT)
        self.appendFile(path, FixedText.HTML_END_TEXT)


    def get_smell_count_in_category(self, cat):
        count = 0
        for smell in self.smell_list:
            if smell.category_obj == cat:
                count += 1
        return count

    def is_sub_category(self, subCat, cat):
        if subCat.parent_obj == cat:
            return True
        return False

    def total_sub_categories(self, cat):
        count = 0
        for category in self.category_list:
            if category.parent_obj == cat:
                count += 1
        return count