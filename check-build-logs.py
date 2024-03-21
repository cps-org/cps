#!/usr/bin/env python

import re
import sys

from typing import List

# -----------------------------------------------------------------------------
def read_log(path: str) -> List[str]:
    out = []

    with open(path, 'rt') as f:
        for line in f:
            out.append(re.sub('\033\\[[0-9;]*m', '', line.strip()))

    return out

# -----------------------------------------------------------------------------
def main(log_path: str, out_path: str):
    re_loc = r'(?P<file>[^:]+):((?P<line>[0-9]+):)?\s*'
    re_info = r'(?P<type>\w+):\s*(?P<message>.*)'
    lines = read_log(log_path)

    result = 0
    for line in lines:
        m = re.match(re_loc + re_info, line)
        if m:
            t = m.group('type').lower()
            if t not in {'warning', 'error'}:
                t = 'warning'

            params = {'file': m.group('file')}
            line = m.group('line')
            if line:
                params['line'] = line

            p = ','.join([f'{k}={v}' for k, v in params.items()])
            m = m.group('message')
            print(f'::{t} {p}::{m}')
            result = 1

    with open(out_path, 'at') as f:
        f.write(f'result={result}\n')

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if __name__ == '__main__':
    main(*sys.argv[1:])
