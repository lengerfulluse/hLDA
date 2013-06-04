#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import sys
import operator
import string

class WordAllocate:
	levels_dir = ""
	# words level allocation.
	allocation = {}
	def __init__(self):
		pass

	def getAllocation(self, levels_dir):
		if not os.path.exists(levels_dir):
			print("%s is not a valid file, please check!" % levels_dir)
			sys.exit(1)
		self.levels_dir = levels_dir
		with open(self.levels_dir, 'r') as fr:
			lines = fr.readlines()
			for line in lines:
				for word_level in string.split(line):
					level = string.split(word_level, ':')[1]
					if not self.allocation.has_key(level):
						self.allocation[level] = 1
					else:
						self.allocation[level] += 1

		for key, value in self.allocation.iteritems():
			print("%s\t%d" % (key, value), file=sys.stdout)
   

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='simple count the number of words in levels of tree structure')
	parser.add_argument('--levels', type=str, required=True, help='the path for mode.levels file')
	args = parser.parse_args()

	alloc =WordAllocate()
	alloc.getAllocation(args.levels)
