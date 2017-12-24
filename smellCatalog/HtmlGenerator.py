import os
import datetime
import FixedText



class HtmlGenerator(object):
    def __init__(self, output_path, smell_list, category_list, tool_list, smell_definition_list):
        self.smell_list = smell_list
        self.out_path = output_path
        self.category_list = category_list
        self.tool_list = tool_list
        self.smell_definition_list = smell_definition_list

    def generate(self):
        self.generate_index()
        self.generate_categories_html()
        self.generate_tools_html()
        self.generate_smell_defs_html()
        for smell in self.smell_list:
            self.generate_smell_html(smell)

    def generate_categories_html(self):
        for cat in self.category_list:
            self.generate_category_html(cat)

    def get_child_categories(self, category):
        result = []
        for cat in self.category_list:
            if (cat.parent_obj == category):
                result.append(cat)
        return result

    def get_all_descendent_categories(self, category):
        result = set([category])
        for cat in self.category_list:
            if cat.parent_obj == category:
                result.add(cat)
                descendents = self.get_all_descendent_categories(cat)
                for a_descendent in descendents:
                    result.add(a_descendent)
        return result

    def write_html_top_stuff(self, path):
        self.writeFile(path, FixedText.TOP_TEXT)
        self.appendFile(path, FixedText.BODY_TOP_PART)
        self.appendFile(path, FixedText.BODY_INDEX)
        # cat_list = sorted(self.category_list, key=lambda cat: cat.name)
        # for cat in cat_list:
        #     if (cat.parent_obj == None):
        #         text = "<a href=\"" + cat.id + ".html\" class=\"w3-bar-item w3-button w3-hover-white\">" + cat.name + "</a>"
        #         self.appendFile(path, text)
        self.appendFile(path, FixedText.BODY_LOW_PART)
        self.appendFile(path, FixedText.BODY_MAIN_TOP)

    def write_html_bottom_stuff(self, path):
        self.appendFile(path, FixedText.ATTRIBUTION_TEXT)
        self.appendFile(path, FixedText.TRACKING_TEXT)
        self.appendFile(path, FixedText.SOCIAL_TEXT)
        self.appendFile(path, FixedText.HTML_END_TEXT)

    def generate_category_html(self, category):
        path = os.path.join(self.out_path, category.id + ".html")
        self.write_html_top_stuff(path)
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
        self.write_html_bottom_stuff(path)

    def generate_index(self):
        path = os.path.join(self.out_path, "index.html")
        self.write_html_top_stuff(path)
        cat_list = sorted(self.category_list, key=lambda cat: cat.name)
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
        self.write_html_bottom_stuff(path)

    def writeFile(self, fileName, text):
        file = os.path.abspath(fileName)
        with open(file, "w", errors='ignore', encoding='utf-8') as f:
            f.write(text)

    def appendFile(self, fileName, text):
        file = os.path.abspath(fileName)
        with open(file, "a", errors='ignore', encoding='utf-8') as f:
            f.write(text)

    def generate_smell_html(self, smell):
        path = os.path.join(self.out_path, smell.id + ".html")
        self.write_html_top_stuff(path)
        smell_name = "<h3>" + smell.name + "</h3>"
        self.appendFile(path, smell_name)
        descriptions = smell.description.split("\\n")
        smell_description = ""
        for des in descriptions:
            smell_description += "<p>" + des + "</p>"
        self.appendFile(path, smell_description)
        if len(smell.example) > 0:
            example_lines = smell.example.split("\\n")
            example_text = "<h4>Example</h4><p>"
            for ex in example_lines:
                example_text += ex + "<br />"
            self.appendFile(path, example_text)
        if(len(smell.aka_obj_list)>0):
            aka_text = "<p>Related smells: "
            for aka in smell.aka_obj_list:
                aka_text += "<a href=\"" + aka.id + ".html\">" + aka.name + "</a> "
            aka_text += "</p>"
            self.appendFile(path, aka_text)
        if (len(smell.tool_list)>0):
            tool_text = "<h4>Tools</h4><p>The following set of tools detects this smell: "
            for tool in smell.tool_list:
                tool_obj = self.get_tool_obj(tool)
                tool_text += "<a href=\"" + tool_obj.id + ".html\">" + tool_obj.name + "(for " + tool_obj.supported_langs + ")</a> "
            tool_text += "</p>"
            self.appendFile(path, tool_text)
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
        self.write_html_bottom_stuff(path)


    def get_smell_count_in_category(self, cat):
        count = 0

        cat_hierarchy_list = self.get_all_descendent_categories(cat)
        for aCat in cat_hierarchy_list:
            for smell in self.smell_list:
                if smell.category_obj == aCat:
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

    def get_tool_obj(self, tool):
        for obj in self.tool_list:
            if obj.id == tool:
                return obj
        return None

    def generate_tools_html(self):
        self.generate_tools_main_html()
        for tool in self.tool_list:
            self.generate_tool_html(tool)

    def generate_tools_main_html(self):
        path = os.path.join(self.out_path, "TOOLS.html")
        self.write_html_top_stuff(path)
        self.appendFile(path, "<h2>Tools</h2>")
        self.appendFile(path, "<ul>")
        for tool in self.tool_list:
            sub_text = "<li><a href=\"" + tool.id + ".html\"><h4>" + tool.name + "</h4></a></li>"
            self.appendFile(path, sub_text)
        self.appendFile(path, "</ul>")
        self.appendFile(path, "<hr>")
        self.appendFile(path, "<a href=\"index.html\"><h3>Home</h3></a>")
        self.appendFile(path, "</div>")
        self.write_html_bottom_stuff(path)

    def generate_tool_html(self, tool):
        path = os.path.join(self.out_path, tool.id + ".html")
        self.write_html_top_stuff(path)
        tool_name = "<h3>" + tool.name + "</h3>"
        self.appendFile(path, tool_name)
        smell_description = "<p>" + tool.description + "</p>"
        self.appendFile(path, smell_description)
        url_text = "<p><b>Website of the tool:</b> <a href=\"" + tool.url + "\">" + tool.url + "</a></p>"
        self.appendFile(path, url_text)
        supported_lang_text = "<p><b>Supported languages: </b>" + tool.supported_langs + "</p>"
        self.appendFile(path, supported_lang_text)
        smell_text = "<h5><b>Supported smells</b></h5><p>The tool supports detection of following set of smells.<ol>"
        for smell in self.smell_list:
            if (tool.id in smell.tool_list):
                smell_text += "<li><a href=\"" + smell.id + ".html\">" + smell.name +  "</a></li>"
        smell_text += "</ol></p>"
        self.appendFile(path, smell_text)

        self.appendFile(path, "<hr>")
        self.appendFile(path, "<a href=\"index.html\"><h3>Home</h3></a>")
        self.appendFile(path, "</div>")
        self.write_html_bottom_stuff(path)

    def generate_smell_defs_html(self):
        path = os.path.join(self.out_path, "smellDefs.html")
        self.write_html_top_stuff(path)
        self.appendFile(path, "<h2>Definitions of a Smell</h2>")
        self.appendFile(path, "<p>Many authors have defined smells from their perspective. This page attempts to provide a consolidated list of such definitions.</p>")

        ref_list = list()
        self.appendFile(path, "<ul>")
        for sd in self.smell_definition_list:
            index = -1
            if ref_list.__contains__(sd.ref_obj):
                index = ref_list.index(sd.ref_obj)
            else:
                ref_list.append(sd.ref_obj)
                index = ref_list.index(sd.ref_obj)
            if index == -1:
                print ("Error: Could not find reference object.")
                exit(7)
            sub_text = "<li><em>" + sd.definition + "</em> ["+ str(index+1) +"]</li>"
            self.appendFile(path, sub_text)
        self.appendFile(path, "</ul>")
        self.appendFile(path, "<hr>")
        #print now all the references
        self.appendFile(path, "<h4>References</h4>")
        self.appendFile(path, "<ol>")
        for ref in ref_list:
            if ref.url == "":
                self.appendFile(path, "<li>" + ref.text + "</li>")
            else:
                self.appendFile(path, "<li><a href=\"" + ref.url + "\">" + ref.text + "</a></li>")
        self.appendFile(path, "</ol>")
        self.appendFile(path, "<a href=\"index.html\"><h3>Home</h3></a>")
        self.appendFile(path, "</div>")
        self.write_html_bottom_stuff(path)



