import argparse

def cmd1(args):
    print('cmd1', args)
def cmd2(args):
    print('cmd2', args)

parser1 = argparse.ArgumentParser()

parser1.add_argument("-i", "--info",  help="Display more information")

parser2 = argparse.ArgumentParser()
subparsers = parser2.add_subparsers(dest='cmd')

parserCmd1 = subparsers.add_parser("cmd1", help="First Command")
parserCmd1.set_defaults(func=cmd1)

parserCmd2 = subparsers.add_parser("cmd2", help="Second Command")
parserCmd2.add_argument("-o", "--output", help="Redirect Output")
parserCmd2.set_defaults(func=cmd2)


args, extras = parser1.parse_known_args()
if len(extras)>0 and extras[0] in ['cmd1','cmd2']:
    args = parser2.parse_args(extras, namespace=args)
    args.func(args)
else:
    print('doing system with', args, extras)



'''
If you add parent parser in subparser for parent add_help has to be false


import argparse
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()
parser.add_argument("--foo",help="first ")
parser_a = subparser.add_parser("a")
parser_a.add_argument("-x")

parser_b = subparser.add_parser("b")
parser_b.add_argument("-y",help="first ")
parser_b.add_argument("-z",help="second ")

rep = parser.parse_args()

print rep
'''

'''
add_mutually_exclusive_group can not be combined with variables of add_group variables


import argparse

parser = argparse.ArgumentParser(description='Simple example')
parser.add_argument('name', help='Who to greet', default='World')
me_group = parser.add_mutually_exclusive_group()

# Create two argument groups
foo_group = parser.add_argument_group(title='Foo options')
bar_group = parser.add_argument_group(title='Bar options')
# Add arguments to those groups
foo_group.add_argument('--bar_this')
foo_group.add_argument('--bar_that')
bar_group.add_argument('--foo_this')
bar_group.add_argument('--foo_that')
me_group.add_argument("--zoo")
me_group.add_argument("--yoo")

args = parser.parse_args()
'''
