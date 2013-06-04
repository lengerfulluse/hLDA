#!/usr/bin/python
from __future__ import print_function
import argparse
import os
import operator
import sys
import string

""" 
   Basic class to analysis the <mode.assign> file.
   to print the final sentence cluser, we also need
   another file, namely <RemoveStop.temp>.
"""

class ModeAssign:
    assign_dir = ""
    remove_stop_dir = ""
    corpus = {}
    assign = {}
    # default display result on stdout.
    output = sys.stdout

    def __init__(self, assign_dir, remove_stop_dir, output=sys.stdout):
        self.assign_dir = assign_dir
        self.remove_stop_dir = remove_stop_dir
        self.output = output
        if not os.path.isfile(self.assign_dir) or not os.path.isfile(self.remove_stop_dir):
            sys.stdout.write("file not found!\n")
            sys.exit(1)
        sys.stdout.write("loading analysis file:\n%s\n%s\n" % (self.assign_dir, self.remove_stop_dir))
        
    def read_corpus(self):
        with open(self.remove_stop_dir, 'r') as f:
            sen_no = 0
            for line in f.readlines():
                self.corpus[str(sen_no)] = line
#                sys.stdout.write("add line %s\n" % line)
                sen_no += 1
        sys.stdout.write("read corpus done!\n")

    def assign_path(self):
        with open(self.assign_dir, 'r') as f:
            for line in f.readlines():
                words = string.split(line, " ")
                doc_no = words[0]
                leaf_node = words[len(words)-1]
                if self.assign.has_key(leaf_node):
                    self.assign[leaf_node] += ":" + doc_no
                else:
                    self.assign[leaf_node] = doc_no
            sys.stdout.write("read mode.assign file done!\n")

        # temp unsorted dict {doc_id: doc_nums}
        unsorted_node = {}
        for key, value in self.assign.iteritems():
            unsorted_node[value] = len(string.split(value, ':'))
        
        sorted_node = sorted(unsorted_node.iteritems(), key=operator.itemgetter(1))
        sorted_node.reverse()
        for (key, value) in sorted_node:
            docs = string.split(key, ':')
            print('%d\t' % len(docs), file=sys.stdout, end='')
            print('+++++++++++++++++++++++++++++++++++++++++++++  %d   ++++++++++++++++++++++++++++++++++++++++++' % len(docs), file=self.output)
            for doc in docs:
                if self.corpus.has_key(doc):
                    print(self.corpus[doc], file=self.output)
                else:
                    print("%s not found!" % doc, file=sys.stderr)
        # sort dict according to doc_nums

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='stupid path assign analysis for hlda-c result')
    parser.add_argument('--assign', type=str, required=True, help='mode.assign file position')
    parser.add_argument('--corpus', type=str, required=True, help='corpus file to contain origin sentence per line')
    parser.add_argument('--output', type=str, nargs='?', help='destinationf file for the analysis result')
    args = parser.parse_args()
    if not args.output:
        output = sys.stdout
    else:
        output = open(args.output, 'w')

    mode_assign = ModeAssign(args.assign, args.corpus, output)
    mode_assign.read_corpus();
    mode_assign.assign_path();
    sys.stdout.write("\nmode assign analysis done!\n")

