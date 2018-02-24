#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 19:36:30 2018

@author: alex
"""

import contextlib
import os
from pathlib import Path

def silent_remove(pathname):
    print ("Removing "+pathname)
    with contextlib.suppress(FileNotFoundError):
        os.remove(pathname)

def re_root_symlink(link_from,link_to,new_root):
    silent_remove(link_from)
    new_link_to = os.path.join(new_root, link_to[1:])
    print ("ln -s {} {}".format(new_link_to, link_from))
    os.symlink(new_link_to, link_from)
 
def symlinks(top_dir):
    """
    :returns: dict mapping from pathnames to destination pathnames
    """
    link_dict = dict()
    for dirName, subdirList, fileList in os.walk(top_dir):
        for file in subdirList + fileList:
            pathname = os.path.join(dirName,file)
            print("Trying " + pathname)
            path = Path(pathname)
            print(path)
            if path.is_symlink():
                print("Resolving " + path.as_posix())
                try:
                    destination_path = path.resolve()
                    if destination_path.root == "/":
                        link_dict[pathname] = destination_path.as_posix()
                except Exception as e:
                    print("Corrupt symlink " + path.as_posix())
                    print(e)
    return link_dict

def re_root_symlinks(top_dir, new_root):
    """
    Change all symlinks that point to root ("/"), so they point to new_root
    """
    for link_from,link_to in symlinks(top_dir).items():
        re_root_symlink(link_from,link_to,new_root)

# Should be called after "cd new_root"
if __name__ == '__main__':
    re_root_symlinks(".", os.getcwd())
