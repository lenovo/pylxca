#!/usr/bin/env python

import argparse
import sys
import re
import shlex

class FakeGit(object):
    '''
    Help for fakegit class
    '''
    def __init__(self):
        '''
        Help for init of fake git
        '''
        parser = argparse.ArgumentParser(
            description=__doc__,
            usage='''git <command> [<args>]

The most commonly used git commands are:
   commit     Record changes to the repository
   fetch      Download objects and refs from another repository
   quit       quit shell
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        while True:
            astr = raw_input('$: ')
            # print astr
            try:
                #args_list = astr.split()
                args_list = shlex.split(astr)
                args = parser.parse_args(args_list[0:1])
            except SystemExit:
                # trap argparse error message
                print 'error'
                continue
            if not hasattr(self, args.command):
                print 'Unrecognized command'
                parser.print_help()
            elif args.command == 'help':
                parser.print_help()
            elif args.command == 'quit':
                break
            else:
                try:
                    getattr(self, args.command)(args_list)
                except SystemExit:
                    print "I am herer "
                    continue
            """
            if args.cmd in ['create', 'delete']:
                print 'doing', args.cmd
            elif args.cmd == 'help':
                parser.print_help()
            else:
                print 'done'
                break
            args = parser.parse_args(sys.argv[1:2])
            if not hasattr(self, args.command):
                print 'Unrecognized command'
                parser.print_help()
                exit(1)
            # use dispatch pattern to invoke method with same name
            getattr(self, args.command)()
            """
    def commit(self, args):
        '''
        Help for commit overridden
        '''

        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(args[1:])
        print 'Running git commit, amend=%s' % args.amend

    def fetch(self, args):
        '''
                Help for fetch overridden
        '''
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('repository')
        args = parser.parse_args(args[1:])
        print 'Running git fetch, repository=%s' % args.repository

    def quit(self):
        exit(0)

if __name__ == '__main__':
    FakeGit()