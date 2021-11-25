import re
from typing import Dict, List

import pandas as pd
from pandas.core.frame import DataFrame


def preprocess_text(filename: str) -> List:
    """
    This function reads a filename and returns a list of lists
    The list consists of the 10 words, that occur after 'dass'
    """
    listed_words = []
    with open(filename, 'r') as annis:
        for line in annis:
            if re.search(r"\d+\.", line) != None: # take only the needed lines 
                if re.search(r"\d+\.\ttok\s\sw\w+\sdass?", line) != None: # check if there is a w-element
                    line = re.sub(r'\d+\.\ttok\s\sw\w+\sdass?', "", line) # strip that part off 
                    listed_words.append(line.split())
                    # print(line.split())
                if re.search(r"\d+\.\s\stok\s\s.+\sdass?", line) != None: # check if there is a phrasal component
                    line = re.sub(r'\d+\.\s\stok\s\s.+\sdass?', "", line) # strip that part off
                    listed_words.append(line.split())
                    # print(line.split())
                if re.search(r"\d+\.\ttok\s\sw\w+\s\w+\sdass?", line) != None: # check if there is a w-element and a phrasal component
                    line = re.sub(r'\d+\.\ttok\s\sw\w+\s\w+\sdass?', "", line) # strip that part of
                    listed_words.append(line.split())
                    # print(line.split())

    return listed_words


def count_collocations(preprocessed_list: List) -> Dict:
    """
    This function reads a list and counts the 10 most occuring collocators in the 10 position after 'dass'
    The dictionary takes the word as a key and the occurances as a enumeration as values
    """
    word_count_dict = {}

    for listed_values in preprocessed_list: #  access single list 
        for value in listed_values: # access single value 
            if value not in word_count_dict.keys(): # if no value is in the dictionary
                word_count_dict[value] = [ # create list of 10 zeros, in order to represent the 10 positions
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

    preprocessed_text = preprocess_text('./w_tot_pos.txt') # read file (txt) : change file path, if needed
    collocations = count_collocations(preprocessed_text)
    save_as_csv(collocations, './w_tot_pos.csv') # write csv from collocations (list[list[(tuple)]])



if __name__ == "__main__":
    main()
