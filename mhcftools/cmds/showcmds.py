
from mhcftools import arg_parser, list_commands, cerr


def init_argparser():
    p = arg_parser()
    return p


def main(args):

    # import heavy modules here

    commands = list_commands()
    cerr('Avaliable commands:')
    cerr('\n'.join(f'  {c}' for c in commands))

# EOF
