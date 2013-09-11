#!/usr/bin/env python

###############################################################################
# Copyright (c) 2012-2013 Yohan Lasorsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###############################################################################

###############################################################################
# NTK/Tagger - Search & replace text tags in source files
#
# NTK
# tagger.py
#
# author       : Yohan Lasorsa (noda)
# version      : 1.0
# last change  : 2013-01-03
#
###############################################################################

import argparse
import sys
import re
import os

class Tagger:
    
    ###########################################################################
    # Process the file at the specified path, replacing content matched by the
    # specified list of regular expressions.
    ###########################################################################
    def process_file(self, path):
        
        in_file = open(path, "r")
        content = in_file.read()
        in_file.close()
        
        # remove content matching the user-specified regex
        for regex in self.to_remove:
            content = regex.sub("", content)
        
        # replace content matching the user-specified regex
        for regex in self.to_replace:
            content = regex[0].sub(regex[1], content)
        
        # replace content matching the user-specified tags
        for tag in self.tags:
            regex = re.compile(r'@@' + tag[0] + '@@')
            content = regex.sub(tag[1], content)
        
        # replace content matching the user-specified tags
        for tag in self.tags_file:
            regex = re.compile(r'@@' + tag[0] + '@@')
            tag_file = open(tag[1], "r")
            file_content = tag_file.read()
            tag_file.close()
            content = regex.sub(file_content, content)
        
        out_path = self.output_path
        
        if not out_path:
            out_path = path
        
        out_file = open(out_path, "w")
        out_file.write(content)
        out_file.close()
        
        sys.stdout.write(".")
        sys.stdout.flush()
    
    ###########################################################################
    # Process tagging tall the files contained within the specified folder,
    # using recursive folder traversal
    ###########################################################################
    def process_folder(self, folder, recursive):
        
        if recursive:
            for root, subfolders, files in os.walk(folder):
                for file in files:
                    self.process_file(os.path.join(root, file))
        else:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                
                if not os.path.isdir(file_path):
                    self.process_file(file_path)
    
    
    ###########################################################################
    # Process tagging the input file at the specified path, or all the files
    # contained within the specified folder
    ###########################################################################
    def process(self):
        
        print("Tagging in progress...")
        
        if os.path.isdir(self.input_path):
            self.process_folder(self.input_path, self.recursive)
        else:
            self.process_file(self.input_path)
        
        print("\nSuccess!\n")
    
    ###########################################################################
    # Constructor
    ###########################################################################
    def __init__(self, input_path, output_path, to_remove, to_replace, tags, tags_file, recursive):
        
        self.input_path = input_path
        self.to_remove = []
        self.to_replace = []
        self.tags = []
        self.tags_file = []
        self.recursive = recursive
        self.output_path = ""
        
        if not os.path.isdir(input_path):
            self.output_path = output_path
        
        if to_remove:
            for regex in to_remove:
                self.to_remove.append(re.compile(regex, re.DOTALL))
        
        if to_replace:
            for regex in to_replace:
                self.to_replace.append((re.compile(regex[0], re.DOTALL), regex[1]))
        
        if tags:
            for tag in tags:
                self.tags.append((tag[0], tag[1]))
        
        if tags_file:
            for tag in tags_file:
                self.tags_file.append((tag[0], tag[1]))

###############################################################################
# Entry point of the program.
###############################################################################
def main():
    
    description = "NTK/Tagger search & replace text tags in source files."
    
    argsparser = argparse.ArgumentParser(description=description)
    argsparser.add_argument("input_file", help="the input file or folder to manipulate")
    argsparser.add_argument("-r", "--remove_expr", help="a python regex for content to remove in the file",
                            dest="remove", action="append", metavar="EXPR_TO_REMOVE")
    argsparser.add_argument("-e", "--replace_expr", nargs=2, help="a python regex for content to replace by the followed string in the file",
                            dest="replace", action="append", metavar=("EXPR_TO_REPLACE", "STRING"))
    argsparser.add_argument("-t", "--replace_tag", nargs=2, help="a tag to replace by the followed string in the file",
                            dest="tag", action="append", metavar=("TAG_TO_REPLACE", "STRING"))
    argsparser.add_argument("-f", "--replace_tag_file", nargs=2, help="a tag to replace by the content at the followed path in the file",
                            dest="file", action="append", metavar=("TAG_TO_REPLACE", "PATH"))
    argsparser.add_argument("-o", "--output_file", help="create a new file to output the modifications (by default the modifications are done in-place), has no effect if the target is a folder")
    argsparser.add_argument("-R", "--recursive", help="if the specified input file is a folder, recurse through all subfolders",
                            dest="recursive", action="store_true")
    
    args = argsparser.parse_args()
    Tagger(args.input_file, args.output_file, args.remove, args.replace, args.tag, args.file, args.recursive).process()

main()
