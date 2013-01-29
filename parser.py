import pickle
import re
from Citation import Citation

# begin actual function of parser script
def main():

    # open list of citations
    with open('/home/sphere/development/python/research/citationProject/citation_array.pickle', 'r') as f:
        citation_list = pickle.load(f) 

    # iterate through list
    for entry in citation_list:
        # create a Citation object
        tempCitation = Citation(entry)
        # assign raw data
        tempCitation.getFields()

    #tempCitation = Citation(citation_list[1])
    #tempCitation.getFields()
    print 'finished'
main()
