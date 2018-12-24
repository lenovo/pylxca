'''
@since: 15 Sep 2015
@author: Girish Kumar <gkumar1@lenovo.com>, Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module provides interactive command class which provides base 
implementation for all command classes 
'''

import sys,getopt,os,json,logging, traceback
import argparse
from pylxca.pylxca_api import lxca_api
from pylxca.pylxca_api.lxca_rest import HTTPError
from pylxca.pylxca_api.lxca_connection import ConnectionError
from pylxca.pylxca_cmd import lxca_view
import textwrap

cmd_data_json_file   = "lxca_cmd_data.json"
pylxca_cmd_data   = os.path.join(os.getenv('PYLXCA_CMD_PATH'), cmd_data_json_file)

class InteractiveCommand(object):
    def __init__(self, shell=None ):
        self.shell = shell
        fp = open(pylxca_cmd_data, 'r')
        self.command_data = json.load(fp)

    def get_options(self):
        return {}

    def get_name(self):
        return self.__class__.__name__
    
    def get_help_option(self):
        return self.command_data[self.__class__.__name__].get('add_help', True)
    
    def get_additional_detail(self):
        epilog = self.command_data[self.__class__.__name__].get('additional_detail', [])
        epilog = "\r\n ".join(epilog)
        epilog = textwrap.dedent(epilog)
        return epilog

    def get_short_desc(self):
        return self.command_data[self.__class__.__name__]['description']

    def cmd1(self, args):
        print('cmd1', args)

    def get_argparse_options(self):
        parser = argparse.ArgumentParser(prog=self.get_name(), description=self.get_short_desc(),
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog=self.get_additional_detail(),
                                         add_help=self.get_help_option())

        arg_list = self.command_data[self.__class__.__name__].get('cmd_args', None)
        if arg_list:
            for opt in arg_list:
                cmd_args = opt[0]["args"]
                cmd_args_list = cmd_args.split(",")
                cmd_args_tuple = tuple(cmd_args_list)
                cmd_dict = opt[0]["opt_dict"]
                parser.add_argument(*cmd_args_tuple, **cmd_dict)

        # Add mutually exclusive args if any specified
        arg_list = self.command_data[self.__class__.__name__].get('mutually_exclusive_args', None)
        if arg_list:
            group = parser.add_mutually_exclusive_group()
            for opt in arg_list:
                cmd_args = opt[0]["args"]
                cmd_args_list = cmd_args.split(",")
                cmd_args_tuple = tuple(cmd_args_list)
                cmd_dict = opt[0]["opt_dict"]
                group.add_argument(*cmd_args_tuple, **cmd_dict)

        # Add subcommand if any specified
        subcmd_list = self.command_data[self.__class__.__name__].get('subcmd', None)
        if subcmd_list:
            sub_parser = parser.add_subparsers()
            for subcmd in subcmd_list:
                sub_cmd_name = subcmd['name']
                subcmd_args_list = subcmd['subcmd_args']
                parser_internal = sub_parser.add_parser(sub_cmd_name)
                parser_internal.required = True
                parser_internal.set_defaults(func=self.cmd1)
                for opt in subcmd_args_list:
                    cmd_args = opt[0]["args"]
                    cmd_args_list = cmd_args.split(",")
                    cmd_args_tuple = tuple(cmd_args_list)
                    cmd_dict = opt[0]["opt_dict"]
                    parser_internal.add_argument(*cmd_args_tuple, **cmd_dict)

        return parser

    def invalid_input_err(self):
        self.sprint("Invalid Input ")
        self.sprint("for help type command -h")
        return
    
    def sprint(self,str):
        if self.shell: self.shell.sprint(str)
        
    def parse_args(self, opts, argv):
        opt_dict = {}
        
        for opt, arg in opts:
            opt_dict[opt.strip('-')] = arg
        
        return opt_dict

    def handle_no_input(self,con_obj):
        #no_opt action can differ command to command so override this function if required
        obj = None
        try:
            api = lxca_api()
            obj = api.api(self.get_name(), None,con_obj)
        except ConnectionError:
            self.sprint("Connection is not Initialized, Try connect")
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        except Exception as err:
            self.sprint("Exception occurred: %s" %(err)) 
        return obj
    
    def handle_input(self, dict_handler,con_obj = None):
        obj = None
        api = lxca_api()
        obj = api.api(self.get_name(),dict_handler,con_obj)
        return obj
    
    def show_output(self, py_obj,view_filter = "default"):

        ostream = sys.__stdout__
        if self.shell:
            ostream = self.shell.ostream
        view = lxca_view.lxca_view(ostream)
        view.show_output(py_obj,self.get_name(),view_filter)
        return
    
    def handle_output(self, py_obj):
        return
    
    def handle_command(self, opts, args):
        
        con_obj = None
        
        try:
            #opts, argv = getopt.getopt(args, self.get_char_options(), self.get_long_options())
            parser = self.get_argparse_options()
            namespace = parser.parse_args(args)
            opts = vars(namespace)
        except argparse.ArgumentError as e:
            print(str(e))
            return
        except SystemExit as e:
            print(str(e))
            return
        except AttributeError as e:
            extype, ex, tb = sys.exc_info()
            formatted = traceback.format_exception_only(extype, ex)[-1]
            message = "Check getopt short and long options  %s" % (formatted)
            raise RuntimeError(message, tb)

        '''
        for opt, arg in opts:
            if '-h' in opt:
                self.sprint(self.__doc__)
                return
            if 'con' in opt:
                con_obj = arg
        '''
        out_obj = None
        opt_dict = None
        view_filter = "default"
        
        try:
            if not opts:
                out_obj = self.handle_no_input(con_obj)
            else:
                #opt_dict = self.parse_args(opts, argv)

                out_obj = self.handle_input(opts,con_obj)
                if opts:
                    view_filter = next((item for item in [opts.get('v') , opts.get('view')] if item is not None),'default')
        
            if out_obj:
                if isinstance(out_obj, dict):
                    self.show_output(out_obj,view_filter)
                else:
                    self.handle_output(out_obj)
        except ConnectionError:
            self.sprint("Connection is not Initialized, Try connect")
        except HTTPError as re:
            self.sprint("Exception %s occurred while executing command."%(re.response.content))
        except ConnectionError as re:
            self.sprint("Exception %s occurred while executing command."%(re.response.content))
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        except Exception as err:
            self.sprint("Exception occurred: %s" %(err)) 
            
        return out_obj