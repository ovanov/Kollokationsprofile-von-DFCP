import re
from typing import Dict, List

import pandas as pd
from pandas.core.frame import DataFrame


def preprocess_text(filename: str) -> List:
    """
    This function reads a filename and returns a list of lists
    The list consists of the 10 words, that occur before 'dass'
    """

    listed_words = []
    with open(filename, 'r') as annis:
        for line in annis:
            if re.search(r"\d+\.\t", line) != None: # take only the needed lines

                line = re.sub(r'\d+\.\ttok\s\s', "", line) # strip off the beginning, which is not needed
                line = re.sub(r'dass\s$', "", line) # when handling collocators before "dass" we need to strip off also "dass" at the end
                
                listed_words.append(line.split()[::-1]) # we append the reversed list in order to have better data for plotting
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
                word_count_dict[value] = [ # create list of 10 zeros, in order to represent the 10 positions before dass
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ]
                word_count_dict[value][listed_values.index(value)] += 1 # increment at the correct number
            else:
                word_count_dict[value][listed_values.index(value)] += 1

    return word_count_dict


def save_as_csv(collocations: Dict, outfile_name: str) -> DataFrame:
    df = pd.DataFrame.from_dict(collocations, orient='index')

    return df.to_csv(outfile_name, sep='\t')


def main():

    preprocessed_text = preprocess_text('./annis_10word_pr.txt') # read file (txt): change filepath
    collocations = count_collocations(preprocessed_text)
    save_as_csv(collocations, './annis_10word_pr.csv') # write csv from collocations (list[list[(tuple)]])


if __name__ == "__main__":
    main()
