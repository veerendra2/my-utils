#!/usr/bin/env python
"""
Author : Veerendra K
Description : Ultimate function for execute shell commands in python
"""
import subprocess


def execute(cmd, verbose=False):
    """
    :param cmd: Command to execute
    :param verbose: Be verbose
    :return: On success, it return command output. On failure, it returns 1
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = []
    while True:
        line = p.stdout.readline()
        out.append(line)
        if verbose:
            print line,
        if not line and p.poll() is not None:
            break
    if p.returncode != 0:
        print p.stderr.read().strip()
        return 1
    else:
        return ''.join(out).strip()
