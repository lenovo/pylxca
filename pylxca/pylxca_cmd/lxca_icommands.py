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
import ast
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
    
    def _process_epilog(self, str_list):
        epilog = "\r\n ".join(str_list)
        epilog = textwrap.dedent(epilog)
        return epilog

    def _validate_combination(self, input_dict, valid_dict):
        '''
        This function validate input combinations
        :param input_dict:  input dict of parameters
        :param valid_list:  valid combination of parameters list
        :return: if True returns True and choosed combination of parameter
                 on failure return false and suggested_combination of parameters
        '''

        try:
            if 'subcmd' in input_dict:
                valid_list = valid_dict[input_dict['subcmd']]
            else:
                valid_list = valid_dict['global']
        except Exception as e:
            raise Exception("Error in getting valid_list")

        # remove None and empty string and len zero lists
        # create copy dict
        copy_input_dict = {}
        for k in input_dict.keys():
            if k not in ['func', 'view','subcmd']:
                if not (input_dict[k] == None or (isinstance(input_dict[k], list) and len(input_dict[k]) == 0)):
                    copy_input_dict[k] = input_dict[k]

        input_key_set = set(copy_input_dict.keys())

        for comb in valid_list:
            comb_set = set(comb)
            if input_key_set == comb_set:
                return True, comb

        # Check for suggestion
        suggested_combination = ""
        for comb in valid_list:
            comb_set = set(comb)
            if len(input_key_set & comb_set) > 0:
                suggested_combination += str(comb)

        return False, suggested_combination

    def get_additional_detail(self):
        epilog = self.command_data[self.__class__.__name__].get('additional_detail', [])
        return self._process_epilog(epilog)

    def get_short_desc(self):
        return self.command_data[self.__class__.__name__]['description']

    def post_parsing_validation(self, opts):
        valid_combination = self.command_data[self.__class__.__name__].get('valid_combination', None)

        if valid_combination:
            valid, combination = self._validate_combination(opts, valid_combination)
            if not valid:
                raise Exception("Invalid Missing Arguments %s" % str(combination))

    def cmd1(self, args):
        print('cmd1', args)

    def _preprocess_argparse_dict(self, cmd_dict):
        try:
            replace_with = {"int": int, "boolean": bool, "json.loads":json.loads, "ast.literal_eval":ast.literal_eval}
            if 'type' in cmd_dict:
                if cmd_dict['type'] in replace_with.keys():
                    cmd_dict['type'] = replace_with[cmd_dict['type']]
        except Exception as err:
            raise("Error while preprocessing  argparse dict for type replacement")
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
                self._preprocess_argparse_dict(cmd_dict)
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
                self._preprocess_argparse_dict(cmd_dict)
                group.add_argument(*cmd_args_tuple, **cmd_dict)

        # Add subcommand if any specified
        subcmd_list = self.command_data[self.__class__.__name__].get('subcmd', None)
        if subcmd_list:
            sub_parser = parser.add_subparsers(dest='subcmd')
            sub_parser.required = True
            for subcmd in subcmd_list:
                sub_cmd_name = subcmd['name']
                subcmd_args_list = subcmd['subcmd_args']
                parser_internal = sub_parser.add_parser(sub_cmd_name,
                                                        formatter_class=argparse.RawDescriptionHelpFormatter,
                                                        help=subcmd['help'], epilog=self._process_epilog(subcmd['additional_detail']))
                parser_internal.required = True
                parser_internal.set_defaults(func=self.cmd1)
                for opt in subcmd_args_list:
                    cmd_args = opt[0]["args"]
                    cmd_args_list = cmd_args.split(",")
                    cmd_args_tuple = tuple(cmd_args_list)
                    cmd_dict = opt[0]["opt_dict"]
                    self._preprocess_argparse_dict(cmd_dict)
                    parser_internal.add_argument(*cmd_args_tuple, **cmd_dict)

                # Add mutually exclusive args if any specified
                arg_list = subcmd.get('mutually_exclusive_args', None)
                if arg_list:
                    group = parser_internal.add_mutually_exclusive_group()
                    for opt in arg_list:
                        cmd_args = opt[0]["args"]
                        cmd_args_list = cmd_args.split(",")
                        cmd_args_tuple = tuple(cmd_args_list)
                        cmd_dict = opt[0]["opt_dict"]
                        self._preprocess_argparse_dict(cmd_dict)
                        group.add_argument(*cmd_args_tuple, **cmd_dict)

        return parser

    def invalid_input_err(self):
        self.sprint("Invalid Input ")
        self.sprint("for help type command -h")
        return
    
    def sprint(self,str):
        if self.shell: self.shell.sprint(str)

    def parse_args(self, args):
        try:
            parser = self.get_argparse_options()
            namespace = parser.parse_args(args)
            opt_dict = vars(namespace)
            self.post_parsing_validation(opt_dict)
        except argparse.ArgumentError as e:
            raise(e)
        except SystemExit as e:
            raise(e)
        except AttributeError as e:
            #TODO  move this some where
            extype, ex, tb = sys.exc_info()
            formatted = traceback.format_exception_only(extype, ex)[-1]
            message = "Check getopt short and long options  %s" % (formatted)
            raise RuntimeError(message, tb)
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
    
    def handle_command(self,  opts, args):
        
        con_obj = None

        try:
            opts = self.parse_args(args)
        except SystemExit as e:
            # ignore this as we need to continue on shell
            return

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
            self.sprint("Error \"%s\" occurred while executing command."%(re.response.reason))
        except ConnectionError as re:
            self.sprint("Error %s occurred while executing command."%(re))
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        except Exception as err:
            self.sprint("Error occurred: %s" %(err)) 
            
        return out_obj
