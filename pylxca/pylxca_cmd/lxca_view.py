'''
@since: 21 Oct 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo
@summary: This module is for view logic of the console commands. It parses the dictionary
data and displays on ostream.
'''

import os
import sys
import logging
#from pprint import pprint
import xml.etree.cElementTree as ElementTree

#import pylxca.pylxca_cmd

FILTER_FILE = "lxca_filters.xml"
OUTPUT_FILE = "lxca_console.out"
pylxca_filter = os.path.join(os.getenv('PYLXCA_CMD_PATH'), FILTER_FILE)
pylxca_outfile = os.path.join(os.getenv('PYLXCA_CMD_PATH'), OUTPUT_FILE)

INDENT = 0
logger = logging.getLogger(__name__)
# pylint: disable=R0205
class Tee(object):
    """ Class Tee"""
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        """ Class Tee write()"""
        for file in self.files:
            file.write(obj)
            file.flush() # If you want the output to be visible immediately
    def flush(self) :
        """ Class Tee flush()"""
        for file in self.files:
            file.flush()
# pylint: disable=C0103
# pylint: disable=R0205
class lxca_ostream(object):
    """ Class lxca_ostream"""
    def __init__(self):
        self.stdout = sys.__stdout__
        self.print_lvl = 1

    def get_lvl(self):
        """ Class lxca_ostream get_lvl()"""
        return self.print_lvl

    def set_lvl(self,lvl):
        """ Class lxca_ostream set_lvl()"""
        self.print_lvl = lvl

        try:
            if lvl == 0:
                self.stdout = open(os.devnull, 'w', encoding="utf8")
            elif lvl == 1:
                self.stdout = sys.__stdout__
            elif lvl == 2:
                self.stdout = open(pylxca_outfile, 'w', encoding="utf8")
            elif lvl == 3:
                with open(pylxca_outfile, 'w', encoding="utf8") as outfile:
                    self.stdout = Tee(sys.__stdout__, outfile)
        except Exception:
            return False
        return True

    def write(self, string):
        """ Class lxca_ostream write()"""
        sys.stdout = self.stdout
        print(string)
        sys.stdout = sys.__stdout__
# pylint: disable=C0103
# pylint: disable=R0205
class lxca_view(object):
    """ Class lxca_view"""

    def __init__(self,ostream = sys.__stdout__):
        self.ostream = ostream
        self.vf_dict =  { 'chassis':'chassisList',
                          'nodes':'nodesList',
                          'switches':'switchList',
                          'fans':'fanList',
                          'powersupplies':'powerSupplyList',
                          'fanmuxes':'fanMuxList',
                          'cmms':'cmmList',
                          'scalablesystem':'scalablesystem',
                          'discovery':'discovery',
                          'updatepolicy': 'policies'}


    def get_val(self,py_obj, tag ):
        """ Class lxca_view get_val()"""
        a = []
        try:
            if isinstance(py_obj, (dict)):
                return py_obj[tag]
            if isinstance(py_obj, (list)):
                for i in enumerate(len(py_obj)):
                    a.append(py_obj[i][tag])
        except Exception:
            return None
        return a

    def get_view_filter(self, cmd_name, filter_tag):
        """ Class lxca_view  get_view_filter() """
        vf_tree = ElementTree.parse(pylxca_filter)
        vf_root = vf_tree.getroot()

        for viewfilter in vf_root.findall(cmd_name):
            if viewfilter.attrib['name']==filter_tag:
                return viewfilter

    def print_recur(self,py_obj,view_filter):
        """Recursively prints the python object content as per view filter"""
        global INDENT
        if str(view_filter.attrib.get('type')) != "object" :
            self.ostream.write(' '*INDENT + '%s: %s' % (view_filter.tag.title(), self.get_val(py_obj,view_filter.attrib.get('name', view_filter.text))))
        #else:
        #    self.ostream.write('%s: ' % (view_filter.tag.title()))

        INDENT += 4
        # View Filter has children so
        py_obj_item = self.get_val(py_obj, view_filter.attrib.get('name', view_filter.text))
        #if py_obj_item is list then iterate through the list and call print recur for each
        if isinstance(py_obj_item, (list)):
            for item in py_obj_item:
                for elem in view_filter.getchildren():
                    self.print_recur(item,elem)
        else:
            for elem in view_filter.getchildren():
                self.print_recur(py_obj_item,elem)
        INDENT -= 4

    def print_cmd_resp_object(self,cmd_resp_item, viewfilter):
        """ Class lxca_view  print_cmd_resp_object() """
        for vf_elem in viewfilter.getchildren():
            self.print_recur(cmd_resp_item,vf_elem)


    def show_output(self,cmd_reponse, cmd_name,filter_tag):
        """ Class lxca_view  show_output() """
        viewfilter = self.get_view_filter(cmd_name,filter_tag)
        self.ostream.write("Printing "+ cmd_name + " Output:"+ "\n")

        if len(list(cmd_reponse.keys())) == 0:
            self.ostream.write("No "+ filter_tag + " returned."+ "\n")
        elif len(list(cmd_reponse.keys())) > 1:
            self.print_cmd_resp_object(cmd_reponse, viewfilter)
        else:
            for cmd_resp_item in cmd_reponse[list(cmd_reponse.keys())[0]]:
                self.print_cmd_resp_object(cmd_resp_item, viewfilter)
                self.ostream.write('\n-----------------------------------------------------')
