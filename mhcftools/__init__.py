
import os
import sys
import argparse
import argcomplete
import pathlib


def cout(msg):
    print(msg, file=sys.stdout)


def cerr(msg):
    print(msg, file=sys.stderr)
    sys.stderr.flush()


def cexit(msg):
    cerr(msg)
    sys.exit(1)


def greet():
    import platform
    cerr(f'mhcftools - microhaplotype call format tools\n'
         f'Host: {platform.uname().node}')


def usage():
    cexit('  usage:\n'
          '    mhcftools CMD [ARGS]'
          '  try: mhcftools showcmds')


def arg_parser(desc=''):
    p = argparse.ArgumentParser(description=desc)
    p.add_argument('--debug', action='store_true', default=False,
                   help='open ipdb when uncatched exception is raised')
    return p


def list_commands():
    # read sqpy.cmds directory
    import mhcftools.cmds
    cmds_directory = pathlib.Path(mhcftools.cmds.__file__).parent
    cmds = set(
        [p.name.removesuffix('.py') for p in cmds_directory.iterdir()]
    ) - {'__init__', '__pycache__'}
    return sorted(cmds)


def cmd_autocomplete(tokens):

    # prepare line

    last_token = tokens[-1]

    if len(tokens) > 1 and (last_token.startswith('.') or last_token.startswith('~')):
        # let bash complete using directory listing
        sys.exit(1)

    # prepare the completion lists
    completions = list_commands()

    if len(tokens) != 1:
        completions = [opt for opt in completions if opt.startswith(last_token)]

    # send results through fd 8
    ifs = os.environ.get('IFS', '\013')
    out_stream = os.fdopen(8, 'w')
    out_stream.write(ifs.join(completions))
    sys.exit(0)


def main():

    # check if we are running under bash autocomplete process
    if '_ARGCOMPLETE' in os.environ:
        line = os.environ.get('COMP_LINE', '')
        tokens = line.split()
        if len(tokens) == 1 or (len(tokens) == 2 and not line.endswith(' ')):
            cmd_autocomplete(tokens)
        os.environ['COMP_LINE'] = line.split(' ', 1)[1]
        os.environ['COMP_POINT'] = str(len(os.environ['COMP_LINE']))
        cmd = tokens[1]

    else:
        # running normally
        greet()
        if len(sys.argv) == 1:
            usage()
        cmd = sys.argv[1]

    sys.exit(0)

# EOF
