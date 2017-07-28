'''
@since: 21 Oct 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module is for view logic of the console commands. It parses the dictionary 
data and displays on ostream.
'''

import json, re, os, sys, logging
from pprint import pprint
import xml.etree.cElementTree as ElementTree
from types import DictionaryType

import pylxca.pylxca_cmd

filter_file = "lxca_filters.xml"
output_file = "lxca_console.out"
pylxca_filter = os.path.join(os.getenv('PYLXCA_CMD_PATH'), filter_file)
pylxca_outfile = os.path.join(os.getenv('PYLXCA_CMD_PATH'), output_file)

indent = 0
logger = logging.getLogger(__name__)

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

class lxca_ostream:
    def __init__(self):
        self.stdout = sys.__stdout__
        self.print_lvl = 1

    def get_lvl(self):
        return self.print_lvl

    def set_lvl(self,lvl):
        self.print_lvl = lvl

        try:
            if lvl == 0:
                self.stdout = open(os.devnull, 'w')
            elif lvl == 1:
                self.stdout = sys.__stdout__
            elif lvl == 2:
                self.stdout = open(pylxca_outfile, 'w')
            elif lvl == 3:
                outfile = open(pylxca_outfile, 'w')
                self.stdout = Tee(sys.__stdout__, outfile)
        except Exception as e:
            return False
        return True

    def write(self, string):
        sys.stdout = self.stdout
        print string
        sys.stdout = sys.__stdout__
        
class lxca_view:
    
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
        a = []
        try:
            if isinstance(py_obj, (dict)):
                return(py_obj[tag])
            if isinstance(py_obj, (list)):
                
                for i in range(0, len(py_obj)):
                    a.append(py_obj[i][tag])
        except:
            return None
        return a
    
    def get_view_filter(self, cmd_name, filter_tag): 
        vf_tree = ElementTree.parse(pylxca_filter)
        vf_root = vf_tree.getroot()

        for vf in vf_root.findall(cmd_name):
            if vf.attrib['name']==filter_tag:
                return vf
            
    def print_recur(self,py_obj,view_filter):
        """Recursively prints the python object content as per view filter"""
        global indent
        if str(view_filter.attrib.get('type')) != "object" :
            self.ostream.write(' '*indent + '%s: %s' % (view_filter.tag.title(), self.get_val(py_obj,view_filter.attrib.get('name', view_filter.text))))
        #else:
        #    self.ostream.write('%s: ' % (view_filter.tag.title()))
            
        indent += 4
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
        indent -= 4
        
    def print_cmd_resp_object(self,cmd_resp_item, vf):
        for vf_elem in vf.getchildren():
            self.print_recur(cmd_resp_item,vf_elem)
            
                    
    def show_output(self,cmd_reponse, cmd_name,filter_tag):
        vf = self.get_view_filter(cmd_name,filter_tag)
        self.ostream.write("Printing "+ cmd_name + " Output:"+ "\n")
        
        if len(cmd_reponse.keys()) == 0:
            self.ostream.write("No "+ filter_tag + " returned."+ "\n")
        elif len(cmd_reponse.keys()) > 1:
            self.print_cmd_resp_object(cmd_reponse, vf)
        else:
            for cmd_resp_item in cmd_reponse[cmd_reponse.keys()[0]]:
                self.print_cmd_resp_object(cmd_resp_item, vf)
                self.ostream.write('\n-----------------------------------------------------')