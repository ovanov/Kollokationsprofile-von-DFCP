import re
from typing import Dict, List

import pandas as pd
from pandas.core.frame import DataFrame


def preprocess_text(filename: str) -> List:
    """
    This function takes a file path and returns a list of lists
    this list contains all the words that come before a w-elemnt dfcp
    """
    listed_words = []
    with open(filename, 'r') as annis:
        for line in annis:
            if re.search(r"\d+\.", line) != None: # take only the needed lines

                line = re.sub(r'\d+\.\s\stok\s\s', "", line) # strip the beginning off, which is not needed
                if re.search(r'uf\s\w+\s\w+\sdass?\s$',line) != None: # check if there is an 'uf' preposition and a phrasal component
                    line = re.sub(r'uf\s\w+\s\w+\sdass?\s$', "", line) # strip that part off
                    listed_words.append(line.split()[::-1]) # append the reversed list, to plot better graphs
                    print(line.split()[::-1])

                if re.search(r'\w+\sw\w+\sdass?\s$',line) != None: # check if there is a preposition with a w-elents 
                    line = re.sub(r'\w+\sw\w+\sdass?\s$', "", line) # strip that part off
                    listed_words.append(line.split()[::-1]) # appned the reversed list, to plot better graphs 
                    print(line.split()[::-1])

    return listed_words


def count_collocations(preprocessed_list: List) -> Dict:
    """
    This function reads a list and counts the 10 most occuring collocators in the 10 position before 'dass'
    The dictionary takes the word as a key and the occurances as a enumeration as values
    """
    word_count_dict = {}

    for listed_values in preprocessed_list: # access single list
        for value in listed_values: # access single value
            if value not in word_count_dict.keys(): # if no value is in the dictionary
                word_count_dict[value] = [ # create list of 10 zeros, in order to represent 10 positions
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ]
                word_count_dict[value][listed_values.index(value)] += 1 # increment at correct number
            else:
                word_count_dict[value][listed_values.index(value)] += 1

    return word_count_dict


def save_as_csv(collocations: Dict, outfile_name: str) -> DataFrame:
    df = pd.DataFrame.from_dict(collocations, orient='index')

    return df.to_csv(outfile_name, sep='\t')


def main():

    preprocessed_text = preprocess_text('./pre.txt') # read file (txt ) : change file path, if needed
    collocations = count_collocations(preprocessed_text)
    save_as_csv(collocations, './phrasal_pre.csv') # write csvfrom collocations (list[list[(tuple)]])


if __name__ == "__main__":
    main()
