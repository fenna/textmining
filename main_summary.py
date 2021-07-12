#!/usr/bin/env python3

"""
This program reads a OCR processed file and extract a summary text
The program uses a text summarizer algorithm based on text ranking
"""

__author__ = "F.Feenstra"

#IMPORTS
import sys
import pandas as pd
import ddsum as tr
import csv

def read_doc(file):
    """read a cleaned file"""
    df = pd.read_csv(file, 
                  header = None, 
                  delimiter="\t", 
                  quoting=csv.QUOTE_NONE, 
                  encoding='utf-8', 
                  names = ['doc', 'line', 'text', 'cleaned'])
    df = df.dropna(axis = 0)
    return df


def get_header(df):
    """fetch the first 15 lines for the header info"""
    df_lines = df.groupby('line').cleaned.apply(list).reset_index()
    df_lines.cleaned = df_lines.cleaned.apply(" ".join)
    return " ".join(df_lines.cleaned[:15])


def main(args):
    """ main function that calls header and sumtext functions """
    if len(args) < 2:
        print("please provide the name of an input file")
        print("Program stopping...")
        return 1
    docs = args[1:]
    for file in docs:
        try: 
            df = read_doc(file)
            print(f'\nBestand: {file}')
            header = get_header(df)  
            print(f'Header: \n {header}')
            with open('doc_txt', 'w') as out:
                out.write(" ".join(df.cleaned))     
            sum_txt = tr.generate_summary('doc_txt', 2)
            print(sum_txt)
        except:
            print('kan niet goed processen')
    return 0


if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)
