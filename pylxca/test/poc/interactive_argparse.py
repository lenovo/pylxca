import argparse
parser = argparse.ArgumentParser(prog='PROG', description='description')
args = ('--cmd','-c')
opt_dict = {'choices':['create', 'delete', 'help', 'quit'], 'help':' Enter your command'}
#parser.add_argument('cmd', choices=['create','delete','help','quit'])
parser.add_argument(*args, **opt_dict)
while True:
    astr = raw_input('$: ')
    # print astr
    try:
        args = parser.parse_args(astr.split())
    except SystemExit:
        # trap argparse error message
        print 'error'
        continue
    if args.cmd in ['create', 'delete']:
        print 'doing', args.cmd
    elif args.cmd == 'help':
        parser.print_help()
    else:
        print 'done'
        break