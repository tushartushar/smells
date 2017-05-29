from yattag import Doc
import os

TOP_TEXT = "<html><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">" +\
"<link rel=\"stylesheet\" href=\"https://www.w3schools.com/w3css/4/w3.css\">" +\
"<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=Poppins\">"\
"<style>body,h1,h2,h3,h4,h5 {font-family: \"Poppins\", sans-serif}" +\
"body {font-size: 16px;}" +\
    ".w3-half img {margin-bottom: -6px;margin-top: 16px;opacity: 0.8;cursor: pointer}" +\
    ".w3-half img:hover {opacity: 1}"+\
"</style>"+\
"<head><title>A Taxonomy of Software Smells</title></head>"

BODY_TOP_PART = "<body>" +\
    "<nav class=\"w3-sidebar w3-gray w3-collapse w3-top w3-large w3-padding\" style=\"z-index:3;width:300px;font-weight:bold;\" id=\"mySidebar\"><br>" +\
        "<div class=\"w3-container\">" +\
            "<h3 class=\"w3-padding-64\"><b>A Taxonomy of Software Smells</b></h3></div>" +\
        "<div class=\"w3-bar-block\">"

BODY_INDEX = "<a href=\"index.html\" class=\"w3-bar-item w3-button w3-hover-white\">Home</a>"

BODY_LOW_PART = "</div>" +\
        "<hr>" +\
        "<div class=\"w3-bar-block\"><a href=\"http://www.tusharma.in\" class=\"w3-bar-item w3-button w3-hover-white\">Tushar's Blog</a></div>" +\
        "<hr>" +\
        "<div class=\"w3-bar-block\"><a href=\"http://bit.ly/DesignSmells\"><img src=\"book_cover.png\" style=\"width:220px;\"></a></div>" +\
        "<hr>" +\
        "<div>Detect smells using Designite<a href=\"http://www.designite-tools.com\"><img src=\"designite.png\" style=\"width:220px;\"></a></div>" +\
    "<hr></nav>"

BODY_MAIN_TOP = "<div class=\"w3-main\" style=\"margin-left:340px;margin-right:40px\">"

ATTRIBUTION_TEXT = "<div class=\"w3-light-grey w3-container w3-padding-32\" style=\"margin-top:75px;padding-right:58px\">"+\
                   "<p class=\"w3-right\">All rights reserved (c) <a href=\"http://www.tusharma.in\">Tushar Sharma</a> 2017.</p></div>"
HTML_END_TEXT = "</body></html>"

TRACKING_TEXT = "<script>" +\
  "(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){" +\
  "(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o)," +\
  "m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)" +\
  "})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');" +\
  "ga('create', 'UA-56403135-3', 'auto');" +\
  "ga('send', 'pageview');"+\
"</script>"

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
        path = os.path.join(self.out_path, category.id + ".html")
        self.writeFile(path, TOP_TEXT)
        self.appendFile(path, BODY_TOP_PART)
        self.appendFile(path, BODY_INDEX)
        cat_list = sorted(self.category_list, key=lambda cat: cat.name)
        for cat in cat_list:
            if (cat.parent_obj == None):
                text = "<a href=\"" + cat.id + ".html\" class=\"w3-bar-item w3-button w3-hover-white\">" + cat.name + "</a>"
                self.appendFile(path, text)
        self.appendFile(path, BODY_LOW_PART)
        self.appendFile(path, BODY_MAIN_TOP)
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
        self.appendFile(path, ATTRIBUTION_TEXT)
        self.appendFile(path, TRACKING_TEXT)
        self.appendFile(path, HTML_END_TEXT)

    def generate_index(self):
        path = os.path.join(self.out_path, "index.html")
        self.writeFile(path, TOP_TEXT)
        self.appendFile(path, BODY_TOP_PART)
        self.appendFile(path, BODY_INDEX)
        cat_list = sorted(self.category_list, key=lambda cat: cat.name)
        for cat in cat_list:
            if (cat.parent_obj == None):
                text = "<a href=\"" + cat.id + ".html\" class=\"w3-bar-item w3-button w3-hover-white\">" + cat.name + "</a>"
                self.appendFile(path, text)
        self.appendFile(path, BODY_LOW_PART)
        self.appendFile(path, BODY_MAIN_TOP)
        main_text = "<h1>A Taxonomy of Software Smells</h1>" +\
            "<img src=\"smells.png\" style=\"width:700px;\">" +\
        "<p>Kent Beck coined the term \"code smell\" in the popular <a href=\"http://amzn.to/2rblDm3\" target=\"_blank\"> " +\
                    "Refactoring book by Martin Fowler</a> and defined it informally as certain structures in the code " +\
                    "that suggest (sometimes they scream for) the possibility of refactoring. " +\
                    "Since then, various smells have been reported that impair software quality in one or more ways. " +\
                    "I attempt to prepare and present a taxonomy of software smells by cataloging, classifying, and " +\
                    "inter-relating smell definitions present in existing literature with their references.</p>"
        self.appendFile(path, main_text)
        self.appendFile(path, "<ul>")
        for cat in cat_list:
            if (cat.parent_obj == None):
                count = self.get_smell_count_in_category(cat)
                text = "<li><h4><a href=\"" + cat.id + ".html\">" + cat.name + " (" + str(count) + ")</a></h4></li>"
                self.appendFile(path, text)
        self.appendFile(path, "</ul>")
        total_text = "<p><b>Total documented smells: " + str(len(self.smell_list)) + "</b></p>"
        self.appendFile(path, total_text)
        additional_text = "<p>This taxonomy is evolving. I plan to add many more smells (for instance, lexicon smells, "+\
                          "performance smells, and energy smells). If you would like to point me to a (missing) smell "+\
                          "or reference, or would like to suggest something, feel free to email to me at tusharsharma@ieee.org.</p>"
        self.appendFile(path, additional_text)
        self.appendFile(path, "</div>")
        self.appendFile(path, ATTRIBUTION_TEXT)
        self.appendFile(path, TRACKING_TEXT)
        self.appendFile(path, HTML_END_TEXT)

    def writeFile(self, fileName, text):
        with open(fileName, "w", errors='ignore') as f:
            f.write(text)

    def appendFile(self, fileName, text):
        with open(fileName, "a", errors='ignore') as f:
            f.write(text)

    def generate_html(self, smell):
        path = os.path.join(self.out_path, smell.id + ".html")
        self.writeFile(path, TOP_TEXT)
        self.appendFile(path, BODY_TOP_PART)
        self.appendFile(path, BODY_INDEX)
        cat_list = sorted(self.category_list, key=lambda cat: cat.name)
        for cat in cat_list:
            if (cat.parent_obj == None):
                text = "<a href=\"" + cat.id + ".html\" class=\"w3-bar-item w3-button w3-hover-white\">" + cat.name + "</a>"
                self.appendFile(path, text)
        self.appendFile(path, BODY_LOW_PART)
        self.appendFile(path, BODY_MAIN_TOP)
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
        self.appendFile(path, ATTRIBUTION_TEXT)
        self.appendFile(path, TRACKING_TEXT)
        self.appendFile(path, HTML_END_TEXT)


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