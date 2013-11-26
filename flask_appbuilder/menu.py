from flask import url_for
from .security.models import PermissionView

class MenuItem(object):

    name = ""
    baseview = None
    href = ""
    icon = ""
    childs = []

    def __init__(self, name, href="", icon="", childs=[], baseview = None):
        self.name = name
        self.href = href
        self.icon = icon
        if (self.childs):
            self.childs = childs
        else: self.childs = []
        self.baseview = baseview

    def get_url(self):
        print self.name
        if not self.href:
            return url_for('%s.%s' % (self.baseview.endpoint, self.baseview.default_view))
        else:
            return self.href

    def __repr__(self):
        return self.name + ' href=' + self.get_url()

class Menu(object):

    menu = []

    def get_list(self):
        return self.menu

    # Mal programado para rever
    def find_category(self, category):
        for i in self.menu:
            if i.name == category:
                return i
            else:
                for j in i.childs:
                    if j.name == category:
                        return j


    def add_category(self, category, icon="", parent_category=""):
        if parent_category == "":
            self.menu.append(MenuItem(name=category, icon = icon))
        else:
            self.find_category(parent_category).childs.append(MenuItem(name=category, icon = icon))
        pvm = PermissionView()
        try:
            pvm = pvm.add_menu_permissions(category)
        except:
            print "Menu add_category Erro: Maybe db not created"


    def add_link(self, name, href="", icon="", parent_category="", baseview = None):
        menu_item = self.find_category(parent_category)
        if menu_item:
            menu_item.childs.append(MenuItem(name=name, href=href, icon = icon, baseview = baseview))
        else:
            self.add_category(category=parent_category)
            self.find_category(parent_category).childs.append(MenuItem(name=name, 
                                        href=href, icon = icon, baseview = baseview))
        pvm = PermissionView()
        try:
            pvm = pvm.add_menu_permissions(name)
        except:
            print "Menu add_category Erro: Maybe db not created"


    def add_separator(self, parent_category=""):
        self.find_category(parent_category).childs.append(MenuItem("-"))
