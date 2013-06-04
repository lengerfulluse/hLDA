#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import jieba
import argparse
import glob

"""Main process module to generate hLDA input files and 
   related feature files for analyzing and parameter adjustment.
"""

class PreProcess:
    theme_dir = []
    merged_document = "merge_document"

    def __init__(self, theme_dir):
        """initiaize PreProcess class with an assigned directory"""

        if not os.path.isdir(theme_dir): 
            print("%s not a valid directory, please check!" % theme_dir, file=sys.stderr)
            sys.exit(1)
        for dirname, dirnames, filenames in os.walk(theme_dir):
            for subdirname in dirnames:
                full_path = os.path.join(dirname, subdirname)
                self.theme_dir.append(full_path)
                print("read theme %s" % full_path, file=sys.stdout)
        print("all themes loaded!", file=sys.stdout)

    def launch(self):
        """Main launch for whole preprocess"""
        
    def merge_docs(self):
        """merge all documents into one bigger file"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pre-process for hLDA modulre')
    parser.add_argument('--theme', type=str, required=True, help='a particular theme directory to process')
    args = parser.parse_args()

    pre = PreProcess(args.theme)
    print("Whole pre-process done!", file=sys.stdout)

    

