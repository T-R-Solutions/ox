"""Test harness: fail on access to the original tree or planning-document names.

This Python audit hook is an observation oracle for our stdlib tools, not a sandbox
for untrusted processes or native code. The parent directory is also denied.
"""
from pathlib import Path
import os
import runpy
import sys
from governance_support import EXTERNAL_DOCUMENTS


def main():
    origin = Path(sys.argv[1]).resolve()
    script, *args = sys.argv[2:]
    cwd = Path.cwd().resolve()
    if cwd.is_relative_to(origin.parent):
        raise ValueError('Independent extraction must be outside original parent')

    def audit(event, values):
        if event not in {'open', 'os.listdir', 'os.scandir'} or not values:
            return
        value = values[0]
        if not isinstance(value, (str, bytes, os.PathLike)):
            return
        path = Path(os.fsdecode(value)).resolve()
        if path.is_relative_to(origin.parent) or path.name in EXTERNAL_DOCUMENTS:
            raise PermissionError(f'Isolation oracle denied {event}: {path}')

    sys.addaudithook(audit)
    sys.argv = [script, *args]
    if script == '-m':
        module = args[0]
        sys.argv = [module, *args[1:]]
        runpy.run_module(module, run_name='__main__', alter_sys=True)
    else:
        runpy.run_path(script, run_name='__main__')


if __name__ == '__main__':
    main()
