#!/usr/bin/env python
from __future__ import with_statement
from os.path import dirname, realpath, join as path_join, expanduser, exists, islink
from os import stat, readlink, symlink, lstat, unlink, mkdir
from stat import S_ISLNK
from shutil import copyfile
from sys import exit, stdout
from difflib import unified_diff
from errno import EEXIST

FILES = (
    'apply_patch.py',
    'btrfs_backup.sh',
    'couleur3.ch',
    'detect_encoding.py',
    'hgeditor',
    'nova.sh',
    'pyreplace.py',
    'releaser.py',
    'rename_torrent.py',
    'scm.py',
    'system_load.py',
    'taskset_isolated.py',
    'upload_private.sh',
    'upload_tmp.sh',
    'cherry_picker.py',
    'gh_pr.sh',
    'dedup.py',
)

def main():
    srcdir = realpath(dirname(__file__))
    dstdir = path_join(expanduser('~'), 'bin')
    try:
        mkdir(dstdir)
    except OSError as err:
        if err.errno == EEXIST:
            pass
        else:
            print("Unable to create directory %s: %s" % (dstdir, err))
            exit(1)

    files = []
    for name in FILES:
        src = path_join(srcdir, name)
        dst = path_join(dstdir, name)
        try:
            dst_link = readlink(dst)
        except OSError:
            pass
        else:
            if dst_link == src:
                continue
        files.append((name, src, dst))

    err = False
    for name, src, dst in files:
        if (not exists(dst)) or islink(dst):
            continue
        err = True
        print("Error: %s already exists" % dst)
        with open(src) as fp:
            src_lines = fp.readlines()
        with open(dst) as fp:
            dst_lines = fp.readlines()
        for line in unified_diff(src_lines, dst_lines, src, dst):
            stdout.write(line)
        print
    if err:
        exit(1)

    if not files:
        print("Nothing to do (symlinks already created).")
        exit(0)

    for name, src, dst in files:
        try:
            lstat(dst)
        except OSError:
            pass
        else:
            # remove broken link
            unlink(dst)
        print("Create link ~/bin/%s" % name)
        symlink(src, dst)

if __name__ == "__main__":
    main()

