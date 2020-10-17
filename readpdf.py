#!/usr/bin/env python3

"""
script dat een pdf omzet naar een ruwe text
usage: vanaf commandline: python3 readpdf.py <filename>
source: https://growteq.nl/2018/08/17/inhoud-pdf-bestanden-analyseren-met-python/
written by 'Gideon Folkers'
"""
__author__ = 'F. Feenstra'

import sys
import pydoc
import PyPDF2

def read_pdf(filename):
    """
    read the pdf filename and store in python readable object
    parameters: filename provided by cmd
    returns: pdfFileReader object
    """
    pdfFileObj = open(filename,'rb')
    return PyPDF2.PdfFileReader(pdfFileObj)

def pdf_toraw(pdfReader):
    """
    convert the pdftext to raw text
    parameters: pdfFileReader object
    returns: raw text
    """
    num_pages = pdfReader.numPages
    count = 0
    raw_text = ""
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        raw_text += pageObj.extractText()
    return raw_text

def store_raw(raw_text, filename = 'out.txt'):
    """
    store the raw text
    parameters: raw_text
    """
    with open(filename, 'w') as o:
        o.write(raw_text)


def main(argv=None):
    try:
        filename = argv[1]
        text = pdf_toraw(read_pdf(filename))
        store_raw(text, filename[:-4] + '.txt')
    except:
       print(pydoc.help(__name__))
    return 0


if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)
