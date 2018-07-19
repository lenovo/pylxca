'''
@since: 15 Sep 2015
@author: Girish Kumar <gkumar1@lenovo.com>, Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module provides interactive shell class which provides base for interactive shell 
feature and accepts raw input from command line 
'''

import re,sys,os,traceback
import itertools
import logging
from platform import python_version

from pylxca.pylxca_cmd import lxca_cmd
from pylxca.pylxca_cmd.lxca_icommands import InteractiveCommand
from pylxca.pylxca_cmd.lxca_view import lxca_ostream
from pylxca.pylxca_cmd import lxca_icommands
#from rlcompleter import readline

logger = logging.getLogger(__name__)

class InteractiveShell(object):

    class help(InteractiveCommand):
        """
        Prints a list of available commands and their descriptions, or the help
        text of a specific command. Requires a list of the available commands in
        order to display text for them. 
        
        @ivar commands: A dictionary of available commands, bound to L{InteractiveShell.commands}
        @type commands: C{dict}
        """
        def __init__(self, commands, shell=None):
            """
            Constructor function for L{_HelpCommand}.
            
            @param commands: A dictionary of available commands, usually L{InteractiveShell.commands}
            @type commands: C{dict}
            """
            self.commands = commands
            self.shell = shell

        def handle_command(self, opts, args):
            """
            Prints a list of available commands and their descriptions if no
            argument is provided. Otherwise, prints the help text of the named
            argument that represents a command. Does not throw an error if the
            named argument doesn't exist in commands, simply prints a warning.
            
            @param opts: Will be an empty dictionary
            @type opts: C{dict}
            @param args: The raw string passed to the command, either a command or nothing
            @type args: C{list}
            
            @return: Returns nothing, sends messages to stdout
            @rtype: None
            """
            
            if len(args) == 0:
                self.do_command_summary( )
                return

            if args[0] not in self.commands:
                self.sprint('No help available for unknown command "%s"' % args[0])
                return
            
            self.sprint(self.commands[args[0]].__doc__)

        def do_command_summary(self):
            """
            If no command is given to display help text for specifically, then
            this helper method is called to print out a list of the available
            commands and their descriptions. Iterates over the list of commands,
            and gets their summary from L{lxca_icommands.get_short_desc}
            
            @return: Returns nothing, sends messages to stdout
            @rtype: C{None}
            """
            self.sprint('The following commands are available:\n')

            cmdwidth = 0
            for name in list(self.commands.keys( )):
                if len(name) > cmdwidth:
                    cmdwidth = len(name)

            cmdwidth += 2
            for name in sorted(self.commands.keys( )):
                command = self.commands[name]

                if name == 'help':
                    continue
                try:
                    self.sprint('  %s   %s' % (name.ljust(cmdwidth),
                                     command.get_short_desc( )))
                except:
                    #For some commands there is no short desc so it will be skipped
                    continue

        def get_short_desc(self):
            return ''
    
        def get_help_message(self):
            return ''

    class exit(InteractiveCommand):
        """
        Exits the interactive shell. 
        """

        def handle_command(self, opts, args):
            sys.exit(0)

        def get_short_desc(self):
            return 'Exit the program.'
    
        def get_help_message(self):
            return 'Type exit and the program will exit.  There are no options to this command'


    def __init__(self, 
        banner="Welcome to Interactive Shell",
        prompt=" >>> "):
        self.banner = banner
        self.prompt = prompt
        self.commands = { }
        self.ostream = lxca_ostream()
        self.add_command(self.help(self.commands,self))
        self.add_command(self.exit())
        
        self.add_command(lxca_cmd.connect(self))
        self.add_command(lxca_cmd.disconnect(self))
        self.add_command(lxca_cmd.log(self))
        self.add_command(lxca_cmd.chassis(self))
        self.add_command(lxca_cmd.nodes(self))
        self.add_command(lxca_cmd.switches(self))
        self.add_command(lxca_cmd.fans(self))
        self.add_command(lxca_cmd.powersupplies(self))
        self.add_command(lxca_cmd.fanmuxes(self))
        self.add_command(lxca_cmd.cmms(self))
        self.add_command(lxca_cmd.scalablesystem(self))
        self.add_command(lxca_cmd.ostream(self))
        self.add_command(lxca_cmd.jobs(self))
        self.add_command(lxca_cmd.discover(self))
        self.add_command(lxca_cmd.manage(self))
        self.add_command(lxca_cmd.unmanage(self))
        self.add_command(lxca_cmd.configpatterns(self))
        self.add_command(lxca_cmd.configprofiles(self))
        self.add_command(lxca_cmd.configtargets(self))
        self.add_command(lxca_cmd.users(self))
        self.add_command(lxca_cmd.lxcalog(self))
        self.add_command(lxca_cmd.ffdc(self))
        self.add_command(lxca_cmd.updatepolicy(self))
        self.add_command(lxca_cmd.updatecomp(self))
        self.add_command(lxca_cmd.updaterepo(self))
        self.add_command(lxca_cmd.tasks(self))
        self.add_command(lxca_cmd.manifests(self))
        self.add_command(lxca_cmd.osimages(self))
        self.add_command(lxca_cmd.resourcegroups(self))
        self.add_command(lxca_cmd.managementserver(self))
        self.add_command(lxca_cmd.rules(self))
        self.add_command(lxca_cmd.compositeResults(self))
        self.add_command(lxca_cmd.storedcredentials(self))

    def set_ostream_to_null(self):
        self.ostream = open(os.devnull, 'w')
        
    def sprint(self,str):
        if self.ostream:
            self.ostream.write(str)
    
    def print_Hello(self):
        self.sprint("Hello")
        
    def add_command(self, command):
        if command.get_name( ) in self.commands:
            raise Exception('command %s already registered' % command.get_name( ))

        self.commands[command.get_name()] = command

    def run(self):
        self.sprint('')
        self.sprint('-'*50)
        self.sprint(self.banner)
        self.sprint('Type "help" at any time for a list of commands.')
        self.sprint('Use "lxca_shell --api" to enable Interactive Python LXCA Shell ')
        self.sprint('-'*50)
        self.sprint('')
            
        while True:
            try:
