# NTK/Tagger - Search & replace text tags in source files

It is part of the NTK project and aims to ease the process of tagging source
files with specific information like license or version information.

A source file tag have the form: @@tag_name@@ 

It can also performs in-file deletions and replacements using python regular 
expressions.

For more information about python regular expressions, please refer to: 
http://docs.python.org/library/re.html

The text processing is done in the following order:

REGEX DELETE > REGEX REPLACE > TAG REPLACE > TAG FILE REPLACE

## Limitations

The '.' (dot) character matches any character, including newline, to allow
multiline search & replace.

## Requirements

Python v.2.7.0 or higher is required.

## Usage

    tagger.py [-h] [-r EXPR_TO_REMOVE] [-e EXPR_TO_REPLACE STRING]
              [-t TAG_TO_REPLACE STRING] [-f TAG_TO_REPLACE PATH]
              [-o OUTPUT_FILE] [-R]
              input_file

Required arguments:

  * input_file          the input file or folder to manipulate

Optional arguments:

  * `-r EXPR_TO_REMOVE, --remove_expr EXPR_TO_REMOVE`
                        a python regex for content to remove in the file

  * `-e EXPR_TO_REPLACE STRING, --replace_expr EXPR_TO_REPLACE STRING`
                        a python regex for content to replace by the followed 
                        string in the file

  * `-t TAG_TO_REPLACE STRING, --replace_tag TAG_TO_REPLACE STRING
                        a tag to replace by the followed string in the file
                        
  * `-f TAG_TO_REPLACE PATH, --replace_tag_file TAG_TO_REPLACE STRING
                        a tag to replace by the content at the followed path
                        in the file
                        
  * `-o OUTPUT_FILE, --output_file OUTPUT_FILE
                        create a new file to output the modifications (by
                        default the modifications are done in-place), has no
                        effect if the target is a folder
                        
  * `-R, --recursive    if the specified input file is a folder, recurse
                        through all subfolders
