'''
@since: 15 Sep 2015
@author: Girish Kumar <gkumar1@lenovo.com>, Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo
@summary: This module provides interactive command class which provides base
implementation for all command classes
'''

import sys
import os
import json
import traceback
import argparse
import textwrap
import ast
from pylxca.pylxca_api import LxcaApi
from pylxca.pylxca_api.lxca_rest import HTTPError
from pylxca.pylxca_api.lxca_connection import ConnectionError
from pylxca.pylxca_cmd import lxca_view

CMD_DATA_JSON_FILE   = "lxca_cmd_data.json"
pylxca_cmd_data   = os.path.join(os.getenv('PYLXCA_CMD_PATH'), CMD_DATA_JSON_FILE)
# pylint: disable=C0301
class InteractiveCommand(object):
    """ Class Interactive command"""
    def __init__(self, shell=None ):
        self.shell = shell
        filepointer = open(pylxca_cmd_data, 'r', encoding="utf8")
        self.command_data = json.load(filepointer)

    def get_options(self):
        """ get_options"""
        return {}

    def get_name(self):
        """ get_name"""
        return self.__class__.__name__
    def get_help_option(self):
        """ get_help_options"""
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
        except Exception:
            raise Exception("Error in getting valid_list")

        # remove None and empty string and len zero lists
        # create copy dict
        copy_input_dict = {}
        for k in input_dict.keys():
            if k not in ['func', 'view','subcmd']:
                if not (input_dict[k] is None or (isinstance(input_dict[k], list) and len(input_dict[k]) == 0)):
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
        """ get_help_options"""
        epilog = self.command_data[self.__class__.__name__].get('additional_detail', [])
        return self._process_epilog(epilog)

    def get_short_desc(self):
        """ get_short_desc"""
        return self.command_data[self.__class__.__name__]['description']

    def post_parsing_validation(self, opts):
        """ post_parsing_validation"""
        valid_combination = self.command_data[self.__class__.__name__].get('valid_combination', None)

        if valid_combination:
            valid, combination = self._validate_combination(opts, valid_combination)
            if not valid:
                raise Exception (f"Invalid Missing Arguments {str(combination)}")

    def cmd1(self, args):
        """ cmd1"""
        print('cmd1', args)

    def _preprocess_argparse_dict(self, cmd_dict):
        try:
            replace_with = {"int": int, "boolean": bool, "json.loads":json.loads, "ast.literal_eval":ast.literal_eval}
            if 'type' in cmd_dict:
                if cmd_dict['type'] in replace_with.keys():
                    cmd_dict['type'] = replace_with[cmd_dict['type']]
        except Exception:
            raise Exception("Error while preprocessing  argparse dict for type replacement")
    def get_argparse_options(self):
        """ get_argparse_options"""
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
        """ invalid_input_err"""
        self.sprint("Invalid Input ")
        self.sprint("for help type command -h")
        return
    def sprint(self,str):
        """ sprint"""
        if self.shell:
            self.shell.sprint(str)
    def parse_args(self, args):
        """ parse_args"""
        try:
            parser = self.get_argparse_options()
            namespace = parser.parse_args(args)
            opt_dict = vars(namespace)
            self.post_parsing_validation(opt_dict)
        except argparse.ArgumentError as argparseerror:
            raise argparseerror
        except SystemExit as systemexiterror:
            raise systemexiterror
        except AttributeError:
            #TODO  move this some where
            extype, ex, tb = sys.exc_info()
            formatted = traceback.format_exception_only(extype, ex)[-1]
            message = f"Check getopt short and long options  {formatted}"
            raise RuntimeError(message, tb)
        return opt_dict

    def handle_no_input(self,con_obj):
        """ parse_args"""
        #no_opt action can differ command to command so override this function if required
        obj = None
        try:
            api = LxcaApi()
            obj = api.api(self.get_name(), None,con_obj)
        except ConnectionError:
            self.sprint("Connection is not Initialized, Try connect")
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        except Exception:
            self.sprint("Exception occurred")
        return obj
    def handle_input(self, dict_handler,con_obj = None):
        """ handle_input"""
        obj = None
        api = LxcaApi()
        obj = api.api(self.get_name(),dict_handler,con_obj)
        return obj
    def show_output(self, py_obj,view_filter = "default"):
        """ show_output"""
        ostream = sys.__stdout__
        if self.shell:
            ostream = self.shell.ostream
        view = lxca_view.lxca_view(ostream)
        view.show_output(py_obj,self.get_name(),view_filter)
        return
    def handle_output(self, py_obj):
        """ handle_output"""
        return
    def handle_command(self,  opts, args):
        """ handle_command"""
        con_obj = None

        try:
            opts = self.parse_args(args)
        except SystemExit:
            # ignore this as we need to continue on shell
            return

        out_obj = None
        #opt_dict = None
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
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        return out_obj
