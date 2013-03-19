# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:56:18 2013

@author: David Stack
"""
import pandas

def main():
    # save text journal text files to pandas data frame
    
    # set to get files from web
    # http://jabref.sourceforge.net/resources.php#downloadlists
    filePaths = ['http://jabref.sourceforge.net/journals/journal_abbreviations_geology_physics.txt']
    
    for filePath in filePaths:
       print 'Reading files...'
       data = pandas.read_csv(filePath, sep='=', skipinitialspace=True, comment='#')
       print data.head(20)
    
    # TODO: write/save all journal names to something other than memory
    # (lookup table)
    # See http://pandas.pydata.org/pandas-docs/stable/io.html
    
# Run main() if module is run as a program
if __name__ == '__main__':
    main()