#                readline.set_completer_delims(' \t\n;')
#                readline.parse_and_bind("tab: complete")
#                readline.set_completer(self.auto_complete)
                if python_version()[0] == '2':
                    command_line = raw_input(self.prompt)
                else:
                    command_line = input(self.prompt)
            except (KeyboardInterrupt, EOFError):
                break

            self.handle_input(command_line)
            continue
            
    # TODO: Need to rename this function to handle_cli_params
    def handle_input(self, command_line):

        command_line = command_line.strip()

        # Get command
        command_args = ""
        if " " in command_line:
            command_line_index = command_line.index(" ")
            command_name = command_line[:command_line_index]
            command_args = command_line[command_line_index+1:]
        else:
            command_name = command_line

        # Show message when no command
        if not command_name:
            return

        if not command_name in self.commands:
            self.sprint('Unknown command: "%s". Type "help" for a list of commands.' % command_name)
            return 

        command = self.commands[command_name]

        opts = {}
        args = []

        # Split the input to allow for quotes option values
        re_args = re.findall('\-\-\S+\=\"[^\"]*\"|\S+', command_args)
        #re_args = re.findall('\-\-\S+|\-\S+|\S+[\s*\w+]*', command_args)
        # Parse args if present
        for i in range(0, len(re_args)):
            args.append( re_args[i] )
        try:
            return command.handle_command(opts=opts, args=args)
        except Exception as err:
            logger.error("Exception occurred while processing command.")
        return
    
    # TODO: We should remove this, All API level code should give call to handle_input_dict rather
    def handle_input_args(self, command_name,*args, **kwargs):
        # Show message when no command
        if not command_name:
            return

        if not command_name in self.commands:
            self.sprint('Unknown command: "%s". Type "help" for a list of commands.' % command_name)
            return

        command = self.commands[command_name]

        opts = {}
        args = {}
       
        for item in kwargs['kwargs']:
            args['--' + item] = kwargs['kwargs'][item]
        
        try:
            return command.handle_command(opts=opts, args=list(itertools.chain(*list(args.items()))))
        except Exception as err:
            self.sprint("Exception occurred while processing command.")
            raise err
            
    # TODO: We should rename this to handle_api_params
    def handle_input_dict(self, command_name,con, param_dict):
        # Show message when no command
        if not command_name:
            return

        if not command_name in self.commands:
            self.sprint('Unknown command: "%s". Type "help" for a list of commands.' % command_name)
            return

        command = self.commands[command_name]
        
        try:
            #return command.handle_command(param_dict,con)
            return command.handle_input(param_dict, con)
        except Exception as err:
            self.sprint("Exception occurred while processing command.")
            raise err
        
        
    
    """
    TODO:
    def auto_complete(self, text, state):
        command_list = self.commands.keys()
        re_space = re.compile('.*\s+$', re.M)
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in command_list][state]
        # account for last argument ending in a space
        if re_space.match(buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in command_list:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in command_list if c.startswith(cmd)] + [None]
        return results[state]
    """
