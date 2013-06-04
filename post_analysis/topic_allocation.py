#!/usr/bin/env python 
from __future__ import print_function
from collections import Counter
import sys
import os
import string
import operator
import argparse

class TopicAllocation:
    assign_dir = ""
    mode_dir = ""
    topic_allocation = {}
    topics = {} 
    def __init__(self, assign_dir, mode_dir):
        if not os.path.exists(assign_dir):
            print("Error: %s cannot find, please check!" % assign_dir, file=sys.stderr)
            sys.exit(1)
        elif not os.path.exists(mode_dir):
            print("Error: %s cannot find, please check!" % mode_dir, file=sys.stderr)
            sys.exit(1)
        self.assign_dir = assign_dir
        self.mode_dir = mode_dir
    
    def cal_topic_levels(self):
        """read mode.assign and mode files to calculate the topic levels"""

        with open(self.assign_dir) as fassign:
            for line in fassign.readlines():
                words = string.split(line.strip(), ' ')
                levels = words[2:len(words)]
                for level in range(len(levels)): 
                    if not self.topic_allocation.has_key(str(level)):
                        self.topic_allocation[str(level)] = []
                        self.topic_allocation[str(level)].append(levels[level])
                    else:
                        self.topic_allocation[str(level)].append(levels[level])

        with open(self.mode_dir) as fmode:
            for line in fmode.readlines():
                topic = string.split(line)
                topic_no = topic[0]
                words = topic[1:len(topic)]
                self.topics[topic_no] = words

        print("%s loaded!" % self.assign_dir)
        for key, value in self.topic_allocation.iteritems():
            print("-----------------------------------------------------")
            level_topic = Counter(value)
            print("level %s, total %s topics" % (key, len(level_topic)), file=sys.stdout)
            sorted_level_topic = sorted(level_topic.iteritems(), key=operator.itemgetter(1))
            sorted_level_topic.reverse()
            for (topic, doc_num) in sorted_level_topic:
                print("topicNo: %s\t" % topic, file=sys.stdout, end='')
                if not self.topics.has_key(topic):
                    print("Error: %s cannot find the topics dictionary" % topic, file=sys.stderr)
                    continue
                print("docNo: %s\twordsNo: %s"  % (self.topics[topic][1], self.topics[topic][2]), file=sys.stdout)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='simple topic allocation in each level')
    parser.add_argument('--assign', type=str, required=True, help='mode.assign file path')
    parser.add_argument('--mode', type=str, required=True, help='mode file path')

    args = parser.parse_args()
    
    alloc = TopicAllocation(args.assign, args.mode)
    alloc.cal_topic_levels()

